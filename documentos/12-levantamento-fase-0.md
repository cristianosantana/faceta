# Levantamento Fase 0 — MySQL `smart`

> Gerado em `2026-08-09 17:24:56` por `scripts/fase0_levantamento.py`.

## Correções pós-geração (Fase 1 — vigentes)

> O corpo abaixo é o dump gerado pelo script. **Use esta seção como verdade atual** para mapeamento Faceta (atualizado após implementação da Fase 1).

| Conceito | Correção |
|---|---|
| `familia_servico` | **`subgrupos_servicos`** via `servicos.subgrupo_servico_id` — **não** `grupos_servicos` |
| `familia_produto` | **`subgrupos_produtos`** via `grupo_produto_id` |
| `servico` | dimensão `dim_servico` + coluna `servico_id` em `fato_os_servico` (grão serviço a serviço) |
| `fato_comissao` | colunas `comissionado_id` + `comissao_tipo_id` (iguais ao MySQL); **não** usar `beneficiario_*` nem derivar tipo de `funcionario_tipos`/cargo |
| Snapshots Postgres | `dim_*` em `memoria_materializada` — ver `10-dicionario-dados.md` §1.2 e `13-fase1-ingestao.md` |

## 1. Conclusões (Fase 0)

- **Schema cadastral:** validado no live.
- **Comissão:** origem `comissoes` (+ `comissao_tipos`, `comissao_periodos`, `comissao_pagamentos`); fórmula `valor_comissao = COALESCE(valor_dentro,0) + COALESCE(valor_fora,0) + COALESCE(valor_combo,0) + COALESCE(valor_compensado_permuta,0) + COALESCE(comissao_couro,0)`.
- **Vendedor/produtivo:** `funcionarios` discriminados por `funcionario_tipos` (via `funcionario_cargos` → `cargos`).
- **Estados:** paga = `paga`+`caixas`; fechada = itens ativos todos fechados (`os_servicos` XOR `os_produtos`); cancelada = `os.cancelada`; `paga=1` sem `caixas` = inconsistência (não cancelada); `os.finalizada` não é critério analítico.
- **Frequência:** ingestão diária do dia D−1 por recorte; OS fechadas (derivadas) sem comissão no período: `35`.
- **Divergências/inconsistências:** fechada flag↔derivada `21`; paga sem caixa `118` (fechada `107`); exclusividade `0`.

## 2. Schema introspectado

### `departamentos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(30) | NO |  |
| sigla | varchar(4) | NO |  |
| sigla_carbel | varchar(255) | YES |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `concessionarias`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(200) | NO |  |
| nome_carbel | varchar(255) | YES |  |
| razao_social | varchar(100) | NO |  |
| cnpj | varchar(14) | NO |  |
| ie | varchar(14) | YES |  |
| im | varchar(14) | YES |  |
| cep | varchar(8) | NO |  |
| logradouro | varchar(100) | NO |  |
| bairro | varchar(100) | NO |  |
| localidade | varchar(100) | NO |  |
| uf | char(2) | NO |  |
| codigo_ibge | varchar(7) | YES |  |
| numero | int | NO |  |
| complemento | varchar(30) | YES |  |
| retem_iss | tinyint(1) | NO |  |
| iss_percentual | decimal(5,2) | NO |  |
| aceita_indicador1 | tinyint(1) | NO |  |
| aceita_indicador2 | tinyint(1) | NO |  |
| restringe_requisicao_kit | tinyint(1) | NO |  |
| edita_observacao_nf | tinyint(1) | NO |  |
| permite_deposito_ci | tinyint(1) | NO |  |
| permite_pcp | tinyint(1) | NO |  |
| permite_vendas_materiais | tinyint(1) | NO |  |
| dias_execucao | int unsigned | NO |  |
| produtivo_base_id | int unsigned | YES | MUL |
| concessionaria_execucao_id | int unsigned | YES | MUL |
| vendedor_responsavel_nf | tinyint(1) | NO |  |
| cancelamento_automatico | tinyint(1) | NO |  |
| dias_cancelamento_automatico | int | NO |  |
| cancelamento_automatico_proposta | tinyint(1) | NO |  |
| dias_cancelamento_automatico_proposta | int | NO |  |
| integracao_carbel | tinyint(1) | NO |  |
| chassis_nf_cortesia | enum('P','S','M') | YES |  |
| numero_controle_nf_cortesia | varchar(255) | NO |  |
| carro_marca_id | int unsigned | NO | MUL |
| comissao_periodo_id | int unsigned | YES | MUL |
| nota_tipo_id | int unsigned | YES | MUL |
| supervisor_vendas_id | int unsigned | YES | MUL |
| cluster_id | bigint unsigned | YES | MUL |
| business_unit_id | bigint unsigned | NO | MUL |
| empresa_faturamento_id | int unsigned | YES | MUL |
| email_vendedora | varchar(50) | YES |  |
| ramal_vendedora | varchar(11) | YES |  |
| gerente_nome | varchar(70) | NO |  |
| gerente_email | varchar(70) | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES | MUL |
| bloqueio | tinyint(1) | YES |  |
| region_id | bigint unsigned | YES | MUL |

