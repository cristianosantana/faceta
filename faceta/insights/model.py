from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from faceta.db import ROOT

DEFAULT_WINDOW = 8
MODELS_DIR = ROOT / "models" / "insights"


@dataclass
class ModelBundle:
    path: Path
    window: int
    threshold: float
    backend: str  # tf | numpy


def _try_tf():
    try:
        import tensorflow as tf  # noqa: WPS433

        return tf
    except Exception:
        return None


def _windows_from_series(valores: list[float], window: int) -> np.ndarray:
    if len(valores) < window:
        return np.zeros((0, window), dtype=np.float32)
    arr = np.array(valores, dtype=np.float32)
    mu, sigma = float(arr.mean()), float(arr.std() or 1.0)
    arr = (arr - mu) / sigma
    out = [arr[i : i + window] for i in range(len(arr) - window + 1)]
    return np.array(out, dtype=np.float32)


class NumpyAutoencoder:
    """Autoencoder denso mínimo (fallback quando TensorFlow não está disponível)."""

    def __init__(self, window: int, hidden: int = 4, seed: int = 0):
        rng = np.random.default_rng(seed)
        self.window = window
        self.W1 = rng.normal(0, 0.1, (window, 16)).astype(np.float32)
        self.b1 = np.zeros(16, dtype=np.float32)
        self.W2 = rng.normal(0, 0.1, (16, hidden)).astype(np.float32)
        self.b2 = np.zeros(hidden, dtype=np.float32)
        self.W3 = rng.normal(0, 0.1, (hidden, 16)).astype(np.float32)
        self.b3 = np.zeros(16, dtype=np.float32)
        self.W4 = rng.normal(0, 0.1, (16, window)).astype(np.float32)
        self.b4 = np.zeros(window, dtype=np.float32)

    def _forward(self, X: np.ndarray):
        h1 = np.maximum(0, X @ self.W1 + self.b1)
        z = np.maximum(0, h1 @ self.W2 + self.b2)
        h2 = np.maximum(0, z @ self.W3 + self.b3)
        out = h2 @ self.W4 + self.b4
        return out, (h1, z, h2)

    def predict(self, X: np.ndarray) -> np.ndarray:
        # aceita (n, window) ou (n, window, 1)
        flat = X.reshape(X.shape[0], -1)
        out, _ = self._forward(flat)
        return out.reshape(X.shape[0], self.window, 1) if X.ndim == 3 else out

    def fit(self, X: np.ndarray, epochs: int = 40, lr: float = 0.05) -> None:
        flat = X.reshape(X.shape[0], -1)
        n = len(flat)
        for _ in range(epochs):
            idx = np.random.permutation(n)
            for i in idx:
                x = flat[i : i + 1]
                out, (h1, z, h2) = self._forward(x)
                err = out - x
                # grads simplificados
                dW4 = h2.T @ err
                db4 = err.sum(axis=0)
                dh2 = err @ self.W4.T
                dh2 *= (h2 > 0)
                dW3 = z.T @ dh2
                db3 = dh2.sum(axis=0)
                dz = dh2 @ self.W3.T
                dz *= (z > 0)
                dW2 = h1.T @ dz
                db2 = dz.sum(axis=0)
                dh1 = dz @ self.W2.T
                dh1 *= (h1 > 0)
                dW1 = x.T @ dh1
                db1 = dh1.sum(axis=0)
                self.W4 -= lr * dW4
                self.b4 -= lr * db4
                self.W3 -= lr * dW3
                self.b3 -= lr * db3
                self.W2 -= lr * dW2
                self.b2 -= lr * db2
                self.W1 -= lr * dW1
                self.b1 -= lr * db1

    def save(self, path: Path) -> None:
        np.savez(
            path,
            W1=self.W1,
            b1=self.b1,
            W2=self.W2,
            b2=self.b2,
            W3=self.W3,
            b3=self.b3,
            W4=self.W4,
            b4=self.b4,
            window=self.window,
        )

    @classmethod
    def load(cls, path: Path) -> NumpyAutoencoder:
        data = np.load(path)
        m = cls(window=int(data["window"]))
        m.W1, m.b1 = data["W1"], data["b1"]
        m.W2, m.b2 = data["W2"], data["b2"]
        m.W3, m.b3 = data["W3"], data["b3"]
        m.W4, m.b4 = data["W4"], data["b4"]
        return m


def build_autoencoder(window: int):
    tf = _try_tf()
    if tf is None:
        return NumpyAutoencoder(window), "numpy"
    inp = tf.keras.Input(shape=(window, 1))
    x = tf.keras.layers.Flatten()(inp)
    x = tf.keras.layers.Dense(16, activation="relu")(x)
    x = tf.keras.layers.Dense(4, activation="relu")(x)
    x = tf.keras.layers.Dense(16, activation="relu")(x)
    x = tf.keras.layers.Dense(window, activation="linear")(x)
    out = tf.keras.layers.Reshape((window, 1))(x)
    model = tf.keras.Model(inp, out)
    model.compile(optimizer="adam", loss="mse")
    return model, "tf"


