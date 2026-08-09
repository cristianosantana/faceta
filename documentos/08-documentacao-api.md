# Documentação de API (Proposta)

> Este endpoint é uma proposta baseada no que foi discutido. Ainda não foi validado como requisito formal — `[PENDENTE]` confirmar se o acesso será via API HTTP, leitura direta ao Postgres, ou ambos.

## `GET /consulta`
Executa o motor de consulta genérico, roteando internamente para a família de fato correta (`fato_os`, `fato_os_servico`, `fato_os_pagamento` ou `fato_comissao`) conforme o `entity_type` pedido, aplicando comparações e ranking quando solicitados. Corresponde exatamente à saída da camada de Entendimento de Pergunta — quem chama esse endpoint nunca precisa saber a qual família o `entity_type` pertence.

**Parâmetros (query)**
| Nome | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `entity_type` | string | sim | Um dos tipos válidos no contrato (ex.: `concessionaria`, `vendedor`, `servico`, `forma_pagamento`, `comissao`) |
| `entity_id` | string | não | Se informado, filtra para uma entidade específica; se omitido, retorna todas (ex.: para ranking) |
| `granularidade` | string | sim | `diario` \| `semanal` \| `mensal` \| `semestral` \| `anual` |
| `periodo` | string | sim | Ex.: `2026-08-07`, `2026-W31`, `2026-08`, `2026-H1`, `2026` |
| `quebra` | string | não | Dimensão da quebra (ex.: `departamento`); deve estar prevista no contrato para o `entity_type`, e nunca cruza `servico` com `forma_pagamento` |
| `comparacao` | string | não | `vs_periodo_anterior` \| `vs_mesmo_periodo_ano_anterior` |
| `ranking` | boolean | não | Se `true`, retorna a lista ordenada de todas as entidades do `entity_type` no período |

**Resposta 200**
```json
{
  "entity_type": "vendedor",
  "entity_id": "vendedor_joao",
  "granularidade": "mensal",
  "periodo": "2026-08",
  "quebra": null,
  "valor": 59000.00,
  "quantidade_os": 22,
  "comparacoes": {
    "vs_periodo_anterior": { "valor_anterior": 54500.00, "variacao_pct": 8.3 }
  },
  "insight": { "assunto": "...", "descricao": "...", "confianca": 0.85 }
}
```
`insight` só aparece se existir linha correspondente na tabela `insights`; caso contrário é omitido.

**Resposta 400** — `entity_type` ou `quebra` fora do contrato, ou tentativa de cruzar `servico` com `forma_pagamento` (rejeitado pela allowlist antes de qualquer consulta ao banco)
**Resposta 404** — combinação válida no contrato, mas sem dado para o período pedido

## Observações
- Nenhuma resposta é pré-computada — a agregação roda na hora, sobre a tabela de fato (família + granularidade) já reduzida pelo tempo
- `[PENDENTE]` autenticação/autorização do endpoint, formato de erro padrão, versionamento de API, limites de taxa para consultas de `ranking` sem `entity_id`