### `grupos_servicos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(30) | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `funcionarios`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(50) | NO |  |
| cpf | varchar(11) | YES | UNI |
| rg | varchar(9) | YES | UNI |
| data_nascimento | datetime | YES |  |
| telefone | varchar(15) | YES |  |
| email | varchar(30) | YES |  |
| agencia | varchar(255) | YES |  |
| conta | varchar(255) | YES |  |
| url_foto | varchar(255) | YES |  |
| terceiros | tinyint(1) | NO |  |
| freelancer | tinyint(1) | NO |  |
| codigo_contabilidade | int unsigned | YES |  |
| fornecedor_id | int unsigned | YES | MUL |
| banco_id | int unsigned | YES | MUL |
| banco_conta_tipo_id | int unsigned | YES | MUL |
| funcionario_situacao_id | int unsigned | YES | MUL |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES | MUL |
| raca_cor_id | int | YES |  |

### `funcionario_tipos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(30) | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `funcionario_cargos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| matricula | varchar(255) | YES |  |
| salario | decimal(8,2) | NO |  |
| data_admissao | date | NO |  |
| demitido | tinyint(1) | NO |  |
| data_demissao | date | YES |  |
| motivo_demissao | text | YES |  |
| fixo | tinyint(1) | NO |  |
| reemprego | tinyint(1) | NO |  |
| periodo_experiencia | tinyint(1) | NO |  |
| inicio_experiencia | date | YES |  |
| fim_experiencia | date | YES |  |
| funcionario_id | int unsigned | NO | MUL |
| cargo_id | int unsigned | NO | MUL |
| empresa_id | int unsigned | YES | MUL |
| produtivo_tipo_id | int unsigned | YES | MUL |
| funcionario_local_id | bigint unsigned | YES | MUL |
| concessionaria_local_id | int unsigned | YES | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `cargos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| cbo | int unsigned | YES |  |
| nome | varchar(100) | NO |  |
| descricao | text | YES |  |
| salario_base | decimal(8,2) unsigned | NO |  |
| ativo | tinyint(1) | NO |  |
| funcionario_tipo_id | int unsigned | NO | MUL |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `caixa_tipos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(30) | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `empresas`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(30) | NO |  |
| razao_social | varchar(100) | NO |  |
| cnpj | varchar(14) | NO |  |
| ie | varchar(14) | YES |  |
| im | varchar(14) | YES |  |
| cep | varchar(8) | NO |  |
| logradouro | varchar(80) | NO |  |
| bairro | varchar(30) | NO |  |
| localidade | varchar(30) | NO |  |
| uf | char(2) | NO |  |
| codigo_ibge | varchar(7) | YES |  |
| numero | int | NO |  |
| complemento | varchar(30) | YES |  |
| layout_nfse | enum('UNIFICADO','BH') | NO |  |
| optante_simples_nacional | tinyint(1) | NO |  |
| crt | tinyint unsigned | YES |  |
| token_ibpt | varchar(64) | YES |  |
| token_sefaz_nfce | varchar(255) | YES |  |
| estabelecimento_cielo | varchar(255) | YES |  |
| user_edi_cielo | varchar(255) | YES |  |
| password_edi_cielo | varchar(255) | YES |  |
| merchant_id | varchar(255) | YES |  |
| merchant_key | varchar(255) | YES |  |
| faturamento_maximo | decimal(10,2) | NO |  |
| numero_empresa_remessa | varchar(255) | YES |  |
| pix_key | varchar(255) | YES |  |
| pix_client_id | varchar(255) | YES |  |
| pix_client_secret | varchar(255) | YES |  |
| pix_access_token | text | YES |  |
| pix_access_token_expiration_date | datetime | YES |  |
| pix_tentativas | int unsigned | NO |  |
| cert_path | varchar(255) | YES |  |
| ssl_key_path | varchar(255) | YES |  |
| url_logo | varchar(100) | YES |  |
| flash_company_id | varchar(255) | YES |  |
| flash_token | varchar(255) | YES |  |
| a1_cert_path | varchar(255) | YES |  |
| a1_cert_password | varchar(255) | YES |  |
| a1_cert_created_at | datetime | YES |  |
| a1_cert_expired_at | datetime | YES |  |
| business_unit_id | bigint unsigned | NO | MUL |
| porcentagem_valor_nota_produto | int | NO |  |
| valor_trib_federal | decimal(7,2) | NO |  |
| valor_trib_estadual | decimal(7,2) | NO |  |
| valor_trib_municipal | decimal(7,2) | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `os`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| uuid | char(36) | NO | UNI |
| os_concessionaria | int unsigned | NO |  |
| tipo_atendimento | enum('PRESENCIAL','TELEFONE','WHATSAPP') | YES |  |
| valor_bruto | decimal(8,2) unsigned | NO |  |
| valor_liquido | decimal(8,2) unsigned | NO |  |
| retencao_iss | tinyint(1) | NO |  |
| paga | tinyint(1) | NO | MUL |
| desconto_aprovado | decimal(10,2) | NO |  |
| data_pagamento | datetime | YES | MUL |
| observacao_pagamento | text | YES |  |
| usuario_pagamento_id | int unsigned | YES | MUL |
| fechada | tinyint(1) | NO | MUL |
| data_fechamento | datetime | YES |  |
| finalizada | tinyint(1) | NO |  |
| data_finalizacao | datetime | YES |  |
| cancelada | tinyint(1) | NO | MUL |
| estornada | tinyint(1) | NO |  |
| data_cancelamento | datetime | YES | MUL |
| solicitado_cancelamento | tinyint(1) | NO |  |
| motivo_cancelamento | text | YES |  |
| cancelamento_recusado | tinyint(1) | YES |  |
| data_recusa_cancelamento | datetime | YES |  |
| cancelamento_motivo_id | int unsigned | YES | MUL |
| contato_cliente_cancelamento | tinyint(1) | YES |  |
| descricao_contato_cancelamento | text | YES |  |
| os_retorno | tinyint(1) | NO |  |
| atendimento_telefonico | tinyint(1) | NO |  |
| nota_solicitada | tinyint(1) | NO |  |
| nota_solicitada_motivo | varchar(255) | YES |  |
| data_solicitacao_nfe | datetime | YES |  |
| nota_aprovada | tinyint(1) | NO |  |
| data_aprovacao_nfe | datetime | YES |  |
| usuario_aprovacao_nfe_id | int unsigned | YES | MUL |
| cep | varchar(8) | YES |  |
| logradouro | varchar(80) | YES |  |
| bairro | varchar(80) | YES |  |
| localidade | varchar(80) | YES |  |
| uf | char(2) | YES |  |
| codigo_ibge | varchar(7) | YES |  |
| numero | int | YES |  |
| complemento | varchar(50) | YES |  |
| data_entrega | datetime | YES | MUL |
| data_edicao_entrega | datetime | YES |  |
| entrega_confirmada | tinyint(1) | NO |  |
| data_confirmacao_entrega | datetime | YES |  |
| execucao_mesmo_dia | tinyint(1) | NO |  |
| email_garantia_enviado | tinyint(1) | NO |  |
| data_envio_garantia | datetime | YES |  |
| observacao_os | text | YES |  |
| observacao_producao | text | YES |  |
| observacao_nf | text | YES |  |
| justificada_concessionaria | tinyint(1) | NO |  |
| desconto_Avista | tinyint(1) | NO |  |
| confirmar_retem_iss | tinyint(1) | NO |  |
| cortesia_migrada | tinyint(1) | NO |  |
| data_migracao_cortesia | date | YES |  |
| nome_responsavel_pj | varchar(255) | YES |  |
| cpf_responsavel_pj | varchar(14) | YES |  |
| nivel_indicador1 | int unsigned | YES |  |
| nivel_indicador2 | int unsigned | YES |  |
| indicador1_id | int unsigned | YES | MUL |
| indicador2_id | int unsigned | YES | MUL |
| departamento_id | int unsigned | NO | MUL |
| vendedor_id | int unsigned | NO | MUL |
| concessionaria_id | int unsigned | NO | MUL |
| cliente_carro_id | int unsigned | NO | MUL |
| cliente_id | int unsigned | NO | MUL |
| os_tipo_id | int unsigned | NO | MUL |
| proposta_id | int unsigned | YES | MUL |
| pre_proposta_id | bigint unsigned | YES | MUL |
| os_retorno_id | int unsigned | YES | MUL |
| os_migracao_cortesia_id | int | YES | MUL |
| usuario_recusa_cancelamento_id | int unsigned | YES | MUL |
| funcionario_confirmacao_entrega_id | int unsigned | YES | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES | MUL |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES | MUL |
| id_antigo | int | YES |  |
| usuario_atendimento_cancelamento_id | int unsigned | YES | MUL |
| justificativa_supervisao | int | YES |  |
| justificativa_supervisao_usuario_id | int | YES |  |
| justificativa_supervisao_texto | text | YES |  |