def _bootstrap_series(
    series_valores: list[list[float]],
    *,
    target_len: int = 12,
) -> list[list[float]]:
    """Amplia séries curtas com ruído para permitir treino inicial (dev/demo)."""
    rng = np.random.default_rng(7)
    out: list[list[float]] = []
    for vals in series_valores:
        if not vals:
            continue
        base = np.array(vals, dtype=np.float32)
        mu = float(base.mean())
        sigma = float(base.std() or abs(mu) * 0.05 or 1.0)
        synth = mu + rng.normal(0, sigma, size=target_len)
        # preserva último valor real
        synth[-1] = base[-1]
        out.append(synth.tolist())
        # cópia com spike artificial para ensinar o AE o que é "normal"
        out.append((mu + rng.normal(0, sigma * 0.5, size=target_len)).tolist())
    return out or [[100.0] * target_len]


def train_autoencoder(
    series_valores: list[list[float]],
    *,
    window: int = DEFAULT_WINDOW,
    epochs: int = 40,
    entity_type: str,
    granularidade: str,
) -> ModelBundle:
    lens = [len(v) for v in series_valores if v]
    if not lens:
        raise RuntimeError("nenhuma série com dados para treino")
    max_len = max(lens)
    if max_len < 3:
        # bootstrap: gera variações sintéticas a partir dos pontos existentes
        series_valores = _bootstrap_series(series_valores, target_len=max(window, 12))
        lens = [len(v) for v in series_valores]
        max_len = max(lens)
    window = min(window, max_len)
    window = max(3, window)

    X_list = [_windows_from_series(v, window) for v in series_valores]
    X_list = [x for x in X_list if len(x)]
    if not X_list:
        raise RuntimeError(
            f"histórico insuficiente para treino (precisa ≥{window} pontos por série)"
        )
    X2d = np.concatenate(X_list, axis=0)
    model, backend = build_autoencoder(window)

    out_dir = MODELS_DIR / f"{entity_type}_{granularidade}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if backend == "tf":
        X = X2d.reshape(-1, window, 1)
        model.fit(X, X, epochs=epochs, batch_size=min(32, len(X)), verbose=0)
        recon = model.predict(X, verbose=0)
        errs = np.mean((recon - X) ** 2, axis=(1, 2))
        model.save(out_dir / "autoencoder.keras")
    else:
        model.fit(X2d, epochs=epochs)
        recon = model.predict(X2d)
        errs = np.mean((recon - X2d) ** 2, axis=1)
        model.save(out_dir / "autoencoder.npz")

    p95 = float(np.percentile(errs, 95))
    p99 = float(np.percentile(errs, 99))
    env_thr = os.getenv("INSIGHT_DETECTION_THRESHOLD")
    threshold = float(env_thr) if env_thr else max(p95 * 1.5, p99)
    threshold = max(threshold, 1e-6)

    meta = {
        "window": window,
        "threshold": threshold,
        "p95_treino": p95,
        "n_windows": int(len(X2d)),
        "backend": backend,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return ModelBundle(path=out_dir, window=window, threshold=threshold, backend=backend)


def load_bundle(entity_type: str, granularidade: str) -> tuple[object, ModelBundle]:
    out_dir = MODELS_DIR / f"{entity_type}_{granularidade}"
    meta_path = out_dir / "meta.json"
    if not meta_path.is_file():
        raise FileNotFoundError(
            f"modelo não treinado: {out_dir}. Rode: python -m faceta.insights train ..."
        )
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    backend = meta.get("backend", "tf")
    if backend == "numpy" or not (out_dir / "autoencoder.keras").is_file():
        model = NumpyAutoencoder.load(out_dir / "autoencoder.npz")
        backend = "numpy"
    else:
        tf = _try_tf()
        if tf is None:
            raise RuntimeError("modelo TF salvo, mas tensorflow não instalado")
        model = tf.keras.models.load_model(out_dir / "autoencoder.keras")
    bundle = ModelBundle(
        path=out_dir,
        window=int(meta["window"]),
        threshold=float(meta["threshold"]),
        backend=backend,
    )
    return model, bundle


def reconstruction_error(model, valores: list[float], *, window: int) -> float | None:
    X2d = _windows_from_series(valores, window)
    if len(X2d) == 0:
        return None
    last = X2d[-1:]
    if isinstance(model, NumpyAutoencoder):
        recon = model.predict(last)
        return float(np.mean((recon - last) ** 2))
    X = last.reshape(1, window, 1)
    recon = model.predict(X, verbose=0)
    return float(np.mean((recon - X) ** 2))


def detect_signal(erro: float | None, threshold: float) -> bool:
    if erro is None:
        return False
    return erro > threshold