### `os_servicos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| codigo | varchar(255) | YES |  |
| valor_venda | decimal(8,2) | NO |  |
| valor_original | decimal(8,2) | NO |  |
| desconto_supervisao | decimal(8,2) | NO |  |
| desconto_migracao_cortesia | decimal(8,2) | NO |  |
| desconto_avista | decimal(8,2) | NO |  |
| valor_venda_real | decimal(8,2) | YES |  |
| desconto_bonus | decimal(8,2) unsigned | NO |  |
| fechado | tinyint(1) | NO | MUL |
| codigo_fechamento | varchar(35) | NO |  |
| data_fechamento | datetime | YES |  |
| tempo_execucao | int unsigned | YES |  |
| data_inicio | datetime | YES | MUL |
| fechado_sem_codigo | tinyint(1) | NO |  |
| justificativa_sem_codigo | text | YES |  |
| cancelado | tinyint(1) | NO | MUL |
| data_cancelamento | datetime | YES |  |
| solicitado_cancelamento | tinyint(1) | NO |  |
| token_segunda_aplicacao | varchar(255) | YES |  |
| executada_segunda_aplicacao | tinyint(1) | NO |  |
| ordem_pcp | int unsigned | YES |  |
| os_id | int unsigned | NO | MUL |
| os_tipo_id | int unsigned | YES | MUL |
| servico_id | int unsigned | NO | MUL |
| tonalidade_id | int unsigned | YES | MUL |
| combo_id | int unsigned | YES | MUL |
| produtivo_id | int unsigned | YES | MUL |
| concessionaria_execucao_id | int unsigned | YES | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES | MUL |
| plotter_corte_id | int unsigned | YES | MUL |

### `os_produtos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| codigo | varchar(255) | NO |  |
| metragem | decimal(8,2) | YES |  |
| valor_venda | decimal(8,2) unsigned | NO |  |
| valor_original | decimal(8,2) unsigned | NO |  |
| desconto_supervisao | decimal(8,2) unsigned | NO |  |
| desconto_migracao_cortesia | decimal(8,2) unsigned | NO |  |
| desconto_avista | decimal(8,2) unsigned | NO |  |
| desconto_bonus | decimal(8,2) unsigned | NO |  |
| valor_venda_real | decimal(8,2) | YES |  |
| fechado | tinyint(1) | NO |  |
| codigo_fechamento | varchar(255) | NO |  |
| data_fechamento | datetime | YES |  |
| fechado_sem_codigo | tinyint(1) | NO |  |
| justificativa_sem_codigo | varchar(255) | YES |  |
| cancelado | tinyint(1) | NO |  |
| data_cancelamento | datetime | YES |  |
| solicitado_cancelamento | tinyint(1) | NO |  |
| os_id | int unsigned | NO | MUL |
| os_tipo_id | int unsigned | NO | MUL |
| produto_id | int unsigned | NO | MUL |
| tonalidade_id | int unsigned | YES | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `servicos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(200) | NO |  |
| custo_fixo | decimal(8,2) unsigned | NO |  |
| codigo_nf | varchar(30) | NO |  |
| fecha_kit | tinyint(1) | NO |  |
| fecha_peca_avulsa | tinyint(1) | NO |  |
| fecha_peca | tinyint(1) | NO |  |
| fecha_produto | tinyint(1) | NO |  |
| fecha_produtivo | tinyint(1) | NO | MUL |
| diferencia_departamento_preco | tinyint(1) | NO |  |
| diferencia_porte | tinyint(1) | NO |  |
| diferencia_departamento | tinyint(1) | NO |  |
| diferencia_porte_comissao | tinyint(1) | NO |  |
| diferencia_tempo_departamento | tinyint(1) | NO |  |
| diferencia_tempo_cor | tinyint(1) | NO |  |
| credito_necessario | int unsigned | NO |  |
| valor_desconto_cortesia | decimal(8,2) unsigned | NO |  |
| aceita_desconto_cortesia | tinyint(1) | NO |  |
| segunda_aplicacao | tinyint(1) | NO |  |
| grupo_servico_id | int unsigned | NO | MUL |
| subgrupo_servico_id | int unsigned | NO | MUL |
| servico_categoria_id | bigint unsigned | YES | MUL |
| tags | varchar(30) | YES |  |
| ativo | tinyint(1) | NO | MUL |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES | MUL |

### `caixas`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| valor | decimal(8,2) | NO |  |
| desconto | decimal(10,2) | NO |  |
| data_vencimento | date | NO | MUL |
| data_pagamento | datetime | NO | MUL |
| cancelado | tinyint(1) | NO |  |
| data_cancelamento | datetime | YES |  |
| fechado | tinyint(1) | NO |  |
| data_fechamento | datetime | YES |  |
| classificado | tinyint(1) | NO |  |
| data_classificacao | datetime | YES |  |
| finalizado | tinyint(1) | NO |  |
| verificado | tinyint(1) | NO |  |
| data_verificacao | datetime | YES |  |
| data_finalizacao | datetime | YES |  |
| parcela | int unsigned | NO |  |
| quant_parcelas | int unsigned | NO |  |
| nome_depositante | varchar(40) | YES |  |
| codigo_transacao | varchar(30) | YES |  |
| nome_titular | varchar(40) | YES |  |
| doc_titular | varchar(14) | YES |  |
| telefone_titular | varchar(15) | YES |  |
| tid_cielo | varchar(36) | YES | MUL |
| taxa_cartao | decimal(4,4) unsigned | NO |  |
| taxa_antecipacao | decimal(4,4) unsigned | NO |  |
| bandeira_cartao | varchar(30) | NO | MUL |
| codigo_autorizacao | varchar(36) | YES |  |
| numero_autorizacao | varchar(36) | YES |  |
| nome_cartao | varchar(36) | YES |  |
| cc_conciliado | int | NO |  |
| pix_payload | varchar(255) | YES |  |
| pix_info_pagador | varchar(255) | YES |  |
| pix_e2ed_id | varchar(255) | YES | UNI |
| pix_rtr_id | varchar(255) | YES |  |
| observacao_financeiro | text | YES |  |
| caixa_preto | tinyint(1) | NO |  |
| usuario_pagamento_id | int unsigned | YES | MUL |
| usuario_verificacao_id | int unsigned | YES | MUL |
| caixa_conta_id | int unsigned | YES | MUL |
| caixa_tipo_id | int unsigned | NO | MUL |
| caixa_pendente_id | bigint unsigned | YES | MUL |
| caixa_status_id | int unsigned | NO | MUL |
| caixa_fechamento_id | int unsigned | YES | MUL |
| caixa_antecipacao_id | bigint unsigned | YES | MUL |
| caixa_original_id | int unsigned | YES | MUL |
| empresa_faturamento_id | int unsigned | YES | MUL |
| financeiro_malote_classificacao_id | int unsigned | YES | MUL |
| financeiro_caixa_destino_id | int unsigned | YES | MUL |
| os_id | int unsigned | NO | MUL |
| mc_conciliacao_lancamento_id | bigint unsigned | YES | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `caixas_pendentes`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | bigint unsigned | NO | PRI |
| valor | decimal(8,2) unsigned | NO |  |
| desconto | decimal(10,2) | NO |  |
| codigo_transacao | varchar(30) | YES |  |
| data_vencimento | date | YES |  |
| parcela | int unsigned | NO |  |
| quant_parcelas | int unsigned | NO |  |
| expiracao | int unsigned | YES |  |
| pix_tx_id | varchar(36) | YES |  |
| pix_payload | varchar(255) | YES |  |
| pix_tentativas | int unsigned | NO |  |
| pix_br_code | text | YES |  |
| pix_info_pagador | varchar(255) | YES |  |
| pix_e2ed_id | varchar(255) | YES |  |
| pix_rtr_id | varchar(255) | YES |  |
| data_criacao_cobranca | datetime | YES |  |
| data_expiracao_cobranca | datetime | YES |  |
| fechado | tinyint(1) | NO |  |
| data_fechamento | datetime | YES |  |
| finalizado | tinyint(1) | NO |  |
| data_finalizacao | datetime | YES |  |
| cancelado | tinyint(1) | NO |  |
| data_cancelamento | datetime | YES |  |
| caixa_tipo_id | int unsigned | NO | MUL |
| caixa_status_id | int unsigned | YES | MUL |
| caixa_fechamento_id | int unsigned | YES | MUL |
| os_id | int unsigned | NO | MUL |
| empresa_id | int unsigned | YES | MUL |
| remessa_os_id | int unsigned | YES | MUL |
| tipo_remessa_id | int unsigned | YES | MUL |
| usuario_pagamento_id | int unsigned | YES | MUL |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `comissoes`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| valor_dentro | decimal(8,2) | NO |  |
| valor_fora | decimal(8,2) | NO |  |
| valor_combo | decimal(8,2) unsigned | YES |  |
| valor_compensado_permuta | decimal(12,2) | NO |  |
| comissao_couro | tinyint(1) | NO |  |
| paga | tinyint(1) | NO |  |
| data_pagamento | date | YES |  |
| estorno | tinyint(1) | NO |  |
| observacao_estorno | text | YES |  |
| comissionado_id | int | NO |  |
| os_servico_id | int unsigned | YES | MUL |
| os_produto_id | int unsigned | YES | MUL |
| comissao_tipo_id | int unsigned | NO | MUL |
| comissao_pagamento_id | int unsigned | YES | MUL |
| comissao_periodo_id | int unsigned | YES | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES | MUL |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |
| comissao_estorno_id | int unsigned | YES | MUL |
| nf_entrada_id | bigint unsigned | YES | MUL |
| mc_lancamento_entrada_id | bigint unsigned | YES | MUL |

### `comissao_tipos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(30) | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `comissao_periodos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| nome | varchar(100) | NO |  |
| inicio | int unsigned | NO |  |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

### `comissao_pagamentos`

| coluna | tipo | nullable | key |
| --- | --- | --- | --- |
| id | int unsigned | NO | PRI |
| funcionario_id | int unsigned | NO | MUL |
| comissao_tipo_id | int unsigned | NO | MUL |
| ativo | tinyint(1) | NO |  |
| created_at | timestamp | YES |  |
| updated_at | timestamp | YES |  |
| deleted_at | timestamp | YES |  |

## 3. Mapeamento origem → Faceta (confirmado no live)

| conceito Faceta | tabela MySQL | colunas-chave | obs |
| --- | --- | --- | --- |
| departamento | departamentos | id, nome | — |
| concessionaria | concessionarias | id, nome | extras ignorados na ingestão |
| familia_servico | **subgrupos_servicos** | id, nome | via servicos.**subgrupo_servico_id** (corrigido pós-Fase 1) |
| familia_produto | subgrupos_produtos | id, nome | espelho produtos |
| vendedor | funcionarios | id, nome | os.vendedor_id; tipo via funcionario_tipos |
| produtivo | funcionarios | id, nome | os_servicos.produtivo_id; tipo via funcionario_tipos |
| funcionario_tipos | funcionario_tipos | id, nome | cadeia funcionario_cargos → cargos.funcionario_tipo_id |
| forma_pagamento | caixa_tipos | id, nome | via caixas.caixa_tipo_id |
| empresa | empresas | id, nome | — |
| servico | servicos | id, nome, subgrupo_servico_id | dimensão unitária |
| fato_os | os | flags + FKs + valores | grão cabeçalho |
| fato_os_servico | os_servicos | os_id, **servico_id**, produtivo_id, valores | + familia = subgrupo |
| fato_os_pagamento | caixas | os_id, valor, caixa_tipo_id | caixas_pendentes ≠ prova de paga |
| fato_comissao | comissoes | **comissionado_id**, **comissao_tipo_id**, valores | satélites comissao_* |

## 4. Amostras de dimensões e tipos

### `departamentos`

| id | nome |
| --- | --- |
| 1 | Veículos Novos |
| 2 | Veículos Usados |
| 3 | Oficina |
| 4 | Frotista |
| 5 | Lanternagem |
| 6 | Venda Direta Interna |
| 7 | Venda Direta Externa |
| 8 | PPF |
| 9 | ESTÉTICA |

### `concessionarias`

| id | nome |
| --- | --- |
| 1 | AUDI CARBEL |
| 2 | AUDI CENTER PAMPULHA |
| 3 | BANZAI |
| 4 | BANZAI PAMPULHA |
| 5 | BORDEAUX |
| 6 | BRASERV LOCADORA DE VEICULOS L |
| 7 | CARBEL |
| 8 | CARBEL JAPÃO BARÃO |
| 9 | CARBEL JAPÃO PAMPULHA |
| 10 | CARBEL KOREA |

### `grupos_servicos`

| id | nome |
| --- | --- |
| 1 | Serviços |
| 2 | Pequenos Serviços |
| 3 | Banco em Couro |
| 4 | OUTROS |
| 5 | DETALHAMENTO |
| 6 | Customização |

### `caixa_tipos`

| id | nome |
| --- | --- |
| 1 | Dinheiro |
| 2 | Depósito Bancário |
| 3 | Cartão de Crédito |
| 4 | Cheque |
| 5 | Concessionária |
| 6 | Cartão de Débito |
| 7 | PIX |
| 8 | Permuta |
| 9 | Parcelamento |

### `empresas`

| id | nome |
| --- | --- |
| 1 | CARSOUL |
| 2 | BH ESTÉTICA |
| 3 | GB ESTÉTICA |
| 4 | GB ESTÉTICA FILIAL - JF |
| 5 | XTREME PPF |
| 6 | GB FILIAL |
| 7 | MFP ESTETICA AUTOMOTIVA |

### `funcionario_tipos`

| id | nome |
| --- | --- |
| 1 | Vendas |
| 2 | Supervisores |
| 3 | Administrativo |
| 4 | Estoque/Entrega |
| 5 | Produtivos |
| 6 | Prestadores de Serviço |
| 7 | Freelancers |
| 8 | Supervisores - Vendas |

### `comissao_tipos`

| id | nome |
| --- | --- |
| 1 | CONCESSIONÁRIA |
| 2 | VENDEDOR |
| 3 | PRODUTIVO |
| 4 | INDICADOR1 |
| 5 | INDICADOR2 |

### Cadeia funcionario_tipos → cargos → funcionario_cargos

| funcionario_tipo_id | nome | funcionarios_distintos |
| --- | --- | --- |
| 1 | Vendas | 184 |
| 2 | Supervisores | 7 |
| 3 | Administrativo | 67 |
| 4 | Estoque/Entrega | 9 |
| 5 | Produtivos | 219 |
| 6 | Prestadores de Serviço | 3 |
| 7 | Freelancers | 35 |
| 8 | Supervisores - Vendas | 0 |

## 5. Estados da OS (últimos 14 dias)

Critérios de negócio (Faceta — **não** usar `os.finalizada` como paga∩fechada):
- **Abertas:** `DATE(created_at)`
- **Pagas:** `os.paga = 1` **e** ≥1 linha em `caixas` (`caixas_pendentes` não conta)
- **Fechadas (derivadas):** itens ativos (`cancelado <> 1`) todos com `fechado = 1` em `os_servicos` **ou** (exclusivo) `os_produtos`
- **Canceladas:** `os.cancelada = 1`
- **Paga sem caixa (inconsistência, não cancelada):** `os.paga = 1` **e** zero `caixas`

| dia | abertas | pagas | fechadas_deriv | canceladas | paga_sem_caixa |
| --- | --- | --- | --- | --- | --- |
| 2026-07-26 | 0 | 1 | 1 | 0 | 0 |
| 2026-07-27 | 124 | 102 | 104 | 0 | 8 |
| 2026-07-28 | 165 | 67 | 142 | 5 | 41 |
| 2026-07-29 | 104 | 52 | 134 | 7 | 5 |
| 2026-07-30 | 124 | 66 | 120 | 4 | 6 |
| 2026-07-31 | 162 | 73 | 228 | 3 | 58 |
| 2026-08-01 | 4 | 3 | 1 | 0 | 0 |

### Checagens vs flags / inconsistências

| checagem | contagem |
| --- | --- |
| divergência os.fechada ↔ fechada derivada | 21 |
| paga=1 sem caixas (inconsistência) | 118 |
| … dessas com os.fechada=1 | 107 |
| … dessas com os.cancelada=1 | 0 |
| itens ativos em os_servicos E os_produtos | 0 |

## 6. Comissão — schema, momento e fórmula

### Regras de negócio

- Comissão **geral** gerada no **pagamento** → OS fechada sem comissão é esperado.
- **Exceção produtivo:** comissão gerada ao **fechar serviços/itens**.
- Ingestão de `fato_comissao` lê `comissoes` materializadas; não assume 1:1 com fechada derivada.

**OS fechadas (derivadas) sem comissão ligada (últimos 14 dias):** `35` (esperado pela regra de pagamento).

### Comissões recentes por tipo de funcionário × tipo de comissão

| beneficiario_tipo | tipo_comissao | qtd | valor_total |
| --- | --- | --- | --- |
| Vendas | VENDEDOR | 1357 | 82635.33 |
| Produtivos | PRODUTIVO | 1224 | 34254 |
| (sem tipo / cargo) | INDICADOR1 | 614 | 20216.5 |
| (sem tipo / cargo) | CONCESSIONÁRIA | 494 | 118288.53 |
| (sem tipo / cargo) | INDICADOR2 | 385 | 5195.5 |
| Freelancers | PRODUTIVO | 39 | 1800 |
| Administrativo | VENDEDOR | 22 | 1728.5 |
| (sem tipo / cargo) | PRODUTIVO | 8 | 34000 |
| (sem tipo / cargo) | VENDEDOR | 6 | 161.2 |

### Componentes de valor em `comissoes`

| coluna | nulos | não-zero | total_periodo |
| --- | --- | --- | --- |
| valor_dentro | 0 | 2818 | 4149 |
| valor_fora | 0 | 3639 | 4149 |
| valor_combo | 3446 | 687 | 4149 |
| valor_compensado_permuta | 0 | 6 | 4149 |
| comissao_couro | 0 | 0 | 4149 |

### Fórmula fixada para `fato_comissao.valor_comissao`

`valor_comissao = COALESCE(valor_dentro,0) + COALESCE(valor_fora,0) + COALESCE(valor_combo,0) + COALESCE(valor_compensado_permuta,0) + COALESCE(comissao_couro,0)`

- `comissionado_id` ← `comissoes.comissionado_id`
- `comissao_tipo_id` ← `comissoes.comissao_tipo_id` (sempre na origem; **não** derivar de `funcionario_tipos`/cargo — concessionária/indicador não têm cargo)
- Nome do tipo: join `dim_comissao_tipo` / `comissao_tipos`
- Data sugerida do fato: `DATE(comissoes.created_at)` (geração no pagamento ou no fechamento do serviço do produtivo)

## 7. Frequência de leitura (recomendação)

Não há um único “dia fechado” global. A ingestão diária deve filtrar por **recorte**:

| Recorte / família | Quando ler o dia D | Filtro |
|---|---|---|
| Abertas / `fato_os` (criação) | D+1 | `DATE(os.created_at) = D` |
| Pagas / pagamentos | D+1 | `os.paga = 1` + existe `caixas`, `DATE(data_pagamento) = D` |
| Fechadas / itens | D+1 | fechada derivada (itens ativos todos `fechado`); preferir não confiar só em `os.fechada` |
| Canceladas | D+1 | `os.cancelada = 1`, `DATE(data_cancelamento) = D` |
| Paga sem caixa | D+1 | inconsistência de origem (`paga=1` sem `caixas`); não ingerir como cancelada |
| Comissão (geral) | D+1 após pagamentos | `comissoes` do dia; aceitar OS fechada sem comissão |
| Comissão (produtivo) | D+1 após fechamento de itens | pode existir antes do pagamento |

Cadência sugerida: **um job diário após 00:30** processando o dia D−1 para todos os recortes, sem bloquear comissão na ausência de pagamento.

## 8. Achados / riscos

- Divergência `os.fechada` vs fechada derivada: 21 OS (últimos 14 dias).

- Inconsistência `paga=1` sem `caixas`: 118 OS (107 com `os.fechada=1`, 0 com `os.cancelada=1`) — não tratar como cancelada.
