SELECT `acesso_regra_grupos`.`id`,
    `acesso_regra_grupos`.`acesso_regra_id`,
    `acesso_regra_grupos`.`grupo_usuario_id`,
    `acesso_regra_grupos`.`created_at`,
    `acesso_regra_grupos`.`updated_at`,
    `acesso_regra_grupos`.`deleted_at`
FROM `smart`.`acesso_regra_grupos`;

SELECT `acesso_regras`.`id`,
    `acesso_regras`.`seg_inicio`,
    `acesso_regras`.`seg_fim`,
    `acesso_regras`.`ter_inicio`,
    `acesso_regras`.`ter_fim`,
    `acesso_regras`.`qua_inicio`,
    `acesso_regras`.`qua_fim`,
    `acesso_regras`.`qui_inicio`,
    `acesso_regras`.`qui_fim`,
    `acesso_regras`.`sex_inicio`,
    `acesso_regras`.`sex_fim`,
    `acesso_regras`.`sab_inicio`,
    `acesso_regras`.`sab_fim`,
    `acesso_regras`.`dom_inicio`,
    `acesso_regras`.`dom_fim`,
    `acesso_regras`.`funcionario_registro_id`,
    `acesso_regras`.`created_at`,
    `acesso_regras`.`updated_at`,
    `acesso_regras`.`deleted_at`
FROM `smart`.`acesso_regras`;

SELECT `achivement_funcionario`.`id`,
    `achivement_funcionario`.`funcionario_id`,
    `achivement_funcionario`.`achivement_id`,
    `achivement_funcionario`.`rating`,
    `achivement_funcionario`.`created_at`,
    `achivement_funcionario`.`updated_at`
FROM `smart`.`achivement_funcionario`;

SELECT `achivement_funcionario_historico`.`id`,
    `achivement_funcionario_historico`.`funcionario_id`,
    `achivement_funcionario_historico`.`achivement_id`,
    `achivement_funcionario_historico`.`rating_anterior`,
    `achivement_funcionario_historico`.`rating_novo`,
    `achivement_funcionario_historico`.`motivo`,
    `achivement_funcionario_historico`.`user_update`,
    `achivement_funcionario_historico`.`created_at`,
    `achivement_funcionario_historico`.`updated_at`
FROM `smart`.`achivement_funcionario_historico`;

SELECT `achivements`.`id`,
    `achivements`.`nome`,
    `achivements`.`descricao`,
    `achivements`.`icone`,
    `achivements`.`nota_minima`,
    `achivements`.`ativo`,
    `achivements`.`created_at`,
    `achivements`.`updated_at`,
    `achivements`.`deleted_at`
FROM `smart`.`achivements`;

SELECT `anuncios_app`.`id`,
    `anuncios_app`.`url`,
    `anuncios_app`.`descricao`,
    `anuncios_app`.`ordem`,
    `anuncios_app`.`ativo`,
    `anuncios_app`.`data_inicio`,
    `anuncios_app`.`data_expiracao`,
    `anuncios_app`.`created_at`,
    `anuncios_app`.`updated_at`
FROM `smart`.`anuncios_app`;

SELECT `avaliacao_qualidade_questao_subgrupos`.`id`,
    `avaliacao_qualidade_questao_subgrupos`.`avaliacao_qualidade_questao_id`,
    `avaliacao_qualidade_questao_subgrupos`.`subgrupo_servico_id`,
    `avaliacao_qualidade_questao_subgrupos`.`created_at`,
    `avaliacao_qualidade_questao_subgrupos`.`updated_at`,
    `avaliacao_qualidade_questao_subgrupos`.`deleted_at`
FROM `smart`.`avaliacao_qualidade_questao_subgrupos`;

SELECT `avaliacao_qualidade_questoes`.`id`,
    `avaliacao_qualidade_questoes`.`descricao`,
    `avaliacao_qualidade_questoes`.`resposta_positiva`,
    `avaliacao_qualidade_questoes`.`ordem`,
    `avaliacao_qualidade_questoes`.`por_subgrupo_servico`,
    `avaliacao_qualidade_questoes`.`created_at`,
    `avaliacao_qualidade_questoes`.`updated_at`,
    `avaliacao_qualidade_questoes`.`deleted_at`
FROM `smart`.`avaliacao_qualidade_questoes`;

SELECT `avaliacao_qualidade_respostas`.`id`,
    `avaliacao_qualidade_respostas`.`resposta`,
    `avaliacao_qualidade_respostas`.`observacao`,
    `avaliacao_qualidade_respostas`.`avaliacao_qualidade_id`,
    `avaliacao_qualidade_respostas`.`avaliacao_qualidade_questao_id`,
    `avaliacao_qualidade_respostas`.`avaliacao_qualidade_servico_id`,
    `avaliacao_qualidade_respostas`.`created_at`,
    `avaliacao_qualidade_respostas`.`updated_at`,
    `avaliacao_qualidade_respostas`.`deleted_at`
FROM `smart`.`avaliacao_qualidade_respostas`;

SELECT `avaliacao_qualidade_servicos`.`id`,
    `avaliacao_qualidade_servicos`.`data_inicio`,
    `avaliacao_qualidade_servicos`.`data_fim`,
    `avaliacao_qualidade_servicos`.`observacao`,
    `avaliacao_qualidade_servicos`.`produtivo_id`,
    `avaliacao_qualidade_servicos`.`os_servico_id`,
    `avaliacao_qualidade_servicos`.`avaliacao_qualidade_id`,
    `avaliacao_qualidade_servicos`.`created_at`,
    `avaliacao_qualidade_servicos`.`updated_at`,
    `avaliacao_qualidade_servicos`.`deleted_at`
FROM `smart`.`avaliacao_qualidade_servicos`;

SELECT `avaliacoes_qualidade`.`id`,
    `avaliacoes_qualidade`.`data_entrega_agendamento`,
    `avaliacoes_qualidade`.`data_entrega_concessionaria`,
    `avaliacoes_qualidade`.`data_entrega_real`,
    `avaliacoes_qualidade`.`observacao`,
    `avaliacoes_qualidade`.`os_id`,
    `avaliacoes_qualidade`.`concessionaria_id`,
    `avaliacoes_qualidade`.`vendedor_id`,
    `avaliacoes_qualidade`.`departamento_id`,
    `avaliacoes_qualidade`.`carro_modelo_id`,
    `avaliacoes_qualidade`.`carro_cor_id`,
    `avaliacoes_qualidade`.`funcionario_cadastro_id`,
    `avaliacoes_qualidade`.`created_at`,
    `avaliacoes_qualidade`.`updated_at`,
    `avaliacoes_qualidade`.`deleted_at`
FROM `smart`.`avaliacoes_qualidade`;

SELECT `banco_conta_tipos`.`id`,
    `banco_conta_tipos`.`nome`,
    `banco_conta_tipos`.`ativo`,
    `banco_conta_tipos`.`created_at`,
    `banco_conta_tipos`.`updated_at`,
    `banco_conta_tipos`.`deleted_at`
FROM `smart`.`banco_conta_tipos`;

SELECT `bancos`.`id`,
    `bancos`.`nome`,
    `bancos`.`ativo`,
    `bancos`.`created_at`,
    `bancos`.`updated_at`,
    `bancos`.`deleted_at`
FROM `smart`.`bancos`;

SELECT `base_concessionarias`.`id`,
    `base_concessionarias`.`concessionaria_id`,
    `base_concessionarias`.`produtivo_base_id`,
    `base_concessionarias`.`ativo`,
    `base_concessionarias`.`created_at`,
    `base_concessionarias`.`updated_at`,
    `base_concessionarias`.`deleted_at`
FROM `smart`.`base_concessionarias`;

SELECT `base_produtivos`.`id`,
    `base_produtivos`.`funcionario_id`,
    `base_produtivos`.`produtivo_base_id`,
    `base_produtivos`.`ativo`,
    `base_produtivos`.`created_at`,
    `base_produtivos`.`updated_at`,
    `base_produtivos`.`deleted_at`
FROM `smart`.`base_produtivos`;

SELECT `boleto_remessas`.`id`,
    `boleto_remessas`.`created_at`,
    `boleto_remessas`.`updated_at`,
    `boleto_remessas`.`deleted_at`
FROM `smart`.`boleto_remessas`;

SELECT `business_units`.`id`,
    `business_units`.`nome`,
    `business_units`.`sigla`,
    `business_units`.`ativo`,
    `business_units`.`created_at`,
    `business_units`.`updated_at`,
    `business_units`.`deleted_at`
FROM `smart`.`business_units`;

SELECT `caixa_antecipacoes`.`id`,
    `caixa_antecipacoes`.`origem`,
    `caixa_antecipacoes`.`data_inicio`,
    `caixa_antecipacoes`.`data_fim`,
    `caixa_antecipacoes`.`valor_pagamento_bruto`,
    `caixa_antecipacoes`.`valor_pagamento_taxa`,
    `caixa_antecipacoes`.`valor_pagamento_liquido`,
    `caixa_antecipacoes`.`valor_mdr_bruto`,
    `caixa_antecipacoes`.`valor_mdr_taxa`,
    `caixa_antecipacoes`.`valor_mdr_liquido`,
    `caixa_antecipacoes`.`porcentagem_mdr_taxa`,
    `caixa_antecipacoes`.`taxa_antecipacao`,
    `caixa_antecipacoes`.`taxa_antecipacao_real`,
    `caixa_antecipacoes`.`valor_taxa`,
    `caixa_antecipacoes`.`valor_liquido`,
    `caixa_antecipacoes`.`valor_liquido_banco`,
    `caixa_antecipacoes`.`valor_antecipacao_banco`,
    `caixa_antecipacoes`.`taxa_banco_real`,
    `caixa_antecipacoes`.`valor_pagamento_banco`,
    `caixa_antecipacoes`.`valor_diferenca`,
    `caixa_antecipacoes`.`funcionario_registro_id`,
    `caixa_antecipacoes`.`empresa_id`,
    `caixa_antecipacoes`.`created_at`,
    `caixa_antecipacoes`.`updated_at`,
    `caixa_antecipacoes`.`deleted_at`
FROM `smart`.`caixa_antecipacoes`;

SELECT `caixa_concessionaria_documentos`.`id`,
    `caixa_concessionaria_documentos`.`documento_assinado_id`,
    `caixa_concessionaria_documentos`.`caixa_fechamento_id`,
    `caixa_concessionaria_documentos`.`concessionaria_email_id`,
    `caixa_concessionaria_documentos`.`created_at`,
    `caixa_concessionaria_documentos`.`updated_at`,
    `caixa_concessionaria_documentos`.`deleted_at`
FROM `smart`.`caixa_concessionaria_documentos`;

SELECT `caixa_contas`.`id`,
    `caixa_contas`.`numero`,
    `caixa_contas`.`agencia`,
    `caixa_contas`.`nome`,
    `caixa_contas`.`empresa_id`,
    `caixa_contas`.`ativo`,
    `caixa_contas`.`created_at`,
    `caixa_contas`.`updated_at`,
    `caixa_contas`.`deleted_at`
FROM `smart`.`caixa_contas`;

SELECT `caixa_fechamentos`.`id`,
    `caixa_fechamentos`.`controle_concessionaria`,
    `caixa_fechamentos`.`finalizado`,
    `caixa_fechamentos`.`data_finalizacao`,
    `caixa_fechamentos`.`valor`,
    `caixa_fechamentos`.`caixa_concessionaria`,
    `caixa_fechamentos`.`concessionaria_id`,
    `caixa_fechamentos`.`vendedor_id`,
    `caixa_fechamentos`.`malote_id`,
    `caixa_fechamentos`.`created_at`,
    `caixa_fechamentos`.`updated_at`,
    `caixa_fechamentos`.`deleted_at`
FROM `smart`.`caixa_fechamentos`;

SELECT `caixas`.`id`,
    `caixas`.`valor`,
    `caixas`.`desconto`,
    `caixas`.`data_vencimento`,
    `caixas`.`data_pagamento`,
    `caixas`.`cancelado`,
    `caixas`.`data_cancelamento`,
    `caixas`.`fechado`,
    `caixas`.`data_fechamento`,
    `caixas`.`classificado`,
    `caixas`.`data_classificacao`,
    `caixas`.`finalizado`,
    `caixas`.`verificado`,
    `caixas`.`data_verificacao`,
    `caixas`.`data_finalizacao`,
    `caixas`.`parcela`,
    `caixas`.`quant_parcelas`,
    `caixas`.`nome_depositante`,
    `caixas`.`codigo_transacao`,
    `caixas`.`nome_titular`,
    `caixas`.`doc_titular`,
    `caixas`.`telefone_titular`,
    `caixas`.`tid_cielo`,
    `caixas`.`taxa_cartao`,
    `caixas`.`taxa_antecipacao`,
    `caixas`.`bandeira_cartao`,
    `caixas`.`codigo_autorizacao`,
    `caixas`.`numero_autorizacao`,
    `caixas`.`nome_cartao`,
    `caixas`.`cc_conciliado`,
    `caixas`.`pix_payload`,
    `caixas`.`pix_info_pagador`,
    `caixas`.`pix_e2ed_id`,
    `caixas`.`pix_rtr_id`,
    `caixas`.`observacao_financeiro`,
    `caixas`.`caixa_preto`,
    `caixas`.`usuario_pagamento_id`,
    `caixas`.`usuario_verificacao_id`,
    `caixas`.`caixa_conta_id`,
    `caixas`.`caixa_tipo_id`,
    `caixas`.`caixa_pendente_id`,
    `caixas`.`caixa_status_id`,
    `caixas`.`caixa_fechamento_id`,
    `caixas`.`caixa_antecipacao_id`,
    `caixas`.`caixa_original_id`,
    `caixas`.`empresa_faturamento_id`,
    `caixas`.`financeiro_malote_classificacao_id`,
    `caixas`.`financeiro_caixa_destino_id`,
    `caixas`.`os_id`,
    `caixas`.`mc_conciliacao_lancamento_id`,
    `caixas`.`ativo`,
    `caixas`.`created_at`,
    `caixas`.`updated_at`,
    `caixas`.`deleted_at`
FROM `smart`.`caixas`;

SELECT `caixas_pendentes`.`id`,
    `caixas_pendentes`.`valor`,
    `caixas_pendentes`.`desconto`,
    `caixas_pendentes`.`codigo_transacao`,
    `caixas_pendentes`.`data_vencimento`,
    `caixas_pendentes`.`parcela`,
    `caixas_pendentes`.`quant_parcelas`,
    `caixas_pendentes`.`expiracao`,
    `caixas_pendentes`.`pix_tx_id`,
    `caixas_pendentes`.`pix_payload`,
    `caixas_pendentes`.`pix_tentativas`,
    `caixas_pendentes`.`pix_br_code`,
    `caixas_pendentes`.`pix_info_pagador`,
    `caixas_pendentes`.`pix_e2ed_id`,
    `caixas_pendentes`.`pix_rtr_id`,
    `caixas_pendentes`.`data_criacao_cobranca`,
    `caixas_pendentes`.`data_expiracao_cobranca`,
    `caixas_pendentes`.`fechado`,
    `caixas_pendentes`.`data_fechamento`,
    `caixas_pendentes`.`finalizado`,
    `caixas_pendentes`.`data_finalizacao`,
    `caixas_pendentes`.`cancelado`,
    `caixas_pendentes`.`data_cancelamento`,
    `caixas_pendentes`.`caixa_tipo_id`,
    `caixas_pendentes`.`caixa_status_id`,
    `caixas_pendentes`.`caixa_fechamento_id`,
    `caixas_pendentes`.`os_id`,
    `caixas_pendentes`.`empresa_id`,
    `caixas_pendentes`.`remessa_os_id`,
    `caixas_pendentes`.`tipo_remessa_id`,
    `caixas_pendentes`.`usuario_pagamento_id`,
    `caixas_pendentes`.`created_at`,
    `caixas_pendentes`.`updated_at`,
    `caixas_pendentes`.`deleted_at`
FROM `smart`.`caixas_pendentes`;

SELECT `caixa_status`.`id`,
    `caixa_status`.`nome`,
    `caixa_status`.`ativo`,
    `caixa_status`.`created_at`,
    `caixa_status`.`updated_at`,
    `caixa_status`.`deleted_at`
FROM `smart`.`caixa_status`;

SELECT `caixa_tipos`.`id`,
    `caixa_tipos`.`nome`,
    `caixa_tipos`.`ativo`,
    `caixa_tipos`.`created_at`,
    `caixa_tipos`.`updated_at`,
    `caixa_tipos`.`deleted_at`
FROM `smart`.`caixa_tipos`;

SELECT `cancelamento_motivos`.`id`,
    `cancelamento_motivos`.`nome`,
    `cancelamento_motivos`.`created_at`,
    `cancelamento_motivos`.`updated_at`,
    `cancelamento_motivos`.`deleted_at`
FROM `smart`.`cancelamento_motivos`;

SELECT `cargo_epi`.`id`,
    `cargo_epi`.`cargo_id`,
    `cargo_epi`.`epi_id`,
    `cargo_epi`.`created_at`,
    `cargo_epi`.`updated_at`,
    `cargo_epi`.`deleted_at`
FROM `smart`.`cargo_epi`;

SELECT `cargos`.`id`,
    `cargos`.`cbo`,
    `cargos`.`nome`,
    `cargos`.`descricao`,
    `cargos`.`salario_base`,
    `cargos`.`ativo`,
    `cargos`.`funcionario_tipo_id`,
    `cargos`.`created_at`,
    `cargos`.`updated_at`,
    `cargos`.`deleted_at`
FROM `smart`.`cargos`;

SELECT `carro_cores`.`id`,
    `carro_cores`.`nome`,
    `carro_cores`.`carro_cor_tipo_id`,
    `carro_cores`.`ativo`,
    `carro_cores`.`created_at`,
    `carro_cores`.`updated_at`,
    `carro_cores`.`deleted_at`
FROM `smart`.`carro_cores`;

SELECT `carro_cor_tipos`.`id`,
    `carro_cor_tipos`.`nome`,
    `carro_cor_tipos`.`ativo`,
    `carro_cor_tipos`.`created_at`,
    `carro_cor_tipos`.`updated_at`,
    `carro_cor_tipos`.`deleted_at`
FROM `smart`.`carro_cor_tipos`;

SELECT `carro_marcas`.`id`,
    `carro_marcas`.`nome`,
    `carro_marcas`.`ativo`,
    `carro_marcas`.`created_at`,
    `carro_marcas`.`updated_at`,
    `carro_marcas`.`deleted_at`
FROM `smart`.`carro_marcas`;

SELECT `carro_modelo_comissao_portes`.`id`,
    `carro_modelo_comissao_portes`.`carro_modelo_id`,
    `carro_modelo_comissao_portes`.`servico_id`,
    `carro_modelo_comissao_portes`.`carro_porte_id`,
    `carro_modelo_comissao_portes`.`ativo`,
    `carro_modelo_comissao_portes`.`created_at`,
    `carro_modelo_comissao_portes`.`updated_at`,
    `carro_modelo_comissao_portes`.`deleted_at`
FROM `smart`.`carro_modelo_comissao_portes`;

SELECT `carro_modelos`.`id`,
    `carro_modelos`.`nome`,
    `carro_modelos`.`carro_marca_id`,
    `carro_modelos`.`ativo`,
    `carro_modelos`.`created_at`,
    `carro_modelos`.`updated_at`,
    `carro_modelos`.`deleted_at`
FROM `smart`.`carro_modelos`;

SELECT `carro_modelo_servico_portes`.`id`,
    `carro_modelo_servico_portes`.`carro_modelo_id`,
    `carro_modelo_servico_portes`.`servico_id`,
    `carro_modelo_servico_portes`.`carro_porte_id`,
    `carro_modelo_servico_portes`.`ativo`,
    `carro_modelo_servico_portes`.`created_at`,
    `carro_modelo_servico_portes`.`updated_at`,
    `carro_modelo_servico_portes`.`deleted_at`
FROM `smart`.`carro_modelo_servico_portes`;

SELECT `carro_portes`.`id`,
    `carro_portes`.`nome`,
    `carro_portes`.`ativo`,
    `carro_portes`.`created_at`,
    `carro_portes`.`updated_at`,
    `carro_portes`.`deleted_at`
FROM `smart`.`carro_portes`;

SELECT `carro_submodelos`.`id`,
    `carro_submodelos`.`nome`,
    `carro_submodelos`.`ativo`,
    `carro_submodelos`.`created_at`,
    `carro_submodelos`.`updated_at`,
    `carro_submodelos`.`deleted_at`
FROM `smart`.`carro_submodelos`;

SELECT `cartas_correcao`.`id`,
    `cartas_correcao`.`nota_fiscal_id`,
    `cartas_correcao`.`chave_nfe`,
    `cartas_correcao`.`status`,
    `cartas_correcao`.`campos_correcao`,
    `cartas_correcao`.`retorna_xml`,
    `cartas_correcao`.`token`,
    `cartas_correcao`.`resultado`,
    `cartas_correcao`.`mensagem`,
    `cartas_correcao`.`xml_cce`,
    `cartas_correcao`.`pedido_enviado_em`,
    `cartas_correcao`.`resposta_recebida_em`,
    `cartas_correcao`.`created_at`,
    `cartas_correcao`.`updated_at`,
    `cartas_correcao`.`deleted_at`
FROM `smart`.`cartas_correcao`;

SELECT `cielo_respostas`.`id`,
    `cielo_respostas`.`estorno`,
    `cielo_respostas`.`return_code`,
    `cielo_respostas`.`return_message`,
    `cielo_respostas`.`payment_id`,
    `cielo_respostas`.`tid`,
    `cielo_respostas`.`response_path`,
    `cielo_respostas`.`os_id`,
    `cielo_respostas`.`funcionario_id`,
    `cielo_respostas`.`created_at`,
    `cielo_respostas`.`updated_at`,
    `cielo_respostas`.`deleted_at`
FROM `smart`.`cielo_respostas`;

SELECT `cliente_carros`.`id`,
    `cliente_carros`.`chassi`,
    `cliente_carros`.`placa`,
    `cliente_carros`.`ano_modelo`,
    `cliente_carros`.`ano`,
    `cliente_carros`.`cadastro_parcial`,
    `cliente_carros`.`cliente_id`,
    `cliente_carros`.`carro_cor_id`,
    `cliente_carros`.`carro_modelo_id`,
    `cliente_carros`.`carro_submodelo_id`,
    `cliente_carros`.`ativo`,
    `cliente_carros`.`created_at`,
    `cliente_carros`.`updated_at`,
    `cliente_carros`.`deleted_at`
FROM `smart`.`cliente_carros`;

SELECT `clientes`.`id`,
    `clientes`.`pf`,
    `clientes`.`nome`,
    `clientes`.`cpf`,
    `clientes`.`sexo`,
    `clientes`.`data_nascimento`,
    `clientes`.`estado_civil`,
    `clientes`.`ie`,
    `clientes`.`ie_verificada`,
    `clientes`.`im`,
    `clientes`.`retem_iss`,
    `clientes`.`cep`,
    `clientes`.`logradouro`,
    `clientes`.`bairro`,
    `clientes`.`localidade`,
    `clientes`.`uf`,
    `clientes`.`codigo_ibge`,
    `clientes`.`numero`,
    `clientes`.`complemento`,
    `clientes`.`telefone1`,
    `clientes`.`telefone2`,
    `clientes`.`email`,
    `clientes`.`bloqueado_serasa`,
    `clientes`.`observacao_serasa`,
    `clientes`.`crmbonus_customer_id`,
    `clientes`.`crmbonus_pin_code`,
    `clientes`.`crmbonus_validado`,
    `clientes`.`crmbonus_data_cadastro`,
    `clientes`.`crmbonus_verificado`,
    `clientes`.`ativo`,
    `clientes`.`created_at`,
    `clientes`.`updated_at`,
    `clientes`.`deleted_at`
FROM `smart`.`clientes`;

SELECT `clusters`.`id`,
    `clusters`.`nome`,
    `clusters`.`valor`,
    `clusters`.`rmf`,
    `clusters`.`pmr`,
    `clusters`.`valor_tipo`,
    `clusters`.`ativo`,
    `clusters`.`created_at`,
    `clusters`.`updated_at`,
    `clusters`.`deleted_at`
FROM `smart`.`clusters`;

SELECT `combo_concessionarias`.`id`,
    `combo_concessionarias`.`combo_id`,
    `combo_concessionarias`.`concessionaria_id`,
    `combo_concessionarias`.`ativo`,
    `combo_concessionarias`.`created_at`,
    `combo_concessionarias`.`updated_at`,
    `combo_concessionarias`.`deleted_at`
FROM `smart`.`combo_concessionarias`;

SELECT `combos`.`id`,
    `combos`.`nome`,
    `combos`.`adicional_dentro`,
    `combos`.`adicional_fora`,
    `combos`.`porcentagem`,
    `combos`.`ativo`,
    `combos`.`data_inicial`,
    `combos`.`data_final`,
    `combos`.`created_at`,
    `combos`.`updated_at`,
    `combos`.`deleted_at`
FROM `smart`.`combos`;

SELECT `combo_servicos`.`id`,
    `combo_servicos`.`valor_venda`,
    `combo_servicos`.`valor_nfe`,
    `combo_servicos`.`combo_id`,
    `combo_servicos`.`servico_id`,
    `combo_servicos`.`carro_porte_id`,
    `combo_servicos`.`ativo`,
    `combo_servicos`.`created_at`,
    `combo_servicos`.`updated_at`,
    `combo_servicos`.`deleted_at`
FROM `smart`.`combo_servicos`;

SELECT `combo_servico_substitutos`.`id`,
    `combo_servico_substitutos`.`combo_servico_id`,
    `combo_servico_substitutos`.`servico_id`,
    `combo_servico_substitutos`.`created_at`,
    `combo_servico_substitutos`.`updated_at`,
    `combo_servico_substitutos`.`deleted_at`
FROM `smart`.`combo_servico_substitutos`;

SELECT `comissao_pagamentos`.`id`,
    `comissao_pagamentos`.`funcionario_id`,
    `comissao_pagamentos`.`comissao_tipo_id`,
    `comissao_pagamentos`.`ativo`,
    `comissao_pagamentos`.`created_at`,
    `comissao_pagamentos`.`updated_at`,
    `comissao_pagamentos`.`deleted_at`
FROM `smart`.`comissao_pagamentos`;

SELECT `comissao_periodos`.`id`,
    `comissao_periodos`.`nome`,
    `comissao_periodos`.`inicio`,
    `comissao_periodos`.`ativo`,
    `comissao_periodos`.`created_at`,
    `comissao_periodos`.`updated_at`,
    `comissao_periodos`.`deleted_at`
FROM `smart`.`comissao_periodos`;

SELECT `comissao_tipos`.`id`,
    `comissao_tipos`.`nome`,
    `comissao_tipos`.`ativo`,
    `comissao_tipos`.`created_at`,
    `comissao_tipos`.`updated_at`,
    `comissao_tipos`.`deleted_at`
FROM `smart`.`comissao_tipos`;

SELECT `comissoes`.`id`,
    `comissoes`.`valor_dentro`,
    `comissoes`.`valor_fora`,
    `comissoes`.`valor_combo`,
    `comissoes`.`valor_compensado_permuta`,
    `comissoes`.`comissao_couro`,
    `comissoes`.`paga`,
    `comissoes`.`data_pagamento`,
    `comissoes`.`estorno`,
    `comissoes`.`observacao_estorno`,
    `comissoes`.`comissionado_id`,
    `comissoes`.`os_servico_id`,
    `comissoes`.`os_produto_id`,
    `comissoes`.`comissao_tipo_id`,
    `comissoes`.`comissao_pagamento_id`,
    `comissoes`.`comissao_periodo_id`,
    `comissoes`.`ativo`,
    `comissoes`.`created_at`,
    `comissoes`.`updated_at`,
    `comissoes`.`deleted_at`,
    `comissoes`.`comissao_estorno_id`,
    `comissoes`.`nf_entrada_id`,
    `comissoes`.`mc_lancamento_entrada_id`
FROM `smart`.`comissoes`;

SELECT `comunicado_grupos`.`id`,
    `comunicado_grupos`.`notificar_usuarios`,
    `comunicado_grupos`.`comunicado_id`,
    `comunicado_grupos`.`grupo_usuario_id`,
    `comunicado_grupos`.`ativo`,
    `comunicado_grupos`.`created_at`,
    `comunicado_grupos`.`updated_at`,
    `comunicado_grupos`.`deleted_at`
FROM `smart`.`comunicado_grupos`;

SELECT `comunicado_imagens`.`id`,
    `comunicado_imagens`.`ordem`,
    `comunicado_imagens`.`titulo`,
    `comunicado_imagens`.`descricao`,
    `comunicado_imagens`.`url_imagem`,
    `comunicado_imagens`.`comunicado_id`,
    `comunicado_imagens`.`ativo`,
    `comunicado_imagens`.`created_at`,
    `comunicado_imagens`.`updated_at`,
    `comunicado_imagens`.`deleted_at`
FROM `smart`.`comunicado_imagens`;

SELECT `comunicado_notificacoes`.`id`,
    `comunicado_notificacoes`.`visualizado`,
    `comunicado_notificacoes`.`comunicado_id`,
    `comunicado_notificacoes`.`usuario_id`,
    `comunicado_notificacoes`.`created_at`,
    `comunicado_notificacoes`.`updated_at`,
    `comunicado_notificacoes`.`deleted_at`
FROM `smart`.`comunicado_notificacoes`;

SELECT `comunicados`.`id`,
    `comunicados`.`titulo`,
    `comunicados`.`tamanho_janela`,
    `comunicados`.`descricao`,
    `comunicados`.`url_video`,
    `comunicados`.`comunicado_tipo_id`,
    `comunicados`.`ativo`,
    `comunicados`.`created_at`,
    `comunicados`.`updated_at`,
    `comunicados`.`deleted_at`
FROM `smart`.`comunicados`;

SELECT `comunicado_tipos`.`id`,
    `comunicado_tipos`.`nome`,
    `comunicado_tipos`.`ativo`,
    `comunicado_tipos`.`created_at`,
    `comunicado_tipos`.`updated_at`,
    `comunicado_tipos`.`deleted_at`
FROM `smart`.`comunicado_tipos`;

SELECT `concessionaria_boletos`.`id`,
    `concessionaria_boletos`.`concessionaria_id`,
    `concessionaria_boletos`.`created_at`,
    `concessionaria_boletos`.`updated_at`,
    `concessionaria_boletos`.`deleted_at`,
    `concessionaria_boletos`.`email_solicitacao_enviado_em`,
    `concessionaria_boletos`.`email_solicitacao_enviado_por`,
    `concessionaria_boletos`.`email_solicitacao_valores`,
    `concessionaria_boletos`.`pago_banco_em`,
    `concessionaria_boletos`.`boleto_recebido_em`,
    `concessionaria_boletos`.`nf_entrada_id`
FROM `smart`.`concessionaria_boletos`;

SELECT `concessionaria_caixa_tipos`.`id`,
    `concessionaria_caixa_tipos`.`concessionaria_id`,
    `concessionaria_caixa_tipos`.`caixa_tipo_id`,
    `concessionaria_caixa_tipos`.`created_at`,
    `concessionaria_caixa_tipos`.`updated_at`,
    `concessionaria_caixa_tipos`.`deleted_at`
FROM `smart`.`concessionaria_caixa_tipos`;

SELECT `concessionaria_cluster`.`id`,
    `concessionaria_cluster`.`concessionaria_id`,
    `concessionaria_cluster`.`cluster_id`,
    `concessionaria_cluster`.`created_at`,
    `concessionaria_cluster`.`updated_at`,
    `concessionaria_cluster`.`deleted_at`
FROM `smart`.`concessionaria_cluster`;

SELECT `concessionaria_email_categoria_departamentos`.`id`,
    `concessionaria_email_categoria_departamentos`.`concessionaria_email_categoria_id`,
    `concessionaria_email_categoria_departamentos`.`departamento_id`,
    `concessionaria_email_categoria_departamentos`.`created_at`,
    `concessionaria_email_categoria_departamentos`.`updated_at`,
    `concessionaria_email_categoria_departamentos`.`deleted_at`
FROM `smart`.`concessionaria_email_categoria_departamentos`;

SELECT `concessionaria_email_categorias`.`id`,
    `concessionaria_email_categorias`.`concessionaria_email_id`,
    `concessionaria_email_categorias`.`email_categoria_id`,
    `concessionaria_email_categorias`.`concessionaria_id`,
    `concessionaria_email_categorias`.`ativo`,
    `concessionaria_email_categorias`.`created_at`,
    `concessionaria_email_categorias`.`updated_at`,
    `concessionaria_email_categorias`.`deleted_at`
FROM `smart`.`concessionaria_email_categorias`;

SELECT `concessionaria_email_departamentos`.`id`,
    `concessionaria_email_departamentos`.`concessionaria_email_id`,
    `concessionaria_email_departamentos`.`departamento_id`,
    `concessionaria_email_departamentos`.`ativo`,
    `concessionaria_email_departamentos`.`created_at`,
    `concessionaria_email_departamentos`.`updated_at`,
    `concessionaria_email_departamentos`.`deleted_at`
FROM `smart`.`concessionaria_email_departamentos`;

SELECT `concessionaria_emails`.`id`,
    `concessionaria_emails`.`nome`,
    `concessionaria_emails`.`email`,
    `concessionaria_emails`.`observacao`,
    `concessionaria_emails`.`grupo`,
    `concessionaria_emails`.`concessionaria_id`,
    `concessionaria_emails`.`ativo`,
    `concessionaria_emails`.`created_at`,
    `concessionaria_emails`.`updated_at`,
    `concessionaria_emails`.`deleted_at`,
    `concessionaria_emails`.`telefone`,
    `concessionaria_emails`.`cargo`
FROM `smart`.`concessionaria_emails`;

SELECT `concessionaria_indicador_confirmacoes`.`id`,
    `concessionaria_indicador_confirmacoes`.`concessionaria_id`,
    `concessionaria_indicador_confirmacoes`.`funcionario_cadastro_id`,
    `concessionaria_indicador_confirmacoes`.`created_at`,
    `concessionaria_indicador_confirmacoes`.`updated_at`,
    `concessionaria_indicador_confirmacoes`.`deleted_at`
FROM `smart`.`concessionaria_indicador_confirmacoes`;

SELECT `concessionaria_limites_caixas`.`id`,
    `concessionaria_limites_caixas`.`limite_aberto`,
    `concessionaria_limites_caixas`.`limite_fechado`,
    `concessionaria_limites_caixas`.`concessionaria_id`,
    `concessionaria_limites_caixas`.`departamento_id`,
    `concessionaria_limites_caixas`.`ativo`,
    `concessionaria_limites_caixas`.`created_at`,
    `concessionaria_limites_caixas`.`updated_at`,
    `concessionaria_limites_caixas`.`deleted_at`
FROM `smart`.`concessionaria_limites_caixas`;

SELECT `concessionaria_produtivos`.`id`,
    `concessionaria_produtivos`.`concessionaria_id`,
    `concessionaria_produtivos`.`produtivo_tipo_id`,
    `concessionaria_produtivos`.`funcionario_id`,
    `concessionaria_produtivos`.`created_at`,
    `concessionaria_produtivos`.`updated_at`,
    `concessionaria_produtivos`.`deleted_at`
FROM `smart`.`concessionaria_produtivos`;

SELECT `concessionarias`.`id`,
    `concessionarias`.`nome`,
    `concessionarias`.`nome_carbel`,
    `concessionarias`.`razao_social`,
    `concessionarias`.`cnpj`,
    `concessionarias`.`ie`,
    `concessionarias`.`im`,
    `concessionarias`.`cep`,
    `concessionarias`.`logradouro`,
    `concessionarias`.`bairro`,
    `concessionarias`.`localidade`,
    `concessionarias`.`uf`,
    `concessionarias`.`codigo_ibge`,
    `concessionarias`.`numero`,
    `concessionarias`.`complemento`,
    `concessionarias`.`retem_iss`,
    `concessionarias`.`iss_percentual`,
    `concessionarias`.`aceita_indicador1`,
    `concessionarias`.`aceita_indicador2`,
    `concessionarias`.`restringe_requisicao_kit`,
    `concessionarias`.`edita_observacao_nf`,
    `concessionarias`.`permite_deposito_ci`,
    `concessionarias`.`permite_pcp`,
    `concessionarias`.`permite_vendas_materiais`,
    `concessionarias`.`dias_execucao`,
    `concessionarias`.`produtivo_base_id`,
    `concessionarias`.`concessionaria_execucao_id`,
    `concessionarias`.`vendedor_responsavel_nf`,
    `concessionarias`.`cancelamento_automatico`,
    `concessionarias`.`dias_cancelamento_automatico`,
    `concessionarias`.`cancelamento_automatico_proposta`,
    `concessionarias`.`dias_cancelamento_automatico_proposta`,
    `concessionarias`.`integracao_carbel`,
    `concessionarias`.`chassis_nf_cortesia`,
    `concessionarias`.`numero_controle_nf_cortesia`,
    `concessionarias`.`carro_marca_id`,
    `concessionarias`.`comissao_periodo_id`,
    `concessionarias`.`nota_tipo_id`,
    `concessionarias`.`supervisor_vendas_id`,
    `concessionarias`.`cluster_id`,
    `concessionarias`.`business_unit_id`,
    `concessionarias`.`empresa_faturamento_id`,
    `concessionarias`.`email_vendedora`,
    `concessionarias`.`ramal_vendedora`,
    `concessionarias`.`gerente_nome`,
    `concessionarias`.`gerente_email`,
    `concessionarias`.`ativo`,
    `concessionarias`.`created_at`,
    `concessionarias`.`updated_at`,
    `concessionarias`.`deleted_at`,
    `concessionarias`.`bloqueio`,
    `concessionarias`.`region_id`
FROM `smart`.`concessionarias`;

SELECT `concessionaria_tabelas_comissoes`.`id`,
    `concessionaria_tabelas_comissoes`.`concessionaria_id`,
    `concessionaria_tabelas_comissoes`.`tabela_comissao_tipo_id`,
    `concessionaria_tabelas_comissoes`.`tabela_comissao_id`,
    `concessionaria_tabelas_comissoes`.`departamento_id`,
    `concessionaria_tabelas_comissoes`.`created_at`,
    `concessionaria_tabelas_comissoes`.`updated_at`,
    `concessionaria_tabelas_comissoes`.`deleted_at`
FROM `smart`.`concessionaria_tabelas_comissoes`;

SELECT `concessionaria_tabelas_precos`.`id`,
    `concessionaria_tabelas_precos`.`concessionaria_id`,
    `concessionaria_tabelas_precos`.`os_tipo_id`,
    `concessionaria_tabelas_precos`.`tabela_preco_id`,
    `concessionaria_tabelas_precos`.`created_at`,
    `concessionaria_tabelas_precos`.`updated_at`,
    `concessionaria_tabelas_precos`.`deleted_at`
FROM `smart`.`concessionaria_tabelas_precos`;

SELECT `concessionaria_venda_veiculos`.`id`,
    `concessionaria_venda_veiculos`.`periodo`,
    `concessionaria_venda_veiculos`.`quantidade`,
    `concessionaria_venda_veiculos`.`quantidade_concessionaria`,
    `concessionaria_venda_veiculos`.`responsavel`,
    `concessionaria_venda_veiculos`.`concessionaria_id`,
    `concessionaria_venda_veiculos`.`departamento_id`,
    `concessionaria_venda_veiculos`.`funcionario_id`,
    `concessionaria_venda_veiculos`.`funcionario_concessionaria_id`,
    `concessionaria_venda_veiculos`.`created_at`,
    `concessionaria_venda_veiculos`.`updated_at`,
    `concessionaria_venda_veiculos`.`deleted_at`
FROM `smart`.`concessionaria_venda_veiculos`;

SELECT `conciliacao_observacoes`.`id`,
    `conciliacao_observacoes`.`data_venda`,
    `conciliacao_observacoes`.`empresa_id`,
    `conciliacao_observacoes`.`observacao`,
    `conciliacao_observacoes`.`user_id`,
    `conciliacao_observacoes`.`created_at`,
    `conciliacao_observacoes`.`updated_at`,
    `conciliacao_observacoes`.`deleted_at`
FROM `smart`.`conciliacao_observacoes`;

SELECT `conciliacoes_financeira`.`id`,
    `conciliacoes_financeira`.`empresa_id`,
    `conciliacoes_financeira`.`concessionaria_os_id`,
    `conciliacoes_financeira`.`cliente_id`,
    `conciliacoes_financeira`.`caixa_id`,
    `conciliacoes_financeira`.`data_transacao`,
    `conciliacoes_financeira`.`valor_bruto`,
    `conciliacoes_financeira`.`taxa`,
    `conciliacoes_financeira`.`previsao_pagamento`,
    `conciliacoes_financeira`.`valor_liquido`,
    `conciliacoes_financeira`.`quantidade_parcelas`,
    `conciliacoes_financeira`.`transacao_id_externo`,
    `conciliacoes_financeira`.`conciliado_cielo`,
    `conciliacoes_financeira`.`status`,
    `conciliacoes_financeira`.`origem`,
    `conciliacoes_financeira`.`created_at`,
    `conciliacoes_financeira`.`updated_at`,
    `conciliacoes_financeira`.`deleted_at`
FROM `smart`.`conciliacoes_financeira`;

SELECT `cortesia_os`.`id`,
    `cortesia_os`.`os_id`,
    `cortesia_os`.`cortesia_id`,
    `cortesia_os`.`ativo`,
    `cortesia_os`.`created_at`,
    `cortesia_os`.`updated_at`,
    `cortesia_os`.`deleted_at`
FROM `smart`.`cortesia_os`;

SELECT `cortesias`.`id`,
    `cortesias`.`mes_referencia`,
    `cortesias`.`valor_bruto`,
    `cortesias`.`valor_liquido`,
    `cortesias`.`retensao_iss`,
    `cortesias`.`paga`,
    `cortesias`.`data_pagamento`,
    `cortesias`.`valor_pago`,
    `cortesias`.`fechada`,
    `cortesias`.`data_fechamento`,
    `cortesias`.`finalizada`,
    `cortesias`.`data_finalizacao`,
    `cortesias`.`cancelada`,
    `cortesias`.`data_cancelamento`,
    `cortesias`.`solicitado_cancelamento`,
    `cortesias`.`motivo_cancelamento`,
    `cortesias`.`observacao`,
    `cortesias`.`email_enviado`,
    `cortesias`.`data_envio_email`,
    `cortesias`.`pagamento_deposito`,
    `cortesias`.`concessionaria_id`,
    `cortesias`.`departamento_id`,
    `cortesias`.`empresa_id`,
    `cortesias`.`funcionario_cancelamento_id`,
    `cortesias`.`ativo`,
    `cortesias`.`created_at`,
    `cortesias`.`updated_at`,
    `cortesias`.`deleted_at`
FROM `smart`.`cortesias`;

SELECT `crmbonus_lancamentos`.`id`,
    `crmbonus_lancamentos`.`tipo`,
    `crmbonus_lancamentos`.`valor_liquido`,
    `crmbonus_lancamentos`.`valor_bruto`,
    `crmbonus_lancamentos`.`valor_bonus`,
    `crmbonus_lancamentos`.`valor_bonus_utilizacao`,
    `crmbonus_lancamentos`.`data_venda`,
    `crmbonus_lancamentos`.`data_utilizacao`,
    `crmbonus_lancamentos`.`data_inicio_validade`,
    `crmbonus_lancamentos`.`data_fim_validade`,
    `crmbonus_lancamentos`.`vendedor`,
    `crmbonus_lancamentos`.`cliente`,
    `crmbonus_lancamentos`.`telefone`,
    `crmbonus_lancamentos`.`os_id`,
    `crmbonus_lancamentos`.`crmbonus_bonus_id`,
    `crmbonus_lancamentos`.`crmbonus_order_id`,
    `crmbonus_lancamentos`.`crmbonus_customer_id`,
    `crmbonus_lancamentos`.`created_at`,
    `crmbonus_lancamentos`.`updated_at`,
    `crmbonus_lancamentos`.`deleted_at`
FROM `smart`.`crmbonus_lancamentos`;

SELECT `departamentos`.`id`,
    `departamentos`.`nome`,
    `departamentos`.`sigla`,
    `departamentos`.`sigla_carbel`,
    `departamentos`.`ativo`,
    `departamentos`.`created_at`,
    `departamentos`.`updated_at`,
    `departamentos`.`deleted_at`
FROM `smart`.`departamentos`;

SELECT `documento_assinado_mensagens`.`id`,
    `documento_assinado_mensagens`.`message_id`,
    `documento_assinado_mensagens`.`message`,
    `documento_assinado_mensagens`.`profile_name`,
    `documento_assinado_mensagens`.`error_message`,
    `documento_assinado_mensagens`.`direction`,
    `documento_assinado_mensagens`.`api_created_at`,
    `documento_assinado_mensagens`.`documento_assinado_id`,
    `documento_assinado_mensagens`.`created_at`,
    `documento_assinado_mensagens`.`updated_at`,
    `documento_assinado_mensagens`.`deleted_at`
FROM `smart`.`documento_assinado_mensagens`;

SELECT `documento_assinados`.`id`,
    `documento_assinados`.`key`,
    `documento_assinados`.`name`,
    `documento_assinados`.`sender_name`,
    `documento_assinados`.`sender_phone`,
    `documento_assinados`.`content`,
    `documento_assinados`.`status`,
    `documento_assinados`.`signer_phone`,
    `documento_assinados`.`signer_name`,
    `documento_assinados`.`sent_at`,
    `documento_assinados`.`api_created_at`,
    `documento_assinados`.`caixa_fechamento_id`,
    `documento_assinados`.`created_at`,
    `documento_assinados`.`updated_at`,
    `documento_assinados`.`deleted_at`
FROM `smart`.`documento_assinados`;

SELECT `email_categoria_rotinas`.`id`,
    `email_categoria_rotinas`.`nome`,
    `email_categoria_rotinas`.`descricao`,
    `email_categoria_rotinas`.`email_categoria_id`,
    `email_categoria_rotinas`.`created_at`,
    `email_categoria_rotinas`.`updated_at`,
    `email_categoria_rotinas`.`deleted_at`
FROM `smart`.`email_categoria_rotinas`;

SELECT `email_categorias`.`id`,
    `email_categorias`.`nome`,
    `email_categorias`.`ativo`,
    `email_categorias`.`created_at`,
    `email_categorias`.`updated_at`,
    `email_categorias`.`deleted_at`
FROM `smart`.`email_categorias`;

SELECT `email_domain_blocklist`.`id`,
    `email_domain_blocklist`.`dominio`,
    `email_domain_blocklist`.`created_at`,
    `email_domain_blocklist`.`updated_at`
FROM `smart`.`email_domain_blocklist`;

SELECT `email_mensagem_concessionarias`.`id`,
    `email_mensagem_concessionarias`.`email_mensagem_id`,
    `email_mensagem_concessionarias`.`concessionaria_id`,
    `email_mensagem_concessionarias`.`created_at`,
    `email_mensagem_concessionarias`.`updated_at`,
    `email_mensagem_concessionarias`.`deleted_at`
FROM `smart`.`email_mensagem_concessionarias`;

SELECT `email_mensagens`.`id`,
    `email_mensagens`.`mensagem`,
    `email_mensagens`.`expired_at`,
    `email_mensagens`.`created_at`,
    `email_mensagens`.`updated_at`,
    `email_mensagens`.`deleted_at`
FROM `smart`.`email_mensagens`;

SELECT `empresa_cartao_taxas`.`id`,
    `empresa_cartao_taxas`.`bandeira`,
    `empresa_cartao_taxas`.`taxa_1`,
    `empresa_cartao_taxas`.`taxa_2`,
    `empresa_cartao_taxas`.`taxa_3`,
    `empresa_cartao_taxas`.`taxa_4`,
    `empresa_cartao_taxas`.`taxa_5`,
    `empresa_cartao_taxas`.`taxa_6`,
    `empresa_cartao_taxas`.`taxa_7`,
    `empresa_cartao_taxas`.`taxa_8`,
    `empresa_cartao_taxas`.`taxa_9`,
    `empresa_cartao_taxas`.`taxa_10`,
    `empresa_cartao_taxas`.`taxa_11`,
    `empresa_cartao_taxas`.`taxa_12`,
    `empresa_cartao_taxas`.`funcionario_registro_id`,
    `empresa_cartao_taxas`.`empresa_id`,
    `empresa_cartao_taxas`.`caixa_tipo_id`,
    `empresa_cartao_taxas`.`created_at`,
    `empresa_cartao_taxas`.`updated_at`,
    `empresa_cartao_taxas`.`deleted_at`
FROM `smart`.`empresa_cartao_taxas`;

SELECT `empresas`.`id`,
    `empresas`.`nome`,
    `empresas`.`razao_social`,
    `empresas`.`cnpj`,
    `empresas`.`ie`,
    `empresas`.`im`,
    `empresas`.`cep`,
    `empresas`.`logradouro`,
    `empresas`.`bairro`,
    `empresas`.`localidade`,
    `empresas`.`uf`,
    `empresas`.`codigo_ibge`,
    `empresas`.`numero`,
    `empresas`.`complemento`,
    `empresas`.`layout_nfse`,
    `empresas`.`optante_simples_nacional`,
    `empresas`.`crt`,
    `empresas`.`token_ibpt`,
    `empresas`.`token_sefaz_nfce`,
    `empresas`.`estabelecimento_cielo`,
    `empresas`.`user_edi_cielo`,
    `empresas`.`password_edi_cielo`,
    `empresas`.`merchant_id`,
    `empresas`.`merchant_key`,
    `empresas`.`faturamento_maximo`,
    `empresas`.`numero_empresa_remessa`,
    `empresas`.`pix_key`,
    `empresas`.`pix_client_id`,
    `empresas`.`pix_client_secret`,
    `empresas`.`pix_access_token`,
    `empresas`.`pix_access_token_expiration_date`,
    `empresas`.`pix_tentativas`,
    `empresas`.`cert_path`,
    `empresas`.`ssl_key_path`,
    `empresas`.`url_logo`,
    `empresas`.`flash_company_id`,
    `empresas`.`flash_token`,
    `empresas`.`a1_cert_path`,
    `empresas`.`a1_cert_password`,
    `empresas`.`a1_cert_created_at`,
    `empresas`.`a1_cert_expired_at`,
    `empresas`.`business_unit_id`,
    `empresas`.`porcentagem_valor_nota_produto`,
    `empresas`.`valor_trib_federal`,
    `empresas`.`valor_trib_estadual`,
    `empresas`.`valor_trib_municipal`,
    `empresas`.`ativo`,
    `empresas`.`created_at`,
    `empresas`.`updated_at`,
    `empresas`.`deleted_at`
FROM `smart`.`empresas`;

SELECT `epi`.`id`,
    `epi`.`nome`,
    `epi`.`descricao`,
    `epi`.`ca`,
    `epi`.`validade`,
    `epi`.`ativo`,
    `epi`.`created_at`,
    `epi`.`updated_at`,
    `epi`.`deleted_at`
FROM `smart`.`epi`;

SELECT `estoque_devolucao_produtos`.`id`,
    `estoque_devolucao_produtos`.`estoque_devolucao_id`,
    `estoque_devolucao_produtos`.`estoque_entrada_produto_id`,
    `estoque_devolucao_produtos`.`created_at`,
    `estoque_devolucao_produtos`.`updated_at`,
    `estoque_devolucao_produtos`.`deleted_at`
FROM `smart`.`estoque_devolucao_produtos`;

SELECT `estoque_devolucoes`.`id`,
    `estoque_devolucoes`.`justificativa`,
    `estoque_devolucoes`.`funcionario_devolucao_id`,
    `estoque_devolucoes`.`created_at`,
    `estoque_devolucoes`.`updated_at`,
    `estoque_devolucoes`.`deleted_at`
FROM `smart`.`estoque_devolucoes`;

SELECT `estoque_entrada_produtos`.`id`,
    `estoque_entrada_produtos`.`valor_unitario`,
    `estoque_entrada_produtos`.`valor_sugerido`,
    `estoque_entrada_produtos`.`valor_unitario_real`,
    `estoque_entrada_produtos`.`valor_icms`,
    `estoque_entrada_produtos`.`valor_icms_subst`,
    `estoque_entrada_produtos`.`base_icms`,
    `estoque_entrada_produtos`.`valor_ipi`,
    `estoque_entrada_produtos`.`aliquota_ipi`,
    `estoque_entrada_produtos`.`codigo`,
    `estoque_entrada_produtos`.`codigo_antigo`,
    `estoque_entrada_produtos`.`individual`,
    `estoque_entrada_produtos`.`quantidade_usos`,
    `estoque_entrada_produtos`.`tamanho`,
    `estoque_entrada_produtos`.`estoque_minimo`,
    `estoque_entrada_produtos`.`finalizado`,
    `estoque_entrada_produtos`.`data_finalizacao`,
    `estoque_entrada_produtos`.`transferido`,
    `estoque_entrada_produtos`.`data_transferencia`,
    `estoque_entrada_produtos`.`impresso`,
    `estoque_entrada_produtos`.`data_impressao`,
    `estoque_entrada_produtos`.`observacao`,
    `estoque_entrada_produtos`.`usuario_transferencia_id`,
    `estoque_entrada_produtos`.`estoque_entrada_id`,
    `estoque_entrada_produtos`.`estoque_id`,
    `estoque_entrada_produtos`.`estoque_original_id`,
    `estoque_entrada_produtos`.`produto_id`,
    `estoque_entrada_produtos`.`tonalidade_id`,
    `estoque_entrada_produtos`.`carro_modelo_id`,
    `estoque_entrada_produtos`.`os_servico_id`,
    `estoque_entrada_produtos`.`os_produto_id`,
    `estoque_entrada_produtos`.`ativo`,
    `estoque_entrada_produtos`.`created_at`,
    `estoque_entrada_produtos`.`updated_at`,
    `estoque_entrada_produtos`.`deleted_at`,
    `estoque_entrada_produtos`.`estoque_fracionamento_id`
FROM `smart`.`estoque_entrada_produtos`;

SELECT `estoque_entradas`.`id`,
    `estoque_entradas`.`nota`,
    `estoque_entradas`.`recuperacao`,
    `estoque_entradas`.`data_emissao`,
    `estoque_entradas`.`total_ipi`,
    `estoque_entradas`.`total_icms_st`,
    `estoque_entradas`.`total_produtos`,
    `estoque_entradas`.`total_tributos`,
    `estoque_entradas`.`total_nota`,
    `estoque_entradas`.`possui_frete`,
    `estoque_entradas`.`frete`,
    `estoque_entradas`.`data_vencimento`,
    `estoque_entradas`.`seguro`,
    `estoque_entradas`.`desconto`,
    `estoque_entradas`.`despesa_acessoria`,
    `estoque_entradas`.`cancelada`,
    `estoque_entradas`.`data_cancelamento`,
    `estoque_entradas`.`solicitado_cancelamento`,
    `estoque_entradas`.`estoque_id`,
    `estoque_entradas`.`fornecedor_id`,
    `estoque_entradas`.`transportadora_id`,
    `estoque_entradas`.`ordem_compra_id`,
    `estoque_entradas`.`ativo`,
    `estoque_entradas`.`created_at`,
    `estoque_entradas`.`updated_at`,
    `estoque_entradas`.`deleted_at`
FROM `smart`.`estoque_entradas`;

SELECT `estoque_fracionamento_fracoes`.`id`,
    `estoque_fracionamento_fracoes`.`tamanho`,
    `estoque_fracionamento_fracoes`.`tamanho_secundario`,
    `estoque_fracionamento_fracoes`.`codigo`,
    `estoque_fracionamento_fracoes`.`finalizado`,
    `estoque_fracionamento_fracoes`.`data_finalizacao`,
    `estoque_fracionamento_fracoes`.`observacao`,
    `estoque_fracionamento_fracoes`.`estoque_fracionamento_id`,
    `estoque_fracionamento_fracoes`.`estoque_id`,
    `estoque_fracionamento_fracoes`.`estoque_fracionamento_secundario_id`,
    `estoque_fracionamento_fracoes`.`concessionaria_id`,
    `estoque_fracionamento_fracoes`.`os_servico_id`,
    `estoque_fracionamento_fracoes`.`os_produto_id`,
    `estoque_fracionamento_fracoes`.`created_at`,
    `estoque_fracionamento_fracoes`.`updated_at`,
    `estoque_fracionamento_fracoes`.`deleted_at`
FROM `smart`.`estoque_fracionamento_fracoes`;

SELECT `estoque_fracionamentos`.`id`,
    `estoque_fracionamentos`.`tamanho`,
    `estoque_fracionamentos`.`finalizado`,
    `estoque_fracionamentos`.`data_finalizacao`,
    `estoque_fracionamentos`.`estoque_saida_produto_id`,
    `estoque_fracionamentos`.`estoque_entrada_produto_id`,
    `estoque_fracionamentos`.`produto_id`,
    `estoque_fracionamentos`.`estoque_id`,
    `estoque_fracionamentos`.`ativo`,
    `estoque_fracionamentos`.`created_at`,
    `estoque_fracionamentos`.`updated_at`,
    `estoque_fracionamentos`.`deleted_at`
FROM `smart`.`estoque_fracionamentos`;

SELECT `estoque_recuperacoes`.`id`,
    `estoque_recuperacoes`.`estoque_entrada_produto_id`,
    `estoque_recuperacoes`.`funcionario_id`,
    `estoque_recuperacoes`.`created_at`,
    `estoque_recuperacoes`.`updated_at`,
    `estoque_recuperacoes`.`deleted_at`
FROM `smart`.`estoque_recuperacoes`;

SELECT `estoques`.`id`,
    `estoques`.`nome`,
    `estoques`.`entrada_produto`,
    `estoques`.`business_unit_id`,
    `estoques`.`estoque_tipo_id`,
    `estoques`.`ativo`,
    `estoques`.`created_at`,
    `estoques`.`updated_at`,
    `estoques`.`deleted_at`
FROM `smart`.`estoques`;

SELECT `estoque_saida_historicos`.`id`,
    `estoque_saida_historicos`.`descricao`,
    `estoque_saida_historicos`.`estoque_saida_id`,
    `estoque_saida_historicos`.`estoque_saida_status_id`,
    `estoque_saida_historicos`.`funcionario_registro_id`,
    `estoque_saida_historicos`.`created_at`,
    `estoque_saida_historicos`.`updated_at`,
    `estoque_saida_historicos`.`deleted_at`
FROM `smart`.`estoque_saida_historicos`;

SELECT `estoque_saida_produto_historicos`.`id`,
    `estoque_saida_produto_historicos`.`descricao`,
    `estoque_saida_produto_historicos`.`estoque_saida_produto_id`,
    `estoque_saida_produto_historicos`.`funcionario_id`,
    `estoque_saida_produto_historicos`.`created_at`,
    `estoque_saida_produto_historicos`.`updated_at`,
    `estoque_saida_produto_historicos`.`deleted_at`
FROM `smart`.`estoque_saida_produto_historicos`;

SELECT `estoque_saida_produtos`.`id`,
    `estoque_saida_produtos`.`cancelado`,
    `estoque_saida_produtos`.`data_cancelamento`,
    `estoque_saida_produtos`.`motivo_cancelamento`,
    `estoque_saida_produtos`.`entregue`,
    `estoque_saida_produtos`.`data_entrega`,
    `estoque_saida_produtos`.`os_servico_entrega_id`,
    `estoque_saida_produtos`.`funcionario_entrega_id`,
    `estoque_saida_produtos`.`recebido`,
    `estoque_saida_produtos`.`data_recebimento`,
    `estoque_saida_produtos`.`funcionario_recebimento_id`,
    `estoque_saida_produtos`.`devolvido`,
    `estoque_saida_produtos`.`data_devolucao`,
    `estoque_saida_produtos`.`produto_id`,
    `estoque_saida_produtos`.`estoque_saida_id`,
    `estoque_saida_produtos`.`estoque_entrada_produto_id`,
    `estoque_saida_produtos`.`created_at`,
    `estoque_saida_produtos`.`updated_at`,
    `estoque_saida_produtos`.`deleted_at`
FROM `smart`.`estoque_saida_produtos`;

SELECT `estoque_saidas`.`id`,
    `estoque_saidas`.`observacao`,
    `estoque_saidas`.`solicitado_cancelamento`,
    `estoque_saidas`.`motivo_cancelamento`,
    `estoque_saidas`.`cancelada`,
    `estoque_saidas`.`data_cancelamento`,
    `estoque_saidas`.`funcionario_registro_id`,
    `estoque_saidas`.`estoque_saida_tipo_id`,
    `estoque_saidas`.`estoque_saida_status_id`,
    `estoque_saidas`.`concessionaria_id`,
    `estoque_saidas`.`concessionaria_execucao_id`,
    `estoque_saidas`.`created_at`,
    `estoque_saidas`.`updated_at`,
    `estoque_saidas`.`deleted_at`
FROM `smart`.`estoque_saidas`;

SELECT `estoque_saida_status`.`id`,
    `estoque_saida_status`.`nome`,
    `estoque_saida_status`.`created_at`,
    `estoque_saida_status`.`updated_at`,
    `estoque_saida_status`.`deleted_at`
FROM `smart`.`estoque_saida_status`;

SELECT `estoque_saida_tipos`.`id`,
    `estoque_saida_tipos`.`nome`,
    `estoque_saida_tipos`.`exibir`,
    `estoque_saida_tipos`.`created_at`,
    `estoque_saida_tipos`.`updated_at`,
    `estoque_saida_tipos`.`deleted_at`
FROM `smart`.`estoque_saida_tipos`;

SELECT `estoque_tipos`.`id`,
    `estoque_tipos`.`nome`,
    `estoque_tipos`.`ativo`,
    `estoque_tipos`.`created_at`,
    `estoque_tipos`.`updated_at`,
    `estoque_tipos`.`deleted_at`
FROM `smart`.`estoque_tipos`;

SELECT `estorno_os_servicos`.`id`,
    `estorno_os_servicos`.`estorno_id`,
    `estorno_os_servicos`.`os_servico_id`,
    `estorno_os_servicos`.`valor`,
    `estorno_os_servicos`.`created_at`,
    `estorno_os_servicos`.`updated_at`
FROM `smart`.`estorno_os_servicos`;

SELECT `estornos`.`id`,
    `estornos`.`tipo`,
    `estornos`.`valor`,
    `estornos`.`motivo`,
    `estornos`.`reason_code_id`,
    `estornos`.`observacao_aprovacao`,
    `estornos`.`status`,
    `estornos`.`permite_repagamento`,
    `estornos`.`pix_rtr_id`,
    `estornos`.`justificativa`,
    `estornos`.`solicitado_por`,
    `estornos`.`atendido_por`,
    `estornos`.`os_id`,
    `estornos`.`caixa_id`,
    `estornos`.`created_at`,
    `estornos`.`updated_at`,
    `estornos`.`deleted_at`,
    `estornos`.`aprovacao_payload`,
    `estornos`.`mc_lancamento_id`,
    `estornos`.`estorno_cancelamento_nfs_em`,
    `estornos`.`externo_solicitado_at`,
    `estornos`.`externo_solicitado_por`
FROM `smart`.`estornos`;

SELECT `estorno_statuses`.`id`,
    `estorno_statuses`.`nome`,
    `estorno_statuses`.`created_at`,
    `estorno_statuses`.`updated_at`,
    `estorno_statuses`.`deleted_at`
FROM `smart`.`estorno_statuses`;

SELECT `factories`.`id`,
    `factories`.`nome`,
    `factories`.`financeiro_caixa_destino_id`,
    `factories`.`taxa`,
    `factories`.`ativo`,
    `factories`.`created_at`,
    `factories`.`updated_at`,
    `factories`.`deleted_at`
FROM `smart`.`factories`;

SELECT `failed_jobs`.`id`,
    `failed_jobs`.`uuid`,
    `failed_jobs`.`connection`,
    `failed_jobs`.`queue`,
    `failed_jobs`.`payload`,
    `failed_jobs`.`exception`,
    `failed_jobs`.`failed_at`
FROM `smart`.`failed_jobs`;

SELECT `feriados`.`id`,
    `feriados`.`nome`,
    `feriados`.`descricao`,
    `feriados`.`data`,
    `feriados`.`ativo`,
    `feriados`.`created_at`,
    `feriados`.`updated_at`,
    `feriados`.`deleted_at`
FROM `smart`.`feriados`;

SELECT `financeiro_caixas_destino`.`id`,
    `financeiro_caixas_destino`.`nome`,
    `financeiro_caixas_destino`.`ativo`,
    `financeiro_caixas_destino`.`created_at`,
    `financeiro_caixas_destino`.`updated_at`,
    `financeiro_caixas_destino`.`deleted_at`
FROM `smart`.`financeiro_caixas_destino`;

SELECT `financeiro_malotes_classificacao`.`id`,
    `financeiro_malotes_classificacao`.`valor`,
    `financeiro_malotes_classificacao`.`auditado`,
    `financeiro_malotes_classificacao`.`data_auditoria`,
    `financeiro_malotes_classificacao`.`classificado`,
    `financeiro_malotes_classificacao`.`data_classificacao`,
    `financeiro_malotes_classificacao`.`caixa_preto`,
    `financeiro_malotes_classificacao`.`usuario_auditoria_id`,
    `financeiro_malotes_classificacao`.`usuario_classificacao_id`,
    `financeiro_malotes_classificacao`.`ativo`,
    `financeiro_malotes_classificacao`.`created_at`,
    `financeiro_malotes_classificacao`.`updated_at`,
    `financeiro_malotes_classificacao`.`deleted_at`
FROM `smart`.`financeiro_malotes_classificacao`;

SELECT `financeiro_recibos`.`id`,
    `financeiro_recibos`.`valor`,
    `financeiro_recibos`.`nome`,
    `financeiro_recibos`.`cpf`,
    `financeiro_recibos`.`conteudo`,
    `financeiro_recibos`.`empresa_id`,
    `financeiro_recibos`.`financeiro_recibo_tipo_id`,
    `financeiro_recibos`.`funcionario_emissao_id`,
    `financeiro_recibos`.`created_at`,
    `financeiro_recibos`.`updated_at`,
    `financeiro_recibos`.`deleted_at`
FROM `smart`.`financeiro_recibos`;

SELECT `financeiro_recibo_tipos`.`id`,
    `financeiro_recibo_tipos`.`nome`,
    `financeiro_recibo_tipos`.`ativo`,
    `financeiro_recibo_tipos`.`created_at`,
    `financeiro_recibo_tipos`.`updated_at`,
    `financeiro_recibo_tipos`.`deleted_at`
FROM `smart`.`financeiro_recibo_tipos`;

SELECT `folha_pagamento_funcionarios`.`id`,
    `folha_pagamento_funcionarios`.`tipo`,
    `folha_pagamento_funcionarios`.`codigo_contabilidade`,
    `folha_pagamento_funcionarios`.`nome`,
    `folha_pagamento_funcionarios`.`valor`,
    `folha_pagamento_funcionarios`.`cpf`,
    `folha_pagamento_funcionarios`.`banco`,
    `folha_pagamento_funcionarios`.`agencia`,
    `folha_pagamento_funcionarios`.`conta`,
    `folha_pagamento_funcionarios`.`folha_pagamento_id`,
    `folha_pagamento_funcionarios`.`funcionario_id`,
    `folha_pagamento_funcionarios`.`created_at`,
    `folha_pagamento_funcionarios`.`updated_at`,
    `folha_pagamento_funcionarios`.`deleted_at`
FROM `smart`.`folha_pagamento_funcionarios`;

SELECT `folha_pagamentos`.`id`,
    `folha_pagamentos`.`valor`,
    `folha_pagamentos`.`data_emissao`,
    `folha_pagamentos`.`url`,
    `folha_pagamentos`.`data_validacao`,
    `folha_pagamentos`.`empresa_id`,
    `folha_pagamentos`.`mc_lancamento_entrada_id`,
    `folha_pagamentos`.`mc_user_validacao_id`,
    `folha_pagamentos`.`created_at`,
    `folha_pagamentos`.`updated_at`,
    `folha_pagamentos`.`deleted_at`
FROM `smart`.`folha_pagamentos`;

SELECT `fornecedores`.`id`,
    `fornecedores`.`nome`,
    `fornecedores`.`razao_social`,
    `fornecedores`.`cnpj`,
    `fornecedores`.`ie`,
    `fornecedores`.`im`,
    `fornecedores`.`cep`,
    `fornecedores`.`logradouro`,
    `fornecedores`.`bairro`,
    `fornecedores`.`localidade`,
    `fornecedores`.`uf`,
    `fornecedores`.`codigo_ibge`,
    `fornecedores`.`numero`,
    `fornecedores`.`complemento`,
    `fornecedores`.`contato`,
    `fornecedores`.`telefone1`,
    `fornecedores`.`telefone2`,
    `fornecedores`.`email`,
    `fornecedores`.`confirmacao_entrega`,
    `fornecedores`.`freelancer`,
    `fornecedores`.`ativo`,
    `fornecedores`.`estoque_id`,
    `fornecedores`.`created_at`,
    `fornecedores`.`updated_at`,
    `fornecedores`.`deleted_at`
FROM `smart`.`fornecedores`;

SELECT `fornecedor_produtos`.`id`,
    `fornecedor_produtos`.`valor_unitario`,
    `fornecedor_produtos`.`valor_icms`,
    `fornecedor_produtos`.`aliquota_ipi`,
    `fornecedor_produtos`.`fornecedor_id`,
    `fornecedor_produtos`.`produto_id`,
    `fornecedor_produtos`.`ativo`,
    `fornecedor_produtos`.`created_at`,
    `fornecedor_produtos`.`updated_at`,
    `fornecedor_produtos`.`deleted_at`
FROM `smart`.`fornecedor_produtos`;

SELECT `freelancer_despesas`.`id`,
    `freelancer_despesas`.`comissionado_id`,
    `freelancer_despesas`.`descricao`,
    `freelancer_despesas`.`valor`,
    `freelancer_despesas`.`nf_entrada_id`,
    `freelancer_despesas`.`mc_lancamento_entrada_id`,
    `freelancer_despesas`.`created_at`,
    `freelancer_despesas`.`updated_at`,
    `freelancer_despesas`.`deleted_at`
FROM `smart`.`freelancer_despesas`;

SELECT `freelancer_servicos`.`id`,
    `freelancer_servicos`.`valor_comissao`,
    `freelancer_servicos`.`funcionario_id`,
    `freelancer_servicos`.`servico_id`,
    `freelancer_servicos`.`created_at`,
    `freelancer_servicos`.`updated_at`,
    `freelancer_servicos`.`deleted_at`
FROM `smart`.`freelancer_servicos`;

SELECT `funcionario_cargos`.`id`,
    `funcionario_cargos`.`matricula`,
    `funcionario_cargos`.`salario`,
    `funcionario_cargos`.`data_admissao`,
    `funcionario_cargos`.`demitido`,
    `funcionario_cargos`.`data_demissao`,
    `funcionario_cargos`.`motivo_demissao`,
    `funcionario_cargos`.`fixo`,
    `funcionario_cargos`.`reemprego`,
    `funcionario_cargos`.`periodo_experiencia`,
    `funcionario_cargos`.`inicio_experiencia`,
    `funcionario_cargos`.`fim_experiencia`,
    `funcionario_cargos`.`funcionario_id`,
    `funcionario_cargos`.`cargo_id`,
    `funcionario_cargos`.`empresa_id`,
    `funcionario_cargos`.`produtivo_tipo_id`,
    `funcionario_cargos`.`funcionario_local_id`,
    `funcionario_cargos`.`concessionaria_local_id`,
    `funcionario_cargos`.`ativo`,
    `funcionario_cargos`.`created_at`,
    `funcionario_cargos`.`updated_at`,
    `funcionario_cargos`.`deleted_at`
FROM `smart`.`funcionario_cargos`;

SELECT `funcionario_concessionaria_departamentos`.`id`,
    `funcionario_concessionaria_departamentos`.`funcionario_concessionaria_id`,
    `funcionario_concessionaria_departamentos`.`departamento_id`,
    `funcionario_concessionaria_departamentos`.`ativo`,
    `funcionario_concessionaria_departamentos`.`created_at`,
    `funcionario_concessionaria_departamentos`.`updated_at`,
    `funcionario_concessionaria_departamentos`.`deleted_at`
FROM `smart`.`funcionario_concessionaria_departamentos`;

SELECT `funcionario_concessionarias`.`id`,
    `funcionario_concessionarias`.`funcionario_id`,
    `funcionario_concessionarias`.`concessionaria_id`,
    `funcionario_concessionarias`.`logistics_center_id`,
    `funcionario_concessionarias`.`padrao`,
    `funcionario_concessionarias`.`ativo`,
    `funcionario_concessionarias`.`created_at`,
    `funcionario_concessionarias`.`updated_at`,
    `funcionario_concessionarias`.`deleted_at`
FROM `smart`.`funcionario_concessionarias`;

SELECT `funcionario_epi_entregas`.`id`,
    `funcionario_epi_entregas`.`quantidade`,
    `funcionario_epi_entregas`.`funcionario_id`,
    `funcionario_epi_entregas`.`epi_id`,
    `funcionario_epi_entregas`.`data_entrega`,
    `funcionario_epi_entregas`.`created_at`,
    `funcionario_epi_entregas`.`updated_at`,
    `funcionario_epi_entregas`.`deleted_at`
FROM `smart`.`funcionario_epi_entregas`;

SELECT `funcionario_estoques`.`id`,
    `funcionario_estoques`.`funcionario_id`,
    `funcionario_estoques`.`estoque_id`,
    `funcionario_estoques`.`padrao`,
    `funcionario_estoques`.`ativo`,
    `funcionario_estoques`.`created_at`,
    `funcionario_estoques`.`updated_at`,
    `funcionario_estoques`.`deleted_at`
FROM `smart`.`funcionario_estoques`;

SELECT `funcionario_locais`.`id`,
    `funcionario_locais`.`nome`,
    `funcionario_locais`.`ativo`,
    `funcionario_locais`.`created_at`,
    `funcionario_locais`.`updated_at`,
    `funcionario_locais`.`deleted_at`
FROM `smart`.`funcionario_locais`;

SELECT `funcionario_ponto_marcacoes`.`id`,
    `funcionario_ponto_marcacoes`.`data`,
    `funcionario_ponto_marcacoes`.`ajuste`,
    `funcionario_ponto_marcacoes`.`motivo`,
    `funcionario_ponto_marcacoes`.`funcionario_id`,
    `funcionario_ponto_marcacoes`.`empresa_id`,
    `funcionario_ponto_marcacoes`.`created_at`,
    `funcionario_ponto_marcacoes`.`updated_at`,
    `funcionario_ponto_marcacoes`.`deleted_at`
FROM `smart`.`funcionario_ponto_marcacoes`;

SELECT `funcionario_retorno_motivos`.`id`,
    `funcionario_retorno_motivos`.`funcionario_id`,
    `funcionario_retorno_motivos`.`retorno_motivo_id`,
    `funcionario_retorno_motivos`.`created_at`,
    `funcionario_retorno_motivos`.`updated_at`,
    `funcionario_retorno_motivos`.`deleted_at`
FROM `smart`.`funcionario_retorno_motivos`;

SELECT `funcionarios`.`id`,
    `funcionarios`.`nome`,
    `funcionarios`.`cpf`,
    `funcionarios`.`rg`,
    `funcionarios`.`data_nascimento`,
    `funcionarios`.`telefone`,
    `funcionarios`.`email`,
    `funcionarios`.`agencia`,
    `funcionarios`.`conta`,
    `funcionarios`.`url_foto`,
    `funcionarios`.`terceiros`,
    `funcionarios`.`freelancer`,
    `funcionarios`.`codigo_contabilidade`,
    `funcionarios`.`fornecedor_id`,
    `funcionarios`.`banco_id`,
    `funcionarios`.`banco_conta_tipo_id`,
    `funcionarios`.`funcionario_situacao_id`,
    `funcionarios`.`created_at`,
    `funcionarios`.`updated_at`,
    `funcionarios`.`deleted_at`,
    `funcionarios`.`raca_cor_id`
FROM `smart`.`funcionarios`;

SELECT `funcionario_situacoes`.`id`,
    `funcionario_situacoes`.`nome`,
    `funcionario_situacoes`.`created_at`,
    `funcionario_situacoes`.`updated_at`,
    `funcionario_situacoes`.`deleted_at`
FROM `smart`.`funcionario_situacoes`;

SELECT `funcionario_tipos`.`id`,
    `funcionario_tipos`.`nome`,
    `funcionario_tipos`.`ativo`,
    `funcionario_tipos`.`created_at`,
    `funcionario_tipos`.`updated_at`,
    `funcionario_tipos`.`deleted_at`
FROM `smart`.`funcionario_tipos`;

SELECT `funcionario_vt_cartoes`.`id`,
    `funcionario_vt_cartoes`.`quantidade_passes`,
    `funcionario_vt_cartoes`.`valor_passe`,
    `funcionario_vt_cartoes`.`valor_inicial`,
    `funcionario_vt_cartoes`.`cancelado`,
    `funcionario_vt_cartoes`.`data_cancelamento`,
    `funcionario_vt_cartoes`.`justificativa_cancelamento`,
    `funcionario_vt_cartoes`.`observacao`,
    `funcionario_vt_cartoes`.`funcionario_id`,
    `funcionario_vt_cartoes`.`vt_cartao_id`,
    `funcionario_vt_cartoes`.`created_at`,
    `funcionario_vt_cartoes`.`updated_at`,
    `funcionario_vt_cartoes`.`deleted_at`
FROM `smart`.`funcionario_vt_cartoes`;

SELECT `grupos_produtos`.`id`,
    `grupos_produtos`.`nome`,
    `grupos_produtos`.`ativo`,
    `grupos_produtos`.`created_at`,
    `grupos_produtos`.`updated_at`,
    `grupos_produtos`.`deleted_at`
FROM `smart`.`grupos_produtos`;

SELECT `grupos_servicos`.`id`,
    `grupos_servicos`.`nome`,
    `grupos_servicos`.`ativo`,
    `grupos_servicos`.`created_at`,
    `grupos_servicos`.`updated_at`,
    `grupos_servicos`.`deleted_at`
FROM `smart`.`grupos_servicos`;

SELECT `grupos_usuarios`.`id`,
    `grupos_usuarios`.`nome`,
    `grupos_usuarios`.`descricao`,
    `grupos_usuarios`.`roles`,
    `grupos_usuarios`.`transporta_malote`,
    `grupos_usuarios`.`vincula_concessionaria`,
    `grupos_usuarios`.`ativo`,
    `grupos_usuarios`.`created_at`,
    `grupos_usuarios`.`updated_at`,
    `grupos_usuarios`.`deleted_at`
FROM `smart`.`grupos_usuarios`;

SELECT `grupo_usuario_modulos`.`id`,
    `grupo_usuario_modulos`.`padrao`,
    `grupo_usuario_modulos`.`modulo_id`,
    `grupo_usuario_modulos`.`grupo_usuario_id`,
    `grupo_usuario_modulos`.`ativo`,
    `grupo_usuario_modulos`.`created_at`,
    `grupo_usuario_modulos`.`updated_at`,
    `grupo_usuario_modulos`.`deleted_at`
FROM `smart`.`grupo_usuario_modulos`;

SELECT `grupo_usuario_telas`.`id`,
    `grupo_usuario_telas`.`tela_id`,
    `grupo_usuario_telas`.`grupo_usuario_id`,
    `grupo_usuario_telas`.`modulo_id`,
    `grupo_usuario_telas`.`ativo`,
    `grupo_usuario_telas`.`created_at`,
    `grupo_usuario_telas`.`updated_at`,
    `grupo_usuario_telas`.`deleted_at`
FROM `smart`.`grupo_usuario_telas`;

SELECT `historico_cheques`.`id`,
    `historico_cheques`.`caixa_id`,
    `historico_cheques`.`num_cheque`,
    `historico_cheques`.`acao`,
    `historico_cheques`.`created_at`,
    `historico_cheques`.`updated_at`,
    `historico_cheques`.`deleted_at`
FROM `smart`.`historico_cheques`;

SELECT `holerite_lancamentos`.`id`,
    `holerite_lancamentos`.`codigo`,
    `holerite_lancamentos`.`descricao`,
    `holerite_lancamentos`.`referencia`,
    `holerite_lancamentos`.`desconto`,
    `holerite_lancamentos`.`valor`,
    `holerite_lancamentos`.`holerite_id`,
    `holerite_lancamentos`.`created_at`,
    `holerite_lancamentos`.`updated_at`,
    `holerite_lancamentos`.`deleted_at`
FROM `smart`.`holerite_lancamentos`;

SELECT `holerites`.`id`,
    `holerites`.`periodo`,
    `holerites`.`matricula`,
    `holerites`.`tipo`,
    `holerites`.`categoria_cargo`,
    `holerites`.`cargo`,
    `holerites`.`cbo`,
    `holerites`.`departamento`,
    `holerites`.`filial`,
    `holerites`.`data_admissao`,
    `holerites`.`observacoes`,
    `holerites`.`total_vencimentos`,
    `holerites`.`total_descontos`,
    `holerites`.`salario_base`,
    `holerites`.`base_inss`,
    `holerites`.`base_fgts`,
    `holerites`.`total_fgts`,
    `holerites`.`base_irrf`,
    `holerites`.`aliquota_irrf`,
    `holerites`.`funcionario_id`,
    `holerites`.`empresa_id`,
    `holerites`.`created_at`,
    `holerites`.`updated_at`,
    `holerites`.`deleted_at`
FROM `smart`.`holerites`;

SELECT `icms_aliquotas`.`id`,
    `icms_aliquotas`.`aliquota_uf`,
    `icms_aliquotas`.`aliquota_interestadual`,
    `icms_aliquotas`.`uf`,
    `icms_aliquotas`.`created_at`,
    `icms_aliquotas`.`updated_at`,
    `icms_aliquotas`.`deleted_at`
FROM `smart`.`icms_aliquotas`;

SELECT `indicador_concessionaria_departamentos`.`id`,
    `indicador_concessionaria_departamentos`.`indicador_concessionaria_id`,
    `indicador_concessionaria_departamentos`.`departamento_id`,
    `indicador_concessionaria_departamentos`.`ativo`,
    `indicador_concessionaria_departamentos`.`created_at`,
    `indicador_concessionaria_departamentos`.`updated_at`,
    `indicador_concessionaria_departamentos`.`deleted_at`
FROM `smart`.`indicador_concessionaria_departamentos`;

SELECT `indicador_concessionarias`.`id`,
    `indicador_concessionarias`.`indicador_id`,
    `indicador_concessionarias`.`concessionaria_id`,
    `indicador_concessionarias`.`ativo`,
    `indicador_concessionarias`.`created_at`,
    `indicador_concessionarias`.`updated_at`,
    `indicador_concessionarias`.`deleted_at`
FROM `smart`.`indicador_concessionarias`;

SELECT `indicadores`.`id`,
    `indicadores`.`nome`,
    `indicadores`.`nome_mae`,
    `indicadores`.`data_nascimento`,
    `indicadores`.`numero_cartao`,
    `indicadores`.`nome_completo`,
    `indicadores`.`cpf`,
    `indicadores`.`matricula`,
    `indicadores`.`funcao`,
    `indicadores`.`agencia`,
    `indicadores`.`conta`,
    `indicadores`.`telefone`,
    `indicadores`.`email`,
    `indicadores`.`indicador_tipo_id`,
    `indicadores`.`banco_id`,
    `indicadores`.`banco_conta_tipo_id`,
    `indicadores`.`flash_employee_id`,
    `indicadores`.`ativo`,
    `indicadores`.`created_at`,
    `indicadores`.`updated_at`,
    `indicadores`.`deleted_at`
FROM `smart`.`indicadores`;

SELECT `indicador_historicos`.`id`,
    `indicador_historicos`.`descricao`,
    `indicador_historicos`.`indicador_id`,
    `indicador_historicos`.`funcionario_id`,
    `indicador_historicos`.`created_at`,
    `indicador_historicos`.`updated_at`,
    `indicador_historicos`.`deleted_at`
FROM `smart`.`indicador_historicos`;

SELECT `indicador_tipos`.`id`,
    `indicador_tipos`.`nome`,
    `indicador_tipos`.`ativo`,
    `indicador_tipos`.`created_at`,
    `indicador_tipos`.`updated_at`,
    `indicador_tipos`.`deleted_at`
FROM `smart`.`indicador_tipos`;

SELECT `llm_perguntas`.`id`,
    `llm_perguntas`.`modelo`,
    `llm_perguntas`.`contexto`,
    `llm_perguntas`.`pergunta`,
    `llm_perguntas`.`resposta`,
    `llm_perguntas`.`debug`,
    `llm_perguntas`.`avaliacao`,
    `llm_perguntas`.`created_by`,
    `llm_perguntas`.`created_at`,
    `llm_perguntas`.`updated_at`,
    `llm_perguntas`.`deleted_at`
FROM `smart`.`llm_perguntas`;

SELECT `log_integracao_api_externa`.`id`,
    `log_integracao_api_externa`.`correlation_id`,
    `log_integracao_api_externa`.`provedor`,
    `log_integracao_api_externa`.`operacao`,
    `log_integracao_api_externa`.`metodo_http`,
    `log_integracao_api_externa`.`url`,
    `log_integracao_api_externa`.`status_http`,
    `log_integracao_api_externa`.`payload_requisicao`,
    `log_integracao_api_externa`.`payload_resposta`,
    `log_integracao_api_externa`.`sucesso`,
    `log_integracao_api_externa`.`mensagem_erro`,
    `log_integracao_api_externa`.`contexto`,
    `log_integracao_api_externa`.`usuario_id`,
    `log_integracao_api_externa`.`created_at`,
    `log_integracao_api_externa`.`updated_at`
FROM `smart`.`log_integracao_api_externa`;

SELECT `logistica_expedicao_historicos`.`id`,
    `logistica_expedicao_historicos`.`logistica_expedicao_id`,
    `logistica_expedicao_historicos`.`logistica_expedicao_status_id`,
    `logistica_expedicao_historicos`.`funcionario_registro_id`,
    `logistica_expedicao_historicos`.`funcionario_recebimento_id`,
    `logistica_expedicao_historicos`.`created_at`,
    `logistica_expedicao_historicos`.`updated_at`,
    `logistica_expedicao_historicos`.`deleted_at`
FROM `smart`.`logistica_expedicao_historicos`;

SELECT `logistica_expedicao_saidas`.`id`,
    `logistica_expedicao_saidas`.`cancelada`,
    `logistica_expedicao_saidas`.`logistica_expedicao_id`,
    `logistica_expedicao_saidas`.`saida_id`,
    `logistica_expedicao_saidas`.`requisicao_id`,
    `logistica_expedicao_saidas`.`created_at`,
    `logistica_expedicao_saidas`.`updated_at`,
    `logistica_expedicao_saidas`.`deleted_at`
FROM `smart`.`logistica_expedicao_saidas`;

SELECT `logistica_expedicao_statuses`.`id`,
    `logistica_expedicao_statuses`.`nome`,
    `logistica_expedicao_statuses`.`created_at`,
    `logistica_expedicao_statuses`.`updated_at`,
    `logistica_expedicao_statuses`.`deleted_at`
FROM `smart`.`logistica_expedicao_statuses`;

SELECT `logistica_expedicoes`.`id`,
    `logistica_expedicoes`.`codigo`,
    `logistica_expedicoes`.`expedicao_tipo`,
    `logistica_expedicoes`.`cancelado`,
    `logistica_expedicoes`.`data_cancelamento`,
    `logistica_expedicoes`.`finalizado`,
    `logistica_expedicoes`.`data_finalizacao`,
    `logistica_expedicoes`.`logistica_expedicao_status_id`,
    `logistica_expedicoes`.`concessionaria_id`,
    `logistica_expedicoes`.`funcionario_registro_id`,
    `logistica_expedicoes`.`funcionario_logistica_id`,
    `logistica_expedicoes`.`funcionario_recebimento_id`,
    `logistica_expedicoes`.`nome_recebedor`,
    `logistica_expedicoes`.`created_at`,
    `logistica_expedicoes`.`updated_at`,
    `logistica_expedicoes`.`deleted_at`
FROM `smart`.`logistica_expedicoes`;

SELECT `logistics_center_concessionaria`.`logistics_center_id`,
    `logistics_center_concessionaria`.`concessionaria_id`,
    `logistics_center_concessionaria`.`created_at`,
    `logistics_center_concessionaria`.`updated_at`
FROM `smart`.`logistics_center_concessionaria`;

SELECT `logistics_centers`.`id`,
    `logistics_centers`.`nome`,
    `logistics_centers`.`cep`,
    `logistics_centers`.`logradouro`,
    `logistics_centers`.`numero`,
    `logistics_centers`.`complemento`,
    `logistics_centers`.`bairro`,
    `logistics_centers`.`localidade`,
    `logistics_centers`.`uf`,
    `logistics_centers`.`codigo_ibge`,
    `logistics_centers`.`ativo`,
    `logistics_centers`.`created_at`,
    `logistics_centers`.`updated_at`,
    `logistics_centers`.`deleted_at`,
    `logistics_centers`.`region_id`
FROM `smart`.`logistics_centers`;

SELECT `malotes`.`id`,
    `malotes`.`valor`,
    `malotes`.`recebido`,
    `malotes`.`data_recebimento`,
    `malotes`.`verificado`,
    `malotes`.`data_verificacao`,
    `malotes`.`usuario_verificacao_id`,
    `malotes`.`codigo`,
    `malotes`.`caixa_concessionaria`,
    `malotes`.`concessionaria_id`,
    `malotes`.`usuario_logistica_id`,
    `malotes`.`usuario_recebimento_id`,
    `malotes`.`ativo`,
    `malotes`.`created_at`,
    `malotes`.`updated_at`,
    `malotes`.`deleted_at`
FROM `smart`.`malotes`;

SELECT `medidas`.`id`,
    `medidas`.`nome`,
    `medidas`.`sigla`,
    `medidas`.`ativo`,
    `medidas`.`created_at`,
    `medidas`.`updated_at`,
    `medidas`.`deleted_at`
FROM `smart`.`medidas`;

SELECT `migrations`.`migration`,
    `migrations`.`batch`
FROM `smart`.`migrations`;

SELECT `modulos`.`id`,
    `modulos`.`ordem`,
    `modulos`.`nome`,
    `modulos`.`index`,
    `modulos`.`classe`,
    `modulos`.`icone`,
    `modulos`.`v3`,
    `modulos`.`ativo`,
    `modulos`.`created_at`,
    `modulos`.`updated_at`,
    `modulos`.`deleted_at`
FROM `smart`.`modulos`;

SELECT `nf_devolucao_itens`.`id`,
    `nf_devolucao_itens`.`motivo_devolucao`,
    `nf_devolucao_itens`.`codigo`,
    `nf_devolucao_itens`.`descricao`,
    `nf_devolucao_itens`.`quantidade`,
    `nf_devolucao_itens`.`medida`,
    `nf_devolucao_itens`.`valor_unitario`,
    `nf_devolucao_itens`.`ncm`,
    `nf_devolucao_itens`.`cfop`,
    `nf_devolucao_itens`.`cst`,
    `nf_devolucao_itens`.`cst_ibs_cbs`,
    `nf_devolucao_itens`.`cclasstrib_ibs_cbs`,
    `nf_devolucao_itens`.`base_calculo_ibs_cbs`,
    `nf_devolucao_itens`.`valor_ibs_uf`,
    `nf_devolucao_itens`.`valor_ibs_mun`,
    `nf_devolucao_itens`.`valor_cbs`,
    `nf_devolucao_itens`.`valor_ipi`,
    `nf_devolucao_itens`.`aliquota_ipi`,
    `nf_devolucao_itens`.`valor_icms`,
    `nf_devolucao_itens`.`aliquota_icms`,
    `nf_devolucao_itens`.`base_calculo_icms`,
    `nf_devolucao_itens`.`valor_icms_st`,
    `nf_devolucao_itens`.`valor_total`,
    `nf_devolucao_itens`.`valor_frete`,
    `nf_devolucao_itens`.`valor_seguro`,
    `nf_devolucao_itens`.`porcentagem_devolucao`,
    `nf_devolucao_itens`.`origem`,
    `nf_devolucao_itens`.`nota_fiscal_id`,
    `nf_devolucao_itens`.`created_at`,
    `nf_devolucao_itens`.`updated_at`,
    `nf_devolucao_itens`.`deleted_at`
FROM `smart`.`nf_devolucao_itens`;

SELECT `nf_entrada_dfes`.`id`,
    `nf_entrada_dfes`.`tipo`,
    `nf_entrada_dfes`.`nsu`,
    `nf_entrada_dfes`.`url_xml`,
    `nf_entrada_dfes`.`nf_entrada_id`,
    `nf_entrada_dfes`.`created_at`,
    `nf_entrada_dfes`.`updated_at`,
    `nf_entrada_dfes`.`deleted_at`
FROM `smart`.`nf_entrada_dfes`;

SELECT `nf_entrada_itens`.`id`,
    `nf_entrada_itens`.`codigo`,
    `nf_entrada_itens`.`descricao`,
    `nf_entrada_itens`.`valor_unitario`,
    `nf_entrada_itens`.`quantidade`,
    `nf_entrada_itens`.`quantidade_nf`,
    `nf_entrada_itens`.`tamanho`,
    `nf_entrada_itens`.`valor_bruto`,
    `nf_entrada_itens`.`valor_imposto`,
    `nf_entrada_itens`.`valor_liquido`,
    `nf_entrada_itens`.`nf_entrada_id`,
    `nf_entrada_itens`.`produto_id`,
    `nf_entrada_itens`.`tonalidade_id`,
    `nf_entrada_itens`.`carro_modelo_id`,
    `nf_entrada_itens`.`created_at`,
    `nf_entrada_itens`.`updated_at`,
    `nf_entrada_itens`.`deleted_at`
FROM `smart`.`nf_entrada_itens`;

SELECT `nf_entrada_resumos`.`id`,
    `nf_entrada_resumos`.`empresa_id`,
    `nf_entrada_resumos`.`chave`,
    `nf_entrada_resumos`.`numero`,
    `nf_entrada_resumos`.`emitente_cnpj`,
    `nf_entrada_resumos`.`emitente_nome`,
    `nf_entrada_resumos`.`valor`,
    `nf_entrada_resumos`.`data_emissao`,
    `nf_entrada_resumos`.`nsu`,
    `nf_entrada_resumos`.`url_xml`,
    `nf_entrada_resumos`.`confirmada_em`,
    `nf_entrada_resumos`.`protocolo_confirmacao`,
    `nf_entrada_resumos`.`mc_user_confirmacao_id`,
    `nf_entrada_resumos`.`created_at`,
    `nf_entrada_resumos`.`updated_at`,
    `nf_entrada_resumos`.`deleted_at`
FROM `smart`.`nf_entrada_resumos`;

SELECT `nf_entradas`.`id`,
    `nf_entradas`.`tipo`,
    `nf_entradas`.`nsu`,
    `nf_entradas`.`chave`,
    `nf_entradas`.`numero`,
    `nf_entradas`.`valor_bruto`,
    `nf_entradas`.`valor_imposto`,
    `nf_entradas`.`valor_liquido`,
    `nf_entradas`.`data_emissao`,
    `nf_entradas`.`pagamentos`,
    `nf_entradas`.`url_xml`,
    `nf_entradas`.`url_pdf`,
    `nf_entradas`.`finalizada`,
    `nf_entradas`.`data_finalizacao`,
    `nf_entradas`.`cancelada`,
    `nf_entradas`.`data_cancelamento`,
    `nf_entradas`.`motivo_cancelamento`,
    `nf_entradas`.`fornecedor_id`,
    `nf_entradas`.`estoque_entrada_id`,
    `nf_entradas`.`empresa_id`,
    `nf_entradas`.`mc_user_finalizacao_id`,
    `nf_entradas`.`mc_user_cancelamento_id`,
    `nf_entradas`.`mc_cadastro_cancelamento_motivo_id`,
    `nf_entradas`.`mc_lancamento_entrada_id`,
    `nf_entradas`.`mc_cadastro_fornecedor_id`,
    `nf_entradas`.`mc_cadastro_empresa_id`,
    `nf_entradas`.`mc_cadastro_tipo_id`,
    `nf_entradas`.`mc_cadastro_caixa_id`,
    `nf_entradas`.`created_at`,
    `nf_entradas`.`updated_at`,
    `nf_entradas`.`deleted_at`
FROM `smart`.`nf_entradas`;

SELECT `nota_fiscal_statuses`.`id`,
    `nota_fiscal_statuses`.`nome`,
    `nota_fiscal_statuses`.`created_at`,
    `nota_fiscal_statuses`.`updated_at`,
    `nota_fiscal_statuses`.`deleted_at`
FROM `smart`.`nota_fiscal_statuses`;

SELECT `notas_fiscais`.`id`,
    `notas_fiscais`.`valor_bruto`,
    `notas_fiscais`.`valor_liquido`,
    `notas_fiscais`.`retencao_iss`,
    `notas_fiscais`.`data_emissao`,
    `notas_fiscais`.`tipo_nota`,
    `notas_fiscais`.`serie`,
    `notas_fiscais`.`bancotoyota`,
    `notas_fiscais`.`numero_nota`,
    `notas_fiscais`.`chave_nota`,
    `notas_fiscais`.`numero_registro`,
    `notas_fiscais`.`status_nota`,
    `notas_fiscais`.`danfe_emitida`,
    `notas_fiscais`.`email_enviado`,
    `notas_fiscais`.`url_danfe`,
    `notas_fiscais`.`resposta_erro`,
    `notas_fiscais`.`cancelada`,
    `notas_fiscais`.`data_cancelamento`,
    `notas_fiscais`.`solicitado_cancelamento`,
    `notas_fiscais`.`motivo_cancelamento`,
    `notas_fiscais`.`devolvida`,
    `notas_fiscais`.`data_devolucao`,
    `notas_fiscais`.`solicitado_devolucao`,
    `notas_fiscais`.`cancelamento_extemporaneo`,
    `notas_fiscais`.`data_cancelamento_extemporaneo`,
    `notas_fiscais`.`solicitado_cancelamento_extemporaneo`,
    `notas_fiscais`.`cancelamento_solicitado_em`,
    `notas_fiscais`.`observacao_devolucao`,
    `notas_fiscais`.`devolucao_pelo_cliente`,
    `notas_fiscais`.`chave_nfe_referencia`,
    `notas_fiscais`.`chave_cte_referencia`,
    `notas_fiscais`.`observacao`,
    `notas_fiscais`.`info_adicional`,
    `notas_fiscais`.`natureza_operacao`,
    `notas_fiscais`.`nfe_inf_complementar`,
    `notas_fiscais`.`nfe_transport_mod_frete`,
    `notas_fiscais`.`nfe_vol_qvol`,
    `notas_fiscais`.`nfe_vol_peso_liquido`,
    `notas_fiscais`.`nfe_vol_peso_bruto`,
    `notas_fiscais`.`nfe_vol_especie`,
    `notas_fiscais`.`nfe_vol_marca`,
    `notas_fiscais`.`nfe_vol_nvol`,
    `notas_fiscais`.`nfe_aliq_pis`,
    `notas_fiscais`.`nfe_aliq_cofins`,
    `notas_fiscais`.`nfe_aliq_icms`,
    `notas_fiscais`.`boleto_emitido`,
    `notas_fiscais`.`url_boleto`,
    `notas_fiscais`.`data_emissao_boleto`,
    `notas_fiscais`.`data_vencimento_boleto`,
    `notas_fiscais`.`boleto_registrado`,
    `notas_fiscais`.`data_registro_boleto`,
    `notas_fiscais`.`lancado_moneycare`,
    `notas_fiscais`.`data_lancamento_moneycare`,
    `notas_fiscais`.`os_id`,
    `notas_fiscais`.`cortesia_id`,
    `notas_fiscais`.`fornecedor_id`,
    `notas_fiscais`.`parent_id`,
    `notas_fiscais`.`boleto_remessa_id`,
    `notas_fiscais`.`empresa_id`,
    `notas_fiscais`.`ativo`,
    `notas_fiscais`.`created_at`,
    `notas_fiscais`.`updated_at`,
    `notas_fiscais`.`deleted_at`
FROM `smart`.`notas_fiscais`;

SELECT `nota_tipos`.`id`,
    `nota_tipos`.`nome`,
    `nota_tipos`.`ativo`,
    `nota_tipos`.`created_at`,
    `nota_tipos`.`updated_at`,
    `nota_tipos`.`deleted_at`
FROM `smart`.`nota_tipos`;

SELECT `observacao_sugerida_departamentos`.`id`,
    `observacao_sugerida_departamentos`.`observacao_id`,
    `observacao_sugerida_departamentos`.`departamento_id`,
    `observacao_sugerida_departamentos`.`ativo`,
    `observacao_sugerida_departamentos`.`created_at`,
    `observacao_sugerida_departamentos`.`updated_at`,
    `observacao_sugerida_departamentos`.`deleted_at`
FROM `smart`.`observacao_sugerida_departamentos`;

SELECT `observacoes_sugeridas`.`id`,
    `observacoes_sugeridas`.`nome`,
    `observacoes_sugeridas`.`texto`,
    `observacoes_sugeridas`.`veiculo`,
    `observacoes_sugeridas`.`chassi`,
    `observacoes_sugeridas`.`servicos`,
    `observacoes_sugeridas`.`concessionaria`,
    `observacoes_sugeridas`.`departamento`,
    `observacoes_sugeridas`.`observacao_tipo`,
    `observacoes_sugeridas`.`concessionaria_id`,
    `observacoes_sugeridas`.`ativo`,
    `observacoes_sugeridas`.`created_at`,
    `observacoes_sugeridas`.`updated_at`,
    `observacoes_sugeridas`.`deleted_at`
FROM `smart`.`observacoes_sugeridas`;

SELECT `ocorrencia_imagens`.`id`,
    `ocorrencia_imagens`.`ocorrencia_id`,
    `ocorrencia_imagens`.`path`,
    `ocorrencia_imagens`.`indice`,
    `ocorrencia_imagens`.`created_at`,
    `ocorrencia_imagens`.`updated_at`
FROM `smart`.`ocorrencia_imagens`;

SELECT `ordem_compra_historicos`.`id`,
    `ordem_compra_historicos`.`descricao`,
    `ordem_compra_historicos`.`ordem_compra_status_original_id`,
    `ordem_compra_historicos`.`ordem_compra_status_id`,
    `ordem_compra_historicos`.`ordem_compra_id`,
    `ordem_compra_historicos`.`funcionario_id`,
    `ordem_compra_historicos`.`created_at`,
    `ordem_compra_historicos`.`updated_at`,
    `ordem_compra_historicos`.`deleted_at`
FROM `smart`.`ordem_compra_historicos`;

SELECT `ordem_compra_produtos`.`id`,
    `ordem_compra_produtos`.`quantidade`,
    `ordem_compra_produtos`.`quantidade_antecipacao`,
    `ordem_compra_produtos`.`quantidade_antecipada`,
    `ordem_compra_produtos`.`quantidade_pendente`,
    `ordem_compra_produtos`.`valor_unitario`,
    `ordem_compra_produtos`.`editado_entrega`,
    `ordem_compra_produtos`.`produto_id`,
    `ordem_compra_produtos`.`produto_tamanho_id`,
    `ordem_compra_produtos`.`tonalidade_id`,
    `ordem_compra_produtos`.`carro_modelo_id`,
    `ordem_compra_produtos`.`ordem_compra_id`,
    `ordem_compra_produtos`.`created_at`,
    `ordem_compra_produtos`.`updated_at`,
    `ordem_compra_produtos`.`deleted_at`
FROM `smart`.`ordem_compra_produtos`;

SELECT `ordem_compra_status`.`id`,
    `ordem_compra_status`.`nome`,
    `ordem_compra_status`.`created_at`,
    `ordem_compra_status`.`updated_at`,
    `ordem_compra_status`.`deleted_at`
FROM `smart`.`ordem_compra_status`;

SELECT `ordem_deposito_caixas`.`id`,
    `ordem_deposito_caixas`.`caixa_id`,
    `ordem_deposito_caixas`.`ordem_deposito_id`,
    `ordem_deposito_caixas`.`devolvido`,
    `ordem_deposito_caixas`.`data_devolucao`,
    `ordem_deposito_caixas`.`inadimplente`,
    `ordem_deposito_caixas`.`data_inadimplencia`,
    `ordem_deposito_caixas`.`recuperado`,
    `ordem_deposito_caixas`.`data_resgate`,
    `ordem_deposito_caixas`.`observacao_resgate`,
    `ordem_deposito_caixas`.`created_at`,
    `ordem_deposito_caixas`.`updated_at`,
    `ordem_deposito_caixas`.`deleted_at`
FROM `smart`.`ordem_deposito_caixas`;

SELECT `ordem_servico_servico_descontos`.`id`,
    `ordem_servico_servico_descontos`.`valor_servico`,
    `ordem_servico_servico_descontos`.`valor_desconto`,
    `ordem_servico_servico_descontos`.`observacao`,
    `ordem_servico_servico_descontos`.`os_servico_id`,
    `ordem_servico_servico_descontos`.`funcionario_id`,
    `ordem_servico_servico_descontos`.`created_at`,
    `ordem_servico_servico_descontos`.`updated_at`,
    `ordem_servico_servico_descontos`.`deleted_at`
FROM `smart`.`ordem_servico_servico_descontos`;

SELECT `ordens_compras`.`id`,
    `ordens_compras`.`proposta_compra_id`,
    `ordens_compras`.`estoque_id`,
    `ordens_compras`.`fornecedor_id`,
    `ordens_compras`.`ordem_compra_status_id`,
    `ordens_compras`.`created_at`,
    `ordens_compras`.`updated_at`,
    `ordens_compras`.`deleted_at`
FROM `smart`.`ordens_compras`;

SELECT `ordens_deposito`.`id`,
    `ordens_deposito`.`valor`,
    `ordens_deposito`.`saida`,
    `ordens_deposito`.`cancelado`,
    `ordens_deposito`.`data_cancelamento`,
    `ordens_deposito`.`justificativa_cancelamento`,
    `ordens_deposito`.`usuario_cadastro_id`,
    `ordens_deposito`.`usuario_cancelamento_id`,
    `ordens_deposito`.`factory_id`,
    `ordens_deposito`.`created_at`,
    `ordens_deposito`.`updated_at`,
    `ordens_deposito`.`deleted_at`
FROM `smart`.`ordens_deposito`;

SELECT `os`.`id`,
    `os`.`uuid`,
    `os`.`os_concessionaria`,
    `os`.`tipo_atendimento`,
    `os`.`valor_bruto`,
    `os`.`valor_liquido`,
    `os`.`retencao_iss`,
    `os`.`paga`,
    `os`.`desconto_aprovado`,
    `os`.`data_pagamento`,
    `os`.`observacao_pagamento`,
    `os`.`usuario_pagamento_id`,
    `os`.`fechada`,
    `os`.`data_fechamento`,
    `os`.`finalizada`,
    `os`.`data_finalizacao`,
    `os`.`cancelada`,
    `os`.`estornada`,
    `os`.`data_cancelamento`,
    `os`.`solicitado_cancelamento`,
    `os`.`motivo_cancelamento`,
    `os`.`cancelamento_recusado`,
    `os`.`data_recusa_cancelamento`,
    `os`.`cancelamento_motivo_id`,
    `os`.`contato_cliente_cancelamento`,
    `os`.`descricao_contato_cancelamento`,
    `os`.`os_retorno`,
    `os`.`atendimento_telefonico`,
    `os`.`nota_solicitada`,
    `os`.`nota_solicitada_motivo`,
    `os`.`data_solicitacao_nfe`,
    `os`.`nota_aprovada`,
    `os`.`data_aprovacao_nfe`,
    `os`.`usuario_aprovacao_nfe_id`,
    `os`.`cep`,
    `os`.`logradouro`,
    `os`.`bairro`,
    `os`.`localidade`,
    `os`.`uf`,
    `os`.`codigo_ibge`,
    `os`.`numero`,
    `os`.`complemento`,
    `os`.`data_entrega`,
    `os`.`data_edicao_entrega`,
    `os`.`entrega_confirmada`,
    `os`.`data_confirmacao_entrega`,
    `os`.`execucao_mesmo_dia`,
    `os`.`email_garantia_enviado`,
    `os`.`data_envio_garantia`,
    `os`.`observacao_os`,
    `os`.`observacao_producao`,
    `os`.`observacao_nf`,
    `os`.`justificada_concessionaria`,
    `os`.`desconto_Avista`,
    `os`.`confirmar_retem_iss`,
    `os`.`cortesia_migrada`,
    `os`.`data_migracao_cortesia`,
    `os`.`nome_responsavel_pj`,
    `os`.`cpf_responsavel_pj`,
    `os`.`nivel_indicador1`,
    `os`.`nivel_indicador2`,
    `os`.`indicador1_id`,
    `os`.`indicador2_id`,
    `os`.`departamento_id`,
    `os`.`vendedor_id`,
    `os`.`concessionaria_id`,
    `os`.`cliente_carro_id`,
    `os`.`cliente_id`,
    `os`.`os_tipo_id`,
    `os`.`proposta_id`,
    `os`.`pre_proposta_id`,
    `os`.`os_retorno_id`,
    `os`.`os_migracao_cortesia_id`,
    `os`.`usuario_recusa_cancelamento_id`,
    `os`.`funcionario_confirmacao_entrega_id`,
    `os`.`ativo`,
    `os`.`created_at`,
    `os`.`updated_at`,
    `os`.`deleted_at`,
    `os`.`id_antigo`,
    `os`.`usuario_atendimento_cancelamento_id`,
    `os`.`justificativa_supervisao`,
    `os`.`justificativa_supervisao_usuario_id`,
    `os`.`justificativa_supervisao_texto`
FROM `smart`.`os`;

SELECT `os_bonus_classificacoes`.`id`,
    `os_bonus_classificacoes`.`classificacao`,
    `os_bonus_classificacoes`.`os_id`,
    `os_bonus_classificacoes`.`funcionario_id`,
    `os_bonus_classificacoes`.`created_at`,
    `os_bonus_classificacoes`.`updated_at`,
    `os_bonus_classificacoes`.`deleted_at`
FROM `smart`.`os_bonus_classificacoes`;

SELECT `os_bonuses`.`id`,
    `os_bonuses`.`valor`,
    `os_bonuses`.`utilizado`,
    `os_bonuses`.`data_utilizacao`,
    `os_bonuses`.`cancelado`,
    `os_bonuses`.`data_cancelamento`,
    `os_bonuses`.`crmbonus_bonus_id`,
    `os_bonuses`.`crmbonus_campanha_id`,
    `os_bonuses`.`crmbonus_order_id`,
    `os_bonuses`.`os_id`,
    `os_bonuses`.`cliente_id`,
    `os_bonuses`.`os_utilizacao_id`,
    `os_bonuses`.`os_servico_utilizacao_id`,
    `os_bonuses`.`created_at`,
    `os_bonuses`.`updated_at`,
    `os_bonuses`.`deleted_at`
FROM `smart`.`os_bonuses`;

SELECT `os_bonus_observacoes`.`id`,
    `os_bonus_observacoes`.`observacao`,
    `os_bonus_observacoes`.`os_id`,
    `os_bonus_observacoes`.`funcionario_id`,
    `os_bonus_observacoes`.`created_at`,
    `os_bonus_observacoes`.`updated_at`,
    `os_bonus_observacoes`.`deleted_at`
FROM `smart`.`os_bonus_observacoes`;

SELECT `os_codigos_rastreio`.`id`,
    `os_codigos_rastreio`.`os_id`,
    `os_codigos_rastreio`.`codigo_rastreio`,
    `os_codigos_rastreio`.`quant_parcelas`,
    `os_codigos_rastreio`.`paga`,
    `os_codigos_rastreio`.`created_at`,
    `os_codigos_rastreio`.`updated_at`,
    `os_codigos_rastreio`.`deleted_at`
FROM `smart`.`os_codigos_rastreio`;

SELECT `os_concessionaria_alteracoes`.`id`,
    `os_concessionaria_alteracoes`.`motivo`,
    `os_concessionaria_alteracoes`.`aprovado`,
    `os_concessionaria_alteracoes`.`data_aprovacao`,
    `os_concessionaria_alteracoes`.`nivel_indicador1`,
    `os_concessionaria_alteracoes`.`nivel_indicador2`,
    `os_concessionaria_alteracoes`.`os_id`,
    `os_concessionaria_alteracoes`.`concessionaria_id`,
    `os_concessionaria_alteracoes`.`indicador1_id`,
    `os_concessionaria_alteracoes`.`indicador2_id`,
    `os_concessionaria_alteracoes`.`funcionario_requisicao_id`,
    `os_concessionaria_alteracoes`.`funcionario_aprovacao_id`,
    `os_concessionaria_alteracoes`.`created_at`,
    `os_concessionaria_alteracoes`.`updated_at`,
    `os_concessionaria_alteracoes`.`deleted_at`
FROM `smart`.`os_concessionaria_alteracoes`;

SELECT `os_historicos`.`id`,
    `os_historicos`.`descricao`,
    `os_historicos`.`os_id`,
    `os_historicos`.`funcionario_id`,
    `os_historicos`.`created_at`,
    `os_historicos`.`updated_at`,
    `os_historicos`.`deleted_at`
FROM `smart`.`os_historicos`;

SELECT `os_justificativa_pendencia`.`id`,
    `os_justificativa_pendencia`.`os_id`,
    `os_justificativa_pendencia`.`funcionario_id`,
    `os_justificativa_pendencia`.`justificativa`,
    `os_justificativa_pendencia`.`ativo`,
    `os_justificativa_pendencia`.`created_at`,
    `os_justificativa_pendencia`.`updated_at`,
    `os_justificativa_pendencia`.`deleted_at`
FROM `smart`.`os_justificativa_pendencia`;

SELECT `os_justificativas`.`id`,
    `os_justificativas`.`justificativa`,
    `os_justificativas`.`os_id`,
    `os_justificativas`.`vendedor_id`,
    `os_justificativas`.`created_at`,
    `os_justificativas`.`updated_at`,
    `os_justificativas`.`deleted_at`
FROM `smart`.`os_justificativas`;

SELECT `os_mudanca_tipo`.`id`,
    `os_mudanca_tipo`.`solicitado_por`,
    `os_mudanca_tipo`.`data_solicitado`,
    `os_mudanca_tipo`.`atendido_por`,
    `os_mudanca_tipo`.`data_atendimento`,
    `os_mudanca_tipo`.`justificativa_solicitacao`,
    `os_mudanca_tipo`.`aprovado`,
    `os_mudanca_tipo`.`recusado`,
    `os_mudanca_tipo`.`houve_estorno`,
    `os_mudanca_tipo`.`os_id`,
    `os_mudanca_tipo`.`antigo_tipo_id`,
    `os_mudanca_tipo`.`novo_tipo_id`,
    `os_mudanca_tipo`.`created_at`,
    `os_mudanca_tipo`.`updated_at`,
    `os_mudanca_tipo`.`deleted_at`
FROM `smart`.`os_mudanca_tipo`;

SELECT `os_produtos`.`id`,
    `os_produtos`.`codigo`,
    `os_produtos`.`metragem`,
    `os_produtos`.`valor_venda`,
    `os_produtos`.`valor_original`,
    `os_produtos`.`desconto_supervisao`,
    `os_produtos`.`desconto_migracao_cortesia`,
    `os_produtos`.`desconto_avista`,
    `os_produtos`.`desconto_bonus`,
    `os_produtos`.`valor_venda_real`,
    `os_produtos`.`fechado`,
    `os_produtos`.`codigo_fechamento`,
    `os_produtos`.`data_fechamento`,
    `os_produtos`.`fechado_sem_codigo`,
    `os_produtos`.`justificativa_sem_codigo`,
    `os_produtos`.`cancelado`,
    `os_produtos`.`data_cancelamento`,
    `os_produtos`.`solicitado_cancelamento`,
    `os_produtos`.`os_id`,
    `os_produtos`.`os_tipo_id`,
    `os_produtos`.`produto_id`,
    `os_produtos`.`tonalidade_id`,
    `os_produtos`.`ativo`,
    `os_produtos`.`created_at`,
    `os_produtos`.`updated_at`,
    `os_produtos`.`deleted_at`
FROM `smart`.`os_produtos`;

SELECT `os_reabertura_produtos`.`id`,
    `os_reabertura_produtos`.`cancelado`,
    `os_reabertura_produtos`.`data_cancelamento`,
    `os_reabertura_produtos`.`motivo_cancelamento`,
    `os_reabertura_produtos`.`os_reabertura_id`,
    `os_reabertura_produtos`.`os_produto_id`,
    `os_reabertura_produtos`.`created_at`,
    `os_reabertura_produtos`.`updated_at`,
    `os_reabertura_produtos`.`deleted_at`
FROM `smart`.`os_reabertura_produtos`;

SELECT `os_reaberturas`.`id`,
    `os_reaberturas`.`justificativa`,
    `os_reaberturas`.`aprovado`,
    `os_reaberturas`.`data_aprovacao`,
    `os_reaberturas`.`cancelado`,
    `os_reaberturas`.`data_cancelamento`,
    `os_reaberturas`.`motivo_cancelamento`,
    `os_reaberturas`.`os_id`,
    `os_reaberturas`.`funcionario_requisitante_id`,
    `os_reaberturas`.`funcionario_finalizacao_id`,
    `os_reaberturas`.`created_at`,
    `os_reaberturas`.`updated_at`,
    `os_reaberturas`.`deleted_at`
FROM `smart`.`os_reaberturas`;

SELECT `os_reabertura_servicos`.`id`,
    `os_reabertura_servicos`.`cancelado`,
    `os_reabertura_servicos`.`data_cancelamento`,
    `os_reabertura_servicos`.`motivo_cancelamento`,
    `os_reabertura_servicos`.`os_reabertura_id`,
    `os_reabertura_servicos`.`os_servico_id`,
    `os_reabertura_servicos`.`created_at`,
    `os_reabertura_servicos`.`updated_at`,
    `os_reabertura_servicos`.`deleted_at`
FROM `smart`.`os_reabertura_servicos`;

SELECT `os_retornos`.`id`,
    `os_retornos`.`descricao`,
    `os_retornos`.`data_solicitacao`,
    `os_retornos`.`data_aprovacao`,
    `os_retornos`.`data_recusa`,
    `os_retornos`.`os_origem_id`,
    `os_retornos`.`os_destino_id`,
    `os_retornos`.`retorno_motivo_id`,
    `os_retornos`.`retorno_classificacao_id`,
    `os_retornos`.`usuario_solicitacao_id`,
    `os_retornos`.`usuario_aprovacao_id`,
    `os_retornos`.`usuario_recusa_id`,
    `os_retornos`.`aprovado`,
    `os_retornos`.`recusado`,
    `os_retornos`.`ativo`,
    `os_retornos`.`created_at`,
    `os_retornos`.`updated_at`,
    `os_retornos`.`deleted_at`
FROM `smart`.`os_retornos`;

SELECT `os_retorno_servicos`.`id`,
    `os_retorno_servicos`.`os_retorno_id`,
    `os_retorno_servicos`.`os_servico_id`,
    `os_retorno_servicos`.`servico_id`,
    `os_retorno_servicos`.`ativo`,
    `os_retorno_servicos`.`created_at`,
    `os_retorno_servicos`.`updated_at`,
    `os_retorno_servicos`.`deleted_at`
FROM `smart`.`os_retorno_servicos`;

SELECT `os_servico_prefechamento_produtos`.`id`,
    `os_servico_prefechamento_produtos`.`os_servico_prefechamento_id`,
    `os_servico_prefechamento_produtos`.`estoque_entrada_produto_id`,
    `os_servico_prefechamento_produtos`.`ativo`,
    `os_servico_prefechamento_produtos`.`created_at`,
    `os_servico_prefechamento_produtos`.`updated_at`,
    `os_servico_prefechamento_produtos`.`deleted_at`,
    `os_servico_prefechamento_produtos`.`codigo`
FROM `smart`.`os_servico_prefechamento_produtos`;

SELECT `os_servico_prefechamentos`.`id`,
    `os_servico_prefechamentos`.`finalizado`,
    `os_servico_prefechamentos`.`data_finalizacao`,
    `os_servico_prefechamentos`.`cancelado`,
    `os_servico_prefechamentos`.`data_cancelamento`,
    `os_servico_prefechamentos`.`motivo_cancelamento`,
    `os_servico_prefechamentos`.`os_id`,
    `os_servico_prefechamentos`.`os_servico_id`,
    `os_servico_prefechamentos`.`produtivo_id`,
    `os_servico_prefechamentos`.`usuario_registro_id`,
    `os_servico_prefechamentos`.`usuario_finalizacao_id`,
    `os_servico_prefechamentos`.`usuario_cancelamento_id`,
    `os_servico_prefechamentos`.`ativo`,
    `os_servico_prefechamentos`.`created_at`,
    `os_servico_prefechamentos`.`updated_at`,
    `os_servico_prefechamentos`.`deleted_at`
FROM `smart`.`os_servico_prefechamentos`;

SELECT `os_servicos`.`id`,
    `os_servicos`.`codigo`,
    `os_servicos`.`valor_venda`,
    `os_servicos`.`valor_original`,
    `os_servicos`.`desconto_supervisao`,
    `os_servicos`.`desconto_migracao_cortesia`,
    `os_servicos`.`desconto_avista`,
    `os_servicos`.`valor_venda_real`,
    `os_servicos`.`desconto_bonus`,
    `os_servicos`.`fechado`,
    `os_servicos`.`codigo_fechamento`,
    `os_servicos`.`data_fechamento`,
    `os_servicos`.`tempo_execucao`,
    `os_servicos`.`data_inicio`,
    `os_servicos`.`fechado_sem_codigo`,
    `os_servicos`.`justificativa_sem_codigo`,
    `os_servicos`.`cancelado`,
    `os_servicos`.`data_cancelamento`,
    `os_servicos`.`solicitado_cancelamento`,
    `os_servicos`.`token_segunda_aplicacao`,
    `os_servicos`.`executada_segunda_aplicacao`,
    `os_servicos`.`ordem_pcp`,
    `os_servicos`.`os_id`,
    `os_servicos`.`os_tipo_id`,
    `os_servicos`.`servico_id`,
    `os_servicos`.`tonalidade_id`,
    `os_servicos`.`combo_id`,
    `os_servicos`.`produtivo_id`,
    `os_servicos`.`concessionaria_execucao_id`,
    `os_servicos`.`ativo`,
    `os_servicos`.`created_at`,
    `os_servicos`.`updated_at`,
    `os_servicos`.`deleted_at`,
    `os_servicos`.`plotter_corte_id`
FROM `smart`.`os_servicos`;

SELECT `os_servicos_historicos`.`id`,
    `os_servicos_historicos`.`os_servico_id`,
    `os_servicos_historicos`.`os_id`,
    `os_servicos_historicos`.`funcionario_id`,
    `os_servicos_historicos`.`tipo`,
    `os_servicos_historicos`.`descricao`,
    `os_servicos_historicos`.`created_at`,
    `os_servicos_historicos`.`updated_at`,
    `os_servicos_historicos`.`deleted_at`
FROM `smart`.`os_servicos_historicos`;

SELECT `os_servicos_lembrete_carro_modelos`.`id`,
    `os_servicos_lembrete_carro_modelos`.`lembrete_id`,
    `os_servicos_lembrete_carro_modelos`.`carro_modelo_id`,
    `os_servicos_lembrete_carro_modelos`.`ativo`,
    `os_servicos_lembrete_carro_modelos`.`created_at`,
    `os_servicos_lembrete_carro_modelos`.`updated_at`,
    `os_servicos_lembrete_carro_modelos`.`deleted_at`
FROM `smart`.`os_servicos_lembrete_carro_modelos`;

SELECT `os_servicos_lembrete_concessionarias`.`id`,
    `os_servicos_lembrete_concessionarias`.`lembrete_id`,
    `os_servicos_lembrete_concessionarias`.`concessionaria_id`,
    `os_servicos_lembrete_concessionarias`.`ativo`,
    `os_servicos_lembrete_concessionarias`.`created_at`,
    `os_servicos_lembrete_concessionarias`.`updated_at`,
    `os_servicos_lembrete_concessionarias`.`deleted_at`
FROM `smart`.`os_servicos_lembrete_concessionarias`;

SELECT `os_servicos_lembretes`.`id`,
    `os_servicos_lembretes`.`texto`,
    `os_servicos_lembretes`.`ativo`,
    `os_servicos_lembretes`.`created_at`,
    `os_servicos_lembretes`.`updated_at`,
    `os_servicos_lembretes`.`deleted_at`
FROM `smart`.`os_servicos_lembretes`;

SELECT `os_servicos_lembrete_servicos`.`id`,
    `os_servicos_lembrete_servicos`.`lembrete_id`,
    `os_servicos_lembrete_servicos`.`servico_id`,
    `os_servicos_lembrete_servicos`.`ativo`,
    `os_servicos_lembrete_servicos`.`created_at`,
    `os_servicos_lembrete_servicos`.`updated_at`,
    `os_servicos_lembrete_servicos`.`deleted_at`
FROM `smart`.`os_servicos_lembrete_servicos`;

SELECT `os_tipos`.`id`,
    `os_tipos`.`nome`,
    `os_tipos`.`ativo`,
    `os_tipos`.`created_at`,
    `os_tipos`.`updated_at`,
    `os_tipos`.`deleted_at`
FROM `smart`.`os_tipos`;

SELECT `pcp_agendamento_alteracoes`.`id`,
    `pcp_agendamento_alteracoes`.`motivo`,
    `pcp_agendamento_alteracoes`.`data_entrega`,
    `pcp_agendamento_alteracoes`.`aprovado`,
    `pcp_agendamento_alteracoes`.`data_aprovacao`,
    `pcp_agendamento_alteracoes`.`pcp_agendamento_id`,
    `pcp_agendamento_alteracoes`.`funcionario_alteracao_id`,
    `pcp_agendamento_alteracoes`.`funcionario_aprovacao_id`,
    `pcp_agendamento_alteracoes`.`created_at`,
    `pcp_agendamento_alteracoes`.`updated_at`,
    `pcp_agendamento_alteracoes`.`deleted_at`
FROM `smart`.`pcp_agendamento_alteracoes`;

SELECT `pcp_agendamentos`.`id`,
    `pcp_agendamentos`.`data_agendamento`,
    `pcp_agendamentos`.`execucao_mesmo_dia`,
    `pcp_agendamentos`.`finalizado`,
    `pcp_agendamentos`.`data_finalizacao`,
    `pcp_agendamentos`.`vencido`,
    `pcp_agendamentos`.`data_vencimento`,
    `pcp_agendamentos`.`observacao`,
    `pcp_agendamentos`.`recusado`,
    `pcp_agendamentos`.`concessionaria_execucao_id`,
    `pcp_agendamentos`.`produtivo_id`,
    `pcp_agendamentos`.`os_servico_id`,
    `pcp_agendamentos`.`funcionario_agendamento_id`,
    `pcp_agendamentos`.`funcionario_finalizacao_id`,
    `pcp_agendamentos`.`created_at`,
    `pcp_agendamentos`.`updated_at`,
    `pcp_agendamentos`.`deleted_at`
FROM `smart`.`pcp_agendamentos`;

SELECT `pix_respostas`.`id`,
    `pix_respostas`.`tx_id`,
    `pix_respostas`.`conteudo`,
    `pix_respostas`.`verificado`,
    `pix_respostas`.`created_at`,
    `pix_respostas`.`updated_at`,
    `pix_respostas`.`deleted_at`
FROM `smart`.`pix_respostas`;

SELECT `plotter_bobinas`.`id`,
    `plotter_bobinas`.`codigo`,
    `plotter_bobinas`.`metros`,
    `plotter_bobinas`.`recuperacao`,
    `plotter_bobinas`.`finalizada`,
    `plotter_bobinas`.`data_finalizacao`,
    `plotter_bobinas`.`cancelada`,
    `plotter_bobinas`.`data_cancelamento`,
    `plotter_bobinas`.`solicitado_cancelamento`,
    `plotter_bobinas`.`estoque_entrada_produto_id`,
    `plotter_bobinas`.`estoque_saida_produto_id`,
    `plotter_bobinas`.`estoque_id`,
    `plotter_bobinas`.`ativo`,
    `plotter_bobinas`.`created_at`,
    `plotter_bobinas`.`updated_at`,
    `plotter_bobinas`.`deleted_at`
FROM `smart`.`plotter_bobinas`;

SELECT `plotter_corte_pecas`.`id`,
    `plotter_corte_pecas`.`plotter_corte_id`,
    `plotter_corte_pecas`.`plotter_peca_id`,
    `plotter_corte_pecas`.`ativo`,
    `plotter_corte_pecas`.`created_at`,
    `plotter_corte_pecas`.`updated_at`,
    `plotter_corte_pecas`.`deleted_at`
FROM `smart`.`plotter_corte_pecas`;

SELECT `plotter_cortes`.`id`,
    `plotter_cortes`.`codigo`,
    `plotter_cortes`.`codigo_antigo`,
    `plotter_cortes`.`metragem_total`,
    `plotter_cortes`.`metragem`,
    `plotter_cortes`.`recuperacao`,
    `plotter_cortes`.`finalizado`,
    `plotter_cortes`.`data_finalizacao`,
    `plotter_cortes`.`solicitado_cancelamento`,
    `plotter_cortes`.`data_solicitacao_cancelamento`,
    `plotter_cortes`.`motivo_cancelamento`,
    `plotter_cortes`.`cancelado`,
    `plotter_cortes`.`data_cancelamento`,
    `plotter_cortes`.`duas_portas`,
    `plotter_cortes`.`liberado`,
    `plotter_cortes`.`data_liberacao`,
    `plotter_cortes`.`concessionaria_liberacao_id`,
    `plotter_cortes`.`justificativa`,
    `plotter_cortes`.`credito`,
    `plotter_cortes`.`usuario_finalizacao_id`,
    `plotter_cortes`.`usuario_solicitacao_cancelamento_id`,
    `plotter_cortes`.`usuario_cancelamento_id`,
    `plotter_cortes`.`usuario_liberacao_id`,
    `plotter_cortes`.`metragem_secundaria`,
    `plotter_cortes`.`metragem_vidros_traseiros`,
    `plotter_cortes`.`metragem_vidros_frontais`,
    `plotter_cortes`.`metragem_parabrisa`,
    `plotter_cortes`.`plotter_bobina_secundaria_id`,
    `plotter_cortes`.`plotter_bobina_vidros_traseiros_id`,
    `plotter_cortes`.`plotter_bobina_vidros_frontais_id`,
    `plotter_cortes`.`plotter_corte_parabrisa_id`,
    `plotter_cortes`.`plotter_corte_tipo_id`,
    `plotter_cortes`.`carro_modelo_id`,
    `plotter_cortes`.`plotter_bobina_id`,
    `plotter_cortes`.`os_servico_id`,
    `plotter_cortes`.`os_produto_id`,
    `plotter_cortes`.`estoque_id`,
    `plotter_cortes`.`user_recuperacao_id`,
    `plotter_cortes`.`ativo`,
    `plotter_cortes`.`created_by`,
    `plotter_cortes`.`created_at`,
    `plotter_cortes`.`updated_at`,
    `plotter_cortes`.`deleted_at`
FROM `smart`.`plotter_cortes`;

SELECT `plotter_corte_tipos`.`id`,
    `plotter_corte_tipos`.`nome`,
    `plotter_corte_tipos`.`ativo`,
    `plotter_corte_tipos`.`created_at`,
    `plotter_corte_tipos`.`updated_at`,
    `plotter_corte_tipos`.`deleted_at`
FROM `smart`.`plotter_corte_tipos`;

SELECT `plotter_devolucao_cortes`.`id`,
    `plotter_devolucao_cortes`.`plotter_devolucao_id`,
    `plotter_devolucao_cortes`.`plotter_corte_id`,
    `plotter_devolucao_cortes`.`created_at`,
    `plotter_devolucao_cortes`.`updated_at`,
    `plotter_devolucao_cortes`.`deleted_at`
FROM `smart`.`plotter_devolucao_cortes`;

SELECT `plotter_devolucoes`.`id`,
    `plotter_devolucoes`.`justificativa`,
    `plotter_devolucoes`.`funcionario_devolucao_id`,
    `plotter_devolucoes`.`created_at`,
    `plotter_devolucoes`.`updated_at`,
    `plotter_devolucoes`.`deleted_at`
FROM `smart`.`plotter_devolucoes`;

SELECT `plotter_estoques_programados`.`id`,
    `plotter_estoques_programados`.`minimo`,
    `plotter_estoques_programados`.`maximo`,
    `plotter_estoques_programados`.`credito_minimo`,
    `plotter_estoques_programados`.`credito_maximo`,
    `plotter_estoques_programados`.`tipo_estoque`,
    `plotter_estoques_programados`.`produto_id`,
    `plotter_estoques_programados`.`tonalidade_id`,
    `plotter_estoques_programados`.`plotter_corte_tipo_id`,
    `plotter_estoques_programados`.`plotter_peca_id`,
    `plotter_estoques_programados`.`concessionaria_id`,
    `plotter_estoques_programados`.`estoque_id`,
    `plotter_estoques_programados`.`carro_modelo_id`,
    `plotter_estoques_programados`.`created_at`,
    `plotter_estoques_programados`.`updated_at`,
    `plotter_estoques_programados`.`deleted_at`
FROM `smart`.`plotter_estoques_programados`;

SELECT `plotter_metragens`.`id`,
    `plotter_metragens`.`metragem`,
    `plotter_metragens`.`metragem_sem_vidro_traseiro`,
    `plotter_metragens`.`carro_modelo_id`,
    `plotter_metragens`.`produto_id`,
    `plotter_metragens`.`tonalidade_id`,
    `plotter_metragens`.`funcionario_id`,
    `plotter_metragens`.`created_at`,
    `plotter_metragens`.`updated_at`,
    `plotter_metragens`.`deleted_at`
FROM `smart`.`plotter_metragens`;

SELECT `plotter_pecas`.`id`,
    `plotter_pecas`.`nome`,
    `plotter_pecas`.`credito_necessario`,
    `plotter_pecas`.`ativo`,
    `plotter_pecas`.`created_at`,
    `plotter_pecas`.`updated_at`,
    `plotter_pecas`.`deleted_at`,
    `plotter_pecas`.`plotter_corte_tipo_id`,
    `plotter_pecas`.`servico_id`
FROM `smart`.`plotter_pecas`;

SELECT `plotter_saida_corte_pecas`.`id`,
    `plotter_saida_corte_pecas`.`plotter_saida_corte_id`,
    `plotter_saida_corte_pecas`.`plotter_peca_id`,
    `plotter_saida_corte_pecas`.`created_at`,
    `plotter_saida_corte_pecas`.`updated_at`,
    `plotter_saida_corte_pecas`.`deleted_at`
FROM `smart`.`plotter_saida_corte_pecas`;

SELECT `plotter_saida_cortes`.`id`,
    `plotter_saida_cortes`.`duas_portas`,
    `plotter_saida_cortes`.`credito_minimo`,
    `plotter_saida_cortes`.`credito_maximo`,
    `plotter_saida_cortes`.`ano_modelo`,
    `plotter_saida_cortes`.`cancelado`,
    `plotter_saida_cortes`.`data_cancelamento`,
    `plotter_saida_cortes`.`motivo_cancelamento`,
    `plotter_saida_cortes`.`plotter_corte_tipo_id`,
    `plotter_saida_cortes`.`plotter_peca_id`,
    `plotter_saida_cortes`.`carro_modelo_id`,
    `plotter_saida_cortes`.`produto_id`,
    `plotter_saida_cortes`.`tonalidade_id`,
    `plotter_saida_cortes`.`produto_traseiro_id`,
    `plotter_saida_cortes`.`tonalidade_traseiro_id`,
    `plotter_saida_cortes`.`produto_dianteiro_id`,
    `plotter_saida_cortes`.`tonalidade_dianteiro_id`,
    `plotter_saida_cortes`.`plotter_saida_id`,
    `plotter_saida_cortes`.`plotter_corte_id`,
    `plotter_saida_cortes`.`os_servico_id`,
    `plotter_saida_cortes`.`os_produto_id`,
    `plotter_saida_cortes`.`created_at`,
    `plotter_saida_cortes`.`updated_at`,
    `plotter_saida_cortes`.`deleted_at`
FROM `smart`.`plotter_saida_cortes`;

SELECT `plotter_saida_historicos`.`id`,
    `plotter_saida_historicos`.`descricao`,
    `plotter_saida_historicos`.`plotter_saida_id`,
    `plotter_saida_historicos`.`plotter_saida_status_id`,
    `plotter_saida_historicos`.`funcionario_registro_id`,
    `plotter_saida_historicos`.`created_at`,
    `plotter_saida_historicos`.`updated_at`,
    `plotter_saida_historicos`.`deleted_at`
FROM `smart`.`plotter_saida_historicos`;

SELECT `plotter_saidas`.`id`,
    `plotter_saidas`.`observacao`,
    `plotter_saidas`.`cancelada`,
    `plotter_saidas`.`data_cancelamento`,
    `plotter_saidas`.`solicitado_cancelamento`,
    `plotter_saidas`.`motivo_cancelamento`,
    `plotter_saidas`.`funcionario_registro_id`,
    `plotter_saidas`.`plotter_saida_tipo_id`,
    `plotter_saidas`.`plotter_saida_status_id`,
    `plotter_saidas`.`concessionaria_id`,
    `plotter_saidas`.`concessionaria_execucao_id`,
    `plotter_saidas`.`os_id`,
    `plotter_saidas`.`created_at`,
    `plotter_saidas`.`updated_at`,
    `plotter_saidas`.`deleted_at`
FROM `smart`.`plotter_saidas`;

SELECT `plotter_saida_status`.`id`,
    `plotter_saida_status`.`nome`,
    `plotter_saida_status`.`created_at`,
    `plotter_saida_status`.`updated_at`,
    `plotter_saida_status`.`deleted_at`
FROM `smart`.`plotter_saida_status`;

SELECT `plotter_saida_tipos`.`id`,
    `plotter_saida_tipos`.`nome`,
    `plotter_saida_tipos`.`created_at`,
    `plotter_saida_tipos`.`updated_at`,
    `plotter_saida_tipos`.`deleted_at`
FROM `smart`.`plotter_saida_tipos`;

SELECT `plotter_vencimento_kits`.`id`,
    `plotter_vencimento_kits`.`vencimento`,
    `plotter_vencimento_kits`.`produto_id`,
    `plotter_vencimento_kits`.`created_at`,
    `plotter_vencimento_kits`.`updated_at`,
    `plotter_vencimento_kits`.`deleted_at`
FROM `smart`.`plotter_vencimento_kits`;

SELECT `ponto_registro_marcacoes`.`id`,
    `ponto_registro_marcacoes`.`data`,
    `ponto_registro_marcacoes`.`motivo`,
    `ponto_registro_marcacoes`.`funcionario_id`,
    `ponto_registro_marcacoes`.`empresa_id`,
    `ponto_registro_marcacoes`.`ponto_registro_id`,
    `ponto_registro_marcacoes`.`created_at`,
    `ponto_registro_marcacoes`.`updated_at`,
    `ponto_registro_marcacoes`.`deleted_at`
FROM `smart`.`ponto_registro_marcacoes`;

SELECT `ponto_registros`.`id`,
    `ponto_registros`.`periodo`,
    `ponto_registros`.`tipo`,
    `ponto_registros`.`empresa_id`,
    `ponto_registros`.`funcionario_registro_id`,
    `ponto_registros`.`created_at`,
    `ponto_registros`.`updated_at`,
    `ponto_registros`.`deleted_at`
FROM `smart`.`ponto_registros`;

SELECT `pos_venda_ticket_historicos`.`id`,
    `pos_venda_ticket_historicos`.`pos_venda_ticket_id`,
    `pos_venda_ticket_historicos`.`responsavel_id`,
    `pos_venda_ticket_historicos`.`observacao`,
    `pos_venda_ticket_historicos`.`status`,
    `pos_venda_ticket_historicos`.`created_at`,
    `pos_venda_ticket_historicos`.`updated_at`,
    `pos_venda_ticket_historicos`.`deleted_at`
FROM `smart`.`pos_venda_ticket_historicos`;

SELECT `pos_venda_tickets`.`id`,
    `pos_venda_tickets`.`nome_solicitante`,
    `pos_venda_tickets`.`telefone_solicitante`,
    `pos_venda_tickets`.`descricao_curta`,
    `pos_venda_tickets`.`os_origem`,
    `pos_venda_tickets`.`categoria`,
    `pos_venda_tickets`.`servicos`,
    `pos_venda_tickets`.`descricao`,
    `pos_venda_tickets`.`vendedor_id`,
    `pos_venda_tickets`.`concessionaria_id`,
    `pos_venda_tickets`.`created_at`,
    `pos_venda_tickets`.`updated_at`,
    `pos_venda_tickets`.`deleted_at`
FROM `smart`.`pos_venda_tickets`;

SELECT `pre_proposta_cancelamento_motivos`.`id`,
    `pre_proposta_cancelamento_motivos`.`nome`,
    `pre_proposta_cancelamento_motivos`.`ativo`,
    `pre_proposta_cancelamento_motivos`.`created_at`,
    `pre_proposta_cancelamento_motivos`.`updated_at`,
    `pre_proposta_cancelamento_motivos`.`deleted_at`
FROM `smart`.`pre_proposta_cancelamento_motivos`;

SELECT `pre_proposta_historicos`.`id`,
    `pre_proposta_historicos`.`estorno`,
    `pre_proposta_historicos`.`sucesso`,
    `pre_proposta_historicos`.`request_body`,
    `pre_proposta_historicos`.`response`,
    `pre_proposta_historicos`.`pre_proposta_id`,
    `pre_proposta_historicos`.`os_id`,
    `pre_proposta_historicos`.`created_at`,
    `pre_proposta_historicos`.`updated_at`,
    `pre_proposta_historicos`.`deleted_at`
FROM `smart`.`pre_proposta_historicos`;

SELECT `pre_propostas`.`id`,
    `pre_propostas`.`cancelada`,
    `pre_propostas`.`data_cancelamento`,
    `pre_propostas`.`solicitado_cancelamento`,
    `pre_propostas`.`data_solicitacao_cancelamento`,
    `pre_propostas`.`motivo_cancelamento`,
    `pre_propostas`.`finalizada`,
    `pre_propostas`.`data_finalizacao`,
    `pre_propostas`.`proposta_carbel`,
    `pre_propostas`.`empresa_carbel`,
    `pre_propostas`.`nome`,
    `pre_propostas`.`cpf`,
    `pre_propostas`.`data_nascimento`,
    `pre_propostas`.`email`,
    `pre_propostas`.`telefone1`,
    `pre_propostas`.`telefone2`,
    `pre_propostas`.`cep`,
    `pre_propostas`.`logradouro`,
    `pre_propostas`.`bairro`,
    `pre_propostas`.`localidade`,
    `pre_propostas`.`uf`,
    `pre_propostas`.`codigo_ibge`,
    `pre_propostas`.`numero`,
    `pre_propostas`.`complemento`,
    `pre_propostas`.`vendedor`,
    `pre_propostas`.`descricao_veiculo`,
    `pre_propostas`.`descricao_veiculo_completa`,
    `pre_propostas`.`descricao_estoque`,
    `pre_propostas`.`chassi`,
    `pre_propostas`.`placa`,
    `pre_propostas`.`pre_proposta_cancelamento_motivo_id`,
    `pre_propostas`.`concessionaria_id`,
    `pre_propostas`.`departamento_id`,
    `pre_propostas`.`carro_marca_id`,
    `pre_propostas`.`carro_modelo_id`,
    `pre_propostas`.`carro_cor_id`,
    `pre_propostas`.`funcionario_solicitacao_cancelamento_id`,
    `pre_propostas`.`funcionario_aprovacao_cancelamento_id`,
    `pre_propostas`.`created_at`,
    `pre_propostas`.`updated_at`,
    `pre_propostas`.`deleted_at`
FROM `smart`.`pre_propostas`;

SELECT `produtividade_periodos`.`id`,
    `produtividade_periodos`.`ano`,
    `produtividade_periodos`.`mes`,
    `produtividade_periodos`.`dias_uteis`,
    `produtividade_periodos`.`created_at`,
    `produtividade_periodos`.`updated_at`
FROM `smart`.`produtividade_periodos`;

SELECT `produtivo_bases`.`id`,
    `produtivo_bases`.`nome`,
    `produtivo_bases`.`ativo`,
    `produtivo_bases`.`created_at`,
    `produtivo_bases`.`updated_at`,
    `produtivo_bases`.`deleted_at`
FROM `smart`.`produtivo_bases`;

SELECT `produtivo_tipos`.`id`,
    `produtivo_tipos`.`nome`,
    `produtivo_tipos`.`master`,
    `produtivo_tipos`.`ativo`,
    `produtivo_tipos`.`created_at`,
    `produtivo_tipos`.`updated_at`,
    `produtivo_tipos`.`deleted_at`
FROM `smart`.`produtivo_tipos`;

SELECT `produtivo_tipo_servicos`.`id`,
    `produtivo_tipo_servicos`.`produtivo_tipo_id`,
    `produtivo_tipo_servicos`.`servico_id`,
    `produtivo_tipo_servicos`.`ativo`,
    `produtivo_tipo_servicos`.`created_at`,
    `produtivo_tipo_servicos`.`updated_at`,
    `produtivo_tipo_servicos`.`deleted_at`
FROM `smart`.`produtivo_tipo_servicos`;

SELECT `produto_concessionaria_estoques`.`id`,
    `produto_concessionaria_estoques`.`estoque_minimo`,
    `produto_concessionaria_estoques`.`estoque_maximo`,
    `produto_concessionaria_estoques`.`concessionaria_id`,
    `produto_concessionaria_estoques`.`produto_id`,
    `produto_concessionaria_estoques`.`produto_tamanho_id`,
    `produto_concessionaria_estoques`.`created_at`,
    `produto_concessionaria_estoques`.`updated_at`,
    `produto_concessionaria_estoques`.`deleted_at`
FROM `smart`.`produto_concessionaria_estoques`;

SELECT `produto_configuracoes_estoque`.`id`,
    `produto_configuracoes_estoque`.`estoque_minimo`,
    `produto_configuracoes_estoque`.`estoque_maximo`,
    `produto_configuracoes_estoque`.`ativo`,
    `produto_configuracoes_estoque`.`produto_id`,
    `produto_configuracoes_estoque`.`produto_tamanho_id`,
    `produto_configuracoes_estoque`.`tonalidade_id`,
    `produto_configuracoes_estoque`.`created_at`,
    `produto_configuracoes_estoque`.`updated_at`,
    `produto_configuracoes_estoque`.`deleted_at`
FROM `smart`.`produto_configuracoes_estoque`;

SELECT `produto_nota_configuracoes`.`id`,
    `produto_nota_configuracoes`.`descricao`,
    `produto_nota_configuracoes`.`ncm`,
    `produto_nota_configuracoes`.`cfop`,
    `produto_nota_configuracoes`.`cfop_saida`,
    `produto_nota_configuracoes`.`cest`,
    `produto_nota_configuracoes`.`cst_ibs_cbs`,
    `produto_nota_configuracoes`.`cclasstrib_ibs_cbs`,
    `produto_nota_configuracoes`.`medida_venda`,
    `produto_nota_configuracoes`.`substituicao_tributaria`,
    `produto_nota_configuracoes`.`produto_id`,
    `produto_nota_configuracoes`.`empresa_id`,
    `produto_nota_configuracoes`.`medida_id`,
    `produto_nota_configuracoes`.`updated_by`,
    `produto_nota_configuracoes`.`ativo`,
    `produto_nota_configuracoes`.`created_at`,
    `produto_nota_configuracoes`.`updated_at`,
    `produto_nota_configuracoes`.`deleted_at`,
    `produto_nota_configuracoes`.`tipo_nota`
FROM `smart`.`produto_nota_configuracoes`;

SELECT `produtos`.`id`,
    `produtos`.`nome`,
    `produtos`.`codigo`,
    `produtos`.`envio_maximo`,
    `produtos`.`fracionavel`,
    `produtos`.`fracao_rastreavel`,
    `produtos`.`rastreavel`,
    `produtos`.`fecha_servico`,
    `produtos`.`fecha_kit`,
    `produtos`.`fecha_peca_avulsa`,
    `produtos`.`fecha_peca`,
    `produtos`.`fecha_produto`,
    `produtos`.`diferencia_tonalidade`,
    `produtos`.`diferencia_modelo`,
    `produtos`.`diferencia_tamanho`,
    `produtos`.`permite_venda`,
    `produtos`.`medida_id`,
    `produtos`.`grupo_produto_id`,
    `produtos`.`subgrupo_produto_id`,
    `produtos`.`produto_parabrisa_id`,
    `produtos`.`ativo`,
    `produtos`.`created_at`,
    `produtos`.`updated_at`,
    `produtos`.`deleted_at`
FROM `smart`.`produtos`;

SELECT `produto_tamanhos`.`id`,
    `produto_tamanhos`.`quantidade`,
    `produto_tamanhos`.`estoque_minimo`,
    `produto_tamanhos`.`estoque_maximo`,
    `produto_tamanhos`.`produto_id`,
    `produto_tamanhos`.`ativo`,
    `produto_tamanhos`.`created_at`,
    `produto_tamanhos`.`updated_at`,
    `produto_tamanhos`.`deleted_at`
FROM `smart`.`produto_tamanhos`;

SELECT `produto_tonalidades`.`id`,
    `produto_tonalidades`.`produto_id`,
    `produto_tonalidades`.`tonalidade_id`,
    `produto_tonalidades`.`created_at`,
    `produto_tonalidades`.`updated_at`,
    `produto_tonalidades`.`deleted_at`
FROM `smart`.`produto_tonalidades`;

SELECT `proposta_compra_produtos`.`id`,
    `proposta_compra_produtos`.`quantidade`,
    `proposta_compra_produtos`.`produto_id`,
    `proposta_compra_produtos`.`produto_tamanho_id`,
    `proposta_compra_produtos`.`tonalidade_id`,
    `proposta_compra_produtos`.`proposta_compra_id`,
    `proposta_compra_produtos`.`created_at`,
    `proposta_compra_produtos`.`updated_at`,
    `proposta_compra_produtos`.`deleted_at`
FROM `smart`.`proposta_compra_produtos`;

SELECT `propostas`.`id`,
    `propostas`.`proposta_concessionaria`,
    `propostas`.`tipo_atendimento`,
    `propostas`.`nome`,
    `propostas`.`sexo`,
    `propostas`.`telefone1`,
    `propostas`.`telefone2`,
    `propostas`.`email`,
    `propostas`.`atendimento_telefonico`,
    `propostas`.`justificativa`,
    `propostas`.`cancelamento_motivo_id`,
    `propostas`.`vendedor_id`,
    `propostas`.`concessionaria_id`,
    `propostas`.`departamento_id`,
    `propostas`.`cliente_id`,
    `propostas`.`cliente_carro_id`,
    `propostas`.`proposta_status_id`,
    `propostas`.`carro_modelo_id`,
    `propostas`.`carro_submodelo_id`,
    `propostas`.`carro_cor_id`,
    `propostas`.`pre_proposta_id`,
    `propostas`.`ativo`,
    `propostas`.`created_at`,
    `propostas`.`updated_at`,
    `propostas`.`deleted_at`
FROM `smart`.`propostas`;

SELECT `propostas_compras`.`id`,
    `propostas_compras`.`finalizada`,
    `propostas_compras`.`data_finalizacao`,
    `propostas_compras`.`funcionario_finalizacao_id`,
    `propostas_compras`.`estoque_id`,
    `propostas_compras`.`fornecedor_id`,
    `propostas_compras`.`created_at`,
    `propostas_compras`.`updated_at`,
    `propostas_compras`.`deleted_at`
FROM `smart`.`propostas_compras`;

SELECT `proposta_servicos`.`id`,
    `proposta_servicos`.`valor_venda`,
    `proposta_servicos`.`valor_original`,
    `proposta_servicos`.`desconto_supervisao`,
    `proposta_servicos`.`cancelado`,
    `proposta_servicos`.`data_cancelamento`,
    `proposta_servicos`.`motivo_cancelamento`,
    `proposta_servicos`.`proposta_id`,
    `proposta_servicos`.`servico_id`,
    `proposta_servicos`.`combo_id`,
    `proposta_servicos`.`tonalidade_id`,
    `proposta_servicos`.`ativo`,
    `proposta_servicos`.`created_at`,
    `proposta_servicos`.`updated_at`,
    `proposta_servicos`.`deleted_at`
FROM `smart`.`proposta_servicos`;

SELECT `proposta_status`.`id`,
    `proposta_status`.`nome`,
    `proposta_status`.`ativo`,
    `proposta_status`.`created_at`,
    `proposta_status`.`updated_at`,
    `proposta_status`.`deleted_at`
FROM `smart`.`proposta_status`;

SELECT `refund_events`.`id`,
    `refund_events`.`estorno_id`,
    `refund_events`.`event_type`,
    `refund_events`.`actor_type`,
    `refund_events`.`actor_id`,
    `refund_events`.`actor_name`,
    `refund_events`.`payload`,
    `refund_events`.`created_at`
FROM `smart`.`refund_events`;

SELECT `refund_reason_codes`.`id`,
    `refund_reason_codes`.`created_at`,
    `refund_reason_codes`.`updated_at`,
    `refund_reason_codes`.`deleted_at`,
    `refund_reason_codes`.`code`,
    `refund_reason_codes`.`display_name`,
    `refund_reason_codes`.`category`,
    `refund_reason_codes`.`active`
FROM `smart`.`refund_reason_codes`;

SELECT `regions`.`id`,
    `regions`.`nome`,
    `regions`.`ativo`,
    `regions`.`created_at`,
    `regions`.`updated_at`,
    `regions`.`deleted_at`
FROM `smart`.`regions`;

SELECT `relatorio_filtros`.`id`,
    `relatorio_filtros`.`relatorio`,
    `relatorio_filtros`.`ref`,
    `relatorio_filtros`.`filtros`,
    `relatorio_filtros`.`funcionario_id`,
    `relatorio_filtros`.`created_at`,
    `relatorio_filtros`.`updated_at`,
    `relatorio_filtros`.`deleted_at`
FROM `smart`.`relatorio_filtros`;

SELECT `remessa_historico_remocao_os`.`id`,
    `remessa_historico_remocao_os`.`justificativa`,
    `remessa_historico_remocao_os`.`funcionario_id`,
    `remessa_historico_remocao_os`.`os_id`,
    `remessa_historico_remocao_os`.`remessa_id`,
    `remessa_historico_remocao_os`.`created_at`,
    `remessa_historico_remocao_os`.`updated_at`,
    `remessa_historico_remocao_os`.`deleted_at`
FROM `smart`.`remessa_historico_remocao_os`;

SELECT `remessa_os`.`os_id`,
    `remessa_os`.`remessa_id`,
    `remessa_os`.`valor_pagamento`,
    `remessa_os`.`usuario_agendamento`,
    `remessa_os`.`data_agendamento`,
    `remessa_os`.`pago`,
    `remessa_os`.`codigo_deposito`,
    `remessa_os`.`id`,
    `remessa_os`.`data_pagamento`,
    `remessa_os`.`remessa_lote_id`,
    `remessa_os`.`created_at`,
    `remessa_os`.`updated_at`,
    `remessa_os`.`deleted_at`
FROM `smart`.`remessa_os`;

SELECT `remessa_os_lotes`.`id`,
    `remessa_os_lotes`.`valor_depositado`,
    `remessa_os_lotes`.`usuario_criacao`,
    `remessa_os_lotes`.`tipo_remessa_id`,
    `remessa_os_lotes`.`caixa_conta_id`,
    `remessa_os_lotes`.`concessionaria_id`,
    `remessa_os_lotes`.`created_at`,
    `remessa_os_lotes`.`updated_at`,
    `remessa_os_lotes`.`deleted_at`
FROM `smart`.`remessa_os_lotes`;

SELECT `remessas`.`id`,
    `remessas`.`usuario_criacao`,
    `remessas`.`tipo_remessa_id`,
    `remessas`.`concessionaria_id`,
    `remessas`.`cancelamento_motivo`,
    `remessas`.`solicitado_cancelamento`,
    `remessas`.`data_solicitacao_cancelamento`,
    `remessas`.`solicitado_por`,
    `remessas`.`cancelada`,
    `remessas`.`data_cancelamento`,
    `remessas`.`atendido_por`,
    `remessas`.`email_enviado`,
    `remessas`.`created_at`,
    `remessas`.`updated_at`,
    `remessas`.`deleted_at`
FROM `smart`.`remessas`;

SELECT `retorno_classificacoes`.`id`,
    `retorno_classificacoes`.`nome`,
    `retorno_classificacoes`.`subgrupo_servico_id`,
    `retorno_classificacoes`.`ativo`,
    `retorno_classificacoes`.`created_at`,
    `retorno_classificacoes`.`updated_at`,
    `retorno_classificacoes`.`deleted_at`
FROM `smart`.`retorno_classificacoes`;

SELECT `retorno_motivos`.`id`,
    `retorno_motivos`.`titulo`,
    `retorno_motivos`.`aprovacao_supervisao`,
    `retorno_motivos`.`estorna_comissao_antiga`,
    `retorno_motivos`.`gera_nova_comissao`,
    `retorno_motivos`.`ativo`,
    `retorno_motivos`.`created_at`,
    `retorno_motivos`.`updated_at`,
    `retorno_motivos`.`deleted_at`
FROM `smart`.`retorno_motivos`;

SELECT `ronda_classificacoes`.`id`,
    `ronda_classificacoes`.`nome`,
    `ronda_classificacoes`.`created_at`,
    `ronda_classificacoes`.`updated_at`,
    `ronda_classificacoes`.`deleted_at`
FROM `smart`.`ronda_classificacoes`;

SELECT `ronda_etapas`.`id`,
    `ronda_etapas`.`descricao`,
    `ronda_etapas`.`resposta_positiva`,
    `ronda_etapas`.`ordem`,
    `ronda_etapas`.`ronda_classificacao_id`,
    `ronda_etapas`.`created_at`,
    `ronda_etapas`.`updated_at`,
    `ronda_etapas`.`deleted_at`
FROM `smart`.`ronda_etapas`;

SELECT `ronda_execucao_respostas`.`id`,
    `ronda_execucao_respostas`.`resposta`,
    `ronda_execucao_respostas`.`observacao`,
    `ronda_execucao_respostas`.`ronda_execucao_id`,
    `ronda_execucao_respostas`.`ronda_classificacao_id`,
    `ronda_execucao_respostas`.`ronda_etapa_id`,
    `ronda_execucao_respostas`.`created_at`,
    `ronda_execucao_respostas`.`updated_at`,
    `ronda_execucao_respostas`.`deleted_at`
FROM `smart`.`ronda_execucao_respostas`;

SELECT `ronda_execucoes`.`id`,
    `ronda_execucoes`.`data_previsao`,
    `ronda_execucoes`.`finalizada`,
    `ronda_execucoes`.`data_finalizacao`,
    `ronda_execucoes`.`ronda_rotina_id`,
    `ronda_execucoes`.`concessionaria_id`,
    `ronda_execucoes`.`funcionario_responsavel_id`,
    `ronda_execucoes`.`created_at`,
    `ronda_execucoes`.`updated_at`,
    `ronda_execucoes`.`deleted_at`
FROM `smart`.`ronda_execucoes`;

SELECT `ronda_rotina_classificacoes`.`id`,
    `ronda_rotina_classificacoes`.`ronda_rotina_id`,
    `ronda_rotina_classificacoes`.`ronda_classificacao_id`,
    `ronda_rotina_classificacoes`.`created_at`,
    `ronda_rotina_classificacoes`.`updated_at`,
    `ronda_rotina_classificacoes`.`deleted_at`
FROM `smart`.`ronda_rotina_classificacoes`;

SELECT `ronda_rotina_concessionarias`.`id`,
    `ronda_rotina_concessionarias`.`ronda_rotina_id`,
    `ronda_rotina_concessionarias`.`concessionaria_id`,
    `ronda_rotina_concessionarias`.`created_at`,
    `ronda_rotina_concessionarias`.`updated_at`,
    `ronda_rotina_concessionarias`.`deleted_at`
FROM `smart`.`ronda_rotina_concessionarias`;

SELECT `ronda_rotinas`.`id`,
    `ronda_rotinas`.`data_inicio`,
    `ronda_rotinas`.`periodicidade`,
    `ronda_rotinas`.`observacao`,
    `ronda_rotinas`.`funcionario_responsavel_id`,
    `ronda_rotinas`.`created_at`,
    `ronda_rotinas`.`updated_at`,
    `ronda_rotinas`.`deleted_at`
FROM `smart`.`ronda_rotinas`;

SELECT `servico_categorias`.`id`,
    `servico_categorias`.`nome`,
    `servico_categorias`.`ativo`,
    `servico_categorias`.`created_at`,
    `servico_categorias`.`updated_at`,
    `servico_categorias`.`deleted_at`
FROM `smart`.`servico_categorias`;

SELECT `servico_departamentos`.`id`,
    `servico_departamentos`.`servico_id`,
    `servico_departamentos`.`servico_acessorio_id`,
    `servico_departamentos`.`acessorio_restringe_execucao`,
    `servico_departamentos`.`departamento_id`,
    `servico_departamentos`.`ativo`,
    `servico_departamentos`.`created_at`,
    `servico_departamentos`.`updated_at`,
    `servico_departamentos`.`deleted_at`
FROM `smart`.`servico_departamentos`;

SELECT `servico_execucao_tempos`.`id`,
    `servico_execucao_tempos`.`tempo_execucao`,
    `servico_execucao_tempos`.`servico_id`,
    `servico_execucao_tempos`.`departamento_id`,
    `servico_execucao_tempos`.`carro_cor_tipo_id`,
    `servico_execucao_tempos`.`carro_porte_id`,
    `servico_execucao_tempos`.`created_at`,
    `servico_execucao_tempos`.`updated_at`,
    `servico_execucao_tempos`.`deleted_at`
FROM `smart`.`servico_execucao_tempos`;

SELECT `servico_garantias`.`id`,
    `servico_garantias`.`texto`,
    `servico_garantias`.`prazo`,
    `servico_garantias`.`prazo_tipo`,
    `servico_garantias`.`servico_id`,
    `servico_garantias`.`durabilidade`,
    `servico_garantias`.`created_at`,
    `servico_garantias`.`updated_at`,
    `servico_garantias`.`deleted_at`
FROM `smart`.`servico_garantias`;

SELECT `servico_nota_configuracoes`.`id`,
    `servico_nota_configuracoes`.`descricao`,
    `servico_nota_configuracoes`.`ncm`,
    `servico_nota_configuracoes`.`cfop`,
    `servico_nota_configuracoes`.`cfop_saida`,
    `servico_nota_configuracoes`.`cest`,
    `servico_nota_configuracoes`.`cst_ibs_cbs`,
    `servico_nota_configuracoes`.`cclasstrib_ibs_cbs`,
    `servico_nota_configuracoes`.`cindop`,
    `servico_nota_configuracoes`.`tipo_nota`,
    `servico_nota_configuracoes`.`porcentagem_emissao`,
    `servico_nota_configuracoes`.`medida_venda`,
    `servico_nota_configuracoes`.`substituicao_tributaria`,
    `servico_nota_configuracoes`.`servico_id`,
    `servico_nota_configuracoes`.`empresa_id`,
    `servico_nota_configuracoes`.`medida_id`,
    `servico_nota_configuracoes`.`ativo`,
    `servico_nota_configuracoes`.`created_at`,
    `servico_nota_configuracoes`.`updated_at`,
    `servico_nota_configuracoes`.`updated_by`,
    `servico_nota_configuracoes`.`deleted_at`
FROM `smart`.`servico_nota_configuracoes`;

SELECT `servico_ocorrencia`.`id`,
    `servico_ocorrencia`.`os_id`,
    `servico_ocorrencia`.`servico_id`,
    `servico_ocorrencia`.`produtivo_id`,
    `servico_ocorrencia`.`tipo`,
    `servico_ocorrencia`.`observacao`,
    `servico_ocorrencia`.`created_at`,
    `servico_ocorrencia`.`updated_at`
FROM `smart`.`servico_ocorrencia`;

SELECT `servico_produto_departamentos`.`id`,
    `servico_produto_departamentos`.`servico_produto_id`,
    `servico_produto_departamentos`.`departamento_id`,
    `servico_produto_departamentos`.`ativo`,
    `servico_produto_departamentos`.`created_at`,
    `servico_produto_departamentos`.`updated_at`,
    `servico_produto_departamentos`.`deleted_at`
FROM `smart`.`servico_produto_departamentos`;

SELECT `servico_produto_portes`.`id`,
    `servico_produto_portes`.`servico_produto_id`,
    `servico_produto_portes`.`carro_porte_id`,
    `servico_produto_portes`.`created_at`,
    `servico_produto_portes`.`updated_at`,
    `servico_produto_portes`.`deleted_at`
FROM `smart`.`servico_produto_portes`;

SELECT `servico_produtos`.`id`,
    `servico_produtos`.`alternavel`,
    `servico_produtos`.`filtro_cor`,
    `servico_produtos`.`filtro_departamento`,
    `servico_produtos`.`servico_id`,
    `servico_produtos`.`produto_id`,
    `servico_produtos`.`ativo`,
    `servico_produtos`.`created_at`,
    `servico_produtos`.`updated_at`,
    `servico_produtos`.`deleted_at`
FROM `smart`.`servico_produtos`;

SELECT `servicos`.`id`,
    `servicos`.`nome`,
    `servicos`.`custo_fixo`,
    `servicos`.`codigo_nf`,
    `servicos`.`fecha_kit`,
    `servicos`.`fecha_peca_avulsa`,
    `servicos`.`fecha_peca`,
    `servicos`.`fecha_produto`,
    `servicos`.`fecha_produtivo`,
    `servicos`.`diferencia_departamento_preco`,
    `servicos`.`diferencia_porte`,
    `servicos`.`diferencia_departamento`,
    `servicos`.`diferencia_porte_comissao`,
    `servicos`.`diferencia_tempo_departamento`,
    `servicos`.`diferencia_tempo_cor`,
    `servicos`.`credito_necessario`,
    `servicos`.`valor_desconto_cortesia`,
    `servicos`.`aceita_desconto_cortesia`,
    `servicos`.`segunda_aplicacao`,
    `servicos`.`grupo_servico_id`,
    `servicos`.`subgrupo_servico_id`,
    `servicos`.`servico_categoria_id`,
    `servicos`.`tags`,
    `servicos`.`ativo`,
    `servicos`.`created_at`,
    `servicos`.`updated_at`,
    `servicos`.`deleted_at`
FROM `smart`.`servicos`;

SELECT `subgrupos_produtos`.`id`,
    `subgrupos_produtos`.`nome`,
    `subgrupos_produtos`.`grupo_produto_id`,
    `subgrupos_produtos`.`ativo`,
    `subgrupos_produtos`.`created_at`,
    `subgrupos_produtos`.`updated_at`,
    `subgrupos_produtos`.`deleted_at`
FROM `smart`.`subgrupos_produtos`;

SELECT `subgrupos_servicos`.`id`,
    `subgrupos_servicos`.`nome`,
    `subgrupos_servicos`.`sigla`,
    `subgrupos_servicos`.`grupo_servico_id`,
    `subgrupos_servicos`.`ativo`,
    `subgrupos_servicos`.`created_at`,
    `subgrupos_servicos`.`updated_at`,
    `subgrupos_servicos`.`deleted_at`
FROM `smart`.`subgrupos_servicos`;

SELECT `tabela_comissao_produtos`.`id`,
    `tabela_comissao_produtos`.`valor_dentro`,
    `tabela_comissao_produtos`.`valor_fora`,
    `tabela_comissao_produtos`.`porcentagem`,
    `tabela_comissao_produtos`.`indicador_tipo_id`,
    `tabela_comissao_produtos`.`produto_id`,
    `tabela_comissao_produtos`.`tabela_comissao_id`,
    `tabela_comissao_produtos`.`funcionario_cadastro_id`,
    `tabela_comissao_produtos`.`ativo`,
    `tabela_comissao_produtos`.`created_at`,
    `tabela_comissao_produtos`.`updated_at`,
    `tabela_comissao_produtos`.`deleted_at`
FROM `smart`.`tabela_comissao_produtos`;

SELECT `tabela_comissao_servicos`.`id`,
    `tabela_comissao_servicos`.`valor_dentro`,
    `tabela_comissao_servicos`.`valor_fora`,
    `tabela_comissao_servicos`.`porcentagem`,
    `tabela_comissao_servicos`.`departamento_id`,
    `tabela_comissao_servicos`.`carro_porte_id`,
    `tabela_comissao_servicos`.`indicador_tipo_id`,
    `tabela_comissao_servicos`.`servico_id`,
    `tabela_comissao_servicos`.`funcionario_cadastro_id`,
    `tabela_comissao_servicos`.`tabela_comissao_id`,
    `tabela_comissao_servicos`.`ativo`,
    `tabela_comissao_servicos`.`created_at`,
    `tabela_comissao_servicos`.`updated_at`,
    `tabela_comissao_servicos`.`deleted_at`
FROM `smart`.`tabela_comissao_servicos`;

SELECT `tabela_comissao_tipos`.`id`,
    `tabela_comissao_tipos`.`nome`,
    `tabela_comissao_tipos`.`tipo_contrato`,
    `tabela_comissao_tipos`.`ordem`,
    `tabela_comissao_tipos`.`ativo`,
    `tabela_comissao_tipos`.`created_at`,
    `tabela_comissao_tipos`.`updated_at`,
    `tabela_comissao_tipos`.`deleted_at`
FROM `smart`.`tabela_comissao_tipos`;

SELECT `tabela_preco_produtos`.`id`,
    `tabela_preco_produtos`.`valor_maximo_venda`,
    `tabela_preco_produtos`.`valor_minimo_venda`,
    `tabela_preco_produtos`.`valor_nfe`,
    `tabela_preco_produtos`.`produto_id`,
    `tabela_preco_produtos`.`funcionario_cadastro_id`,
    `tabela_preco_produtos`.`tabela_preco_id`,
    `tabela_preco_produtos`.`ativo`,
    `tabela_preco_produtos`.`created_at`,
    `tabela_preco_produtos`.`updated_at`,
    `tabela_preco_produtos`.`deleted_at`
FROM `smart`.`tabela_preco_produtos`;

SELECT `tabela_preco_servicos`.`id`,
    `tabela_preco_servicos`.`valor_maximo_venda`,
    `tabela_preco_servicos`.`valor_minimo_venda`,
    `tabela_preco_servicos`.`valor_nfe`,
    `tabela_preco_servicos`.`servico_id`,
    `tabela_preco_servicos`.`combo_id`,
    `tabela_preco_servicos`.`carro_porte_id`,
    `tabela_preco_servicos`.`departamento_id`,
    `tabela_preco_servicos`.`funcionario_cadastro_id`,
    `tabela_preco_servicos`.`tabela_preco_id`,
    `tabela_preco_servicos`.`ativo`,
    `tabela_preco_servicos`.`created_at`,
    `tabela_preco_servicos`.`updated_at`,
    `tabela_preco_servicos`.`deleted_at`
FROM `smart`.`tabela_preco_servicos`;

SELECT `tabelas_comissoes`.`id`,
    `tabelas_comissoes`.`nome`,
    `tabelas_comissoes`.`tabela_comissao_tipo_id`,
    `tabelas_comissoes`.`ativo`,
    `tabelas_comissoes`.`created_at`,
    `tabelas_comissoes`.`updated_at`,
    `tabelas_comissoes`.`deleted_at`
FROM `smart`.`tabelas_comissoes`;

SELECT `tabelas_precos`.`id`,
    `tabelas_precos`.`nome`,
    `tabelas_precos`.`ativo`,
    `tabelas_precos`.`created_at`,
    `tabelas_precos`.`updated_at`,
    `tabelas_precos`.`deleted_at`
FROM `smart`.`tabelas_precos`;

SELECT `telas`.`id`,
    `telas`.`nome`,
    `telas`.`url`,
    `telas`.`rota`,
    `telas`.`ordem`,
    `telas`.`icone`,
    `telas`.`controller`,
    `telas`.`parametros`,
    `telas`.`exibir_menu`,
    `telas`.`v3`,
    `telas`.`parente`,
    `telas`.`modulo_id`,
    `telas`.`ativo`,
    `telas`.`created_at`,
    `telas`.`updated_at`,
    `telas`.`deleted_at`
FROM `smart`.`telas`;

SELECT `tipo_remessa_concessionarias`.`id`,
    `tipo_remessa_concessionarias`.`concessionaria_id`,
    `tipo_remessa_concessionarias`.`tipo_remessa_id`,
    `tipo_remessa_concessionarias`.`created_at`,
    `tipo_remessa_concessionarias`.`updated_at`,
    `tipo_remessa_concessionarias`.`deleted_at`
FROM `smart`.`tipo_remessa_concessionarias`;

SELECT `tipo_remessas`.`id`,
    `tipo_remessas`.`nome`,
    `tipo_remessas`.`ativo`,
    `tipo_remessas`.`created_at`,
    `tipo_remessas`.`updated_at`,
    `tipo_remessas`.`deleted_at`
FROM `smart`.`tipo_remessas`;

SELECT `tonalidades`.`id`,
    `tonalidades`.`nome`,
    `tonalidades`.`ativo`,
    `tonalidades`.`created_at`,
    `tonalidades`.`updated_at`,
    `tonalidades`.`deleted_at`
FROM `smart`.`tonalidades`;

SELECT `transportadoras`.`id`,
    `transportadoras`.`nome`,
    `transportadoras`.`razao_social`,
    `transportadoras`.`cnpj`,
    `transportadoras`.`ie`,
    `transportadoras`.`im`,
    `transportadoras`.`telefone1`,
    `transportadoras`.`telefone2`,
    `transportadoras`.`email`,
    `transportadoras`.`ativo`,
    `transportadoras`.`created_at`,
    `transportadoras`.`updated_at`,
    `transportadoras`.`deleted_at`
FROM `smart`.`transportadoras`;

SELECT `unique_requests`.`id`,
    `unique_requests`.`request_id`,
    `unique_requests`.`route`,
    `unique_requests`.`payload`,
    `unique_requests`.`user_id`,
    `unique_requests`.`created_at`,
    `unique_requests`.`updated_at`
FROM `smart`.`unique_requests`;

SELECT `usuario_acessos`.`id`,
    `usuario_acessos`.`ip`,
    `usuario_acessos`.`localidade`,
    `usuario_acessos`.`detalhes`,
    `usuario_acessos`.`sucesso`,
    `usuario_acessos`.`observacao`,
    `usuario_acessos`.`usuario_id`,
    `usuario_acessos`.`created_at`,
    `usuario_acessos`.`updated_at`,
    `usuario_acessos`.`deleted_at`
FROM `smart`.`usuario_acessos`;

SELECT `usuarios`.`id`,
    `usuarios`.`login`,
    `usuarios`.`password`,
    `usuarios`.`funcionario_id`,
    `usuarios`.`mc_user_id`,
    `usuarios`.`grupo_usuario_id`,
    `usuarios`.`bloqueio_justificativa`,
    `usuarios`.`gestor_antecipacao`,
    `usuarios`.`ativo`,
    `usuarios`.`created_at`,
    `usuarios`.`updated_at`,
    `usuarios`.`deleted_at`,
    `usuarios`.`bloqueio`
FROM `smart`.`usuarios`;

SELECT `venda_meta_departamentos`.`id`,
    `venda_meta_departamentos`.`departamento_id`,
    `venda_meta_departamentos`.`venda_meta_id`,
    `venda_meta_departamentos`.`created_at`,
    `venda_meta_departamentos`.`updated_at`,
    `venda_meta_departamentos`.`deleted_at`
FROM `smart`.`venda_meta_departamentos`;

SELECT `venda_meta_historicos`.`id`,
    `venda_meta_historicos`.`descricao`,
    `venda_meta_historicos`.`venda_meta_id`,
    `venda_meta_historicos`.`funcionario_registro_id`,
    `venda_meta_historicos`.`created_at`,
    `venda_meta_historicos`.`updated_at`,
    `venda_meta_historicos`.`deleted_at`
FROM `smart`.`venda_meta_historicos`;

SELECT `venda_meta_meses`.`id`,
    `venda_meta_meses`.`mes_referencia`,
    `venda_meta_meses`.`valor_meta`,
    `venda_meta_meses`.`porcentagem_minima_meta`,
    `venda_meta_meses`.`porcentagem_minima_recebimento`,
    `venda_meta_meses`.`venda_meta_id`,
    `venda_meta_meses`.`created_at`,
    `venda_meta_meses`.`updated_at`,
    `venda_meta_meses`.`deleted_at`
FROM `smart`.`venda_meta_meses`;

SELECT `venda_meta_os_tipos`.`id`,
    `venda_meta_os_tipos`.`venda_meta_id`,
    `venda_meta_os_tipos`.`os_tipo_id`,
    `venda_meta_os_tipos`.`created_at`,
    `venda_meta_os_tipos`.`updated_at`,
    `venda_meta_os_tipos`.`deleted_at`
FROM `smart`.`venda_meta_os_tipos`;

SELECT `venda_metas`.`id`,
    `venda_metas`.`ano_referencia`,
    `venda_metas`.`concessionaria_id`,
    `venda_metas`.`funcionario_cadastro_id`,
    `venda_metas`.`vendedor_treinador_id`,
    `venda_metas`.`vendedor_id`,
    `venda_metas`.`valor_premiacao_recebimento`,
    `venda_metas`.`porcentagem_minima_recebimento`,
    `venda_metas`.`valor_premiacao_dvu`,
    `venda_metas`.`valor_meta_dvu`,
    `venda_metas`.`valor_premiacao_dvn`,
    `venda_metas`.`valor_meta_dvn`,
    `venda_metas`.`valor_meta_frotista`,
    `venda_metas`.`valor_premiacao_frotista`,
    `venda_metas`.`valor_meta_oficina`,
    `venda_metas`.`valor_premiacao_oficina`,
    `venda_metas`.`validade`,
    `venda_metas`.`periodo`,
    `venda_metas`.`created_at`,
    `venda_metas`.`updated_at`,
    `venda_metas`.`deleted_at`
FROM `smart`.`venda_metas`;

SELECT `vinculo_comissao_permuta_itens`.`id`,
    `vinculo_comissao_permuta_itens`.`vinculo_id`,
    `vinculo_comissao_permuta_itens`.`comissao_id`,
    `vinculo_comissao_permuta_itens`.`caixa_pendente_id`,
    `vinculo_comissao_permuta_itens`.`caixa_id`,
    `vinculo_comissao_permuta_itens`.`valor`,
    `vinculo_comissao_permuta_itens`.`created_at`,
    `vinculo_comissao_permuta_itens`.`updated_at`
FROM `smart`.`vinculo_comissao_permuta_itens`;

SELECT `vinculos_comissao_permuta`.`id`,
    `vinculos_comissao_permuta`.`comissionado_id`,
    `vinculos_comissao_permuta`.`usuario_id`,
    `vinculos_comissao_permuta`.`valor_total`,
    `vinculos_comissao_permuta`.`created_at`,
    `vinculos_comissao_permuta`.`updated_at`
FROM `smart`.`vinculos_comissao_permuta`;

SELECT `vr_cartoes`.`id`,
    `vr_cartoes`.`numero`,
    `vr_cartoes`.`valor_dia`,
    `vr_cartoes`.`desconto_dia`,
    `vr_cartoes`.`cancelado`,
    `vr_cartoes`.`data_cancelamento`,
    `vr_cartoes`.`justificativa_cancelamento`,
    `vr_cartoes`.`observacao`,
    `vr_cartoes`.`funcionario_id`,
    `vr_cartoes`.`empresa_id`,
    `vr_cartoes`.`vr_tipo_id`,
    `vr_cartoes`.`ativo`,
    `vr_cartoes`.`created_at`,
    `vr_cartoes`.`updated_at`,
    `vr_cartoes`.`deleted_at`
FROM `smart`.`vr_cartoes`;

SELECT `vr_historicos`.`id`,
    `vr_historicos`.`detalhes`,
    `vr_historicos`.`funcionario_id`,
    `vr_historicos`.`vr_cartao_id`,
    `vr_historicos`.`created_at`,
    `vr_historicos`.`updated_at`,
    `vr_historicos`.`deleted_at`
FROM `smart`.`vr_historicos`;

SELECT `vr_pagamento_lancamentos`.`id`,
    `vr_pagamento_lancamentos`.`valor_dia`,
    `vr_pagamento_lancamentos`.`desconto_dia`,
    `vr_pagamento_lancamentos`.`dias_uteis`,
    `vr_pagamento_lancamentos`.`valor_total`,
    `vr_pagamento_lancamentos`.`desconto_total`,
    `vr_pagamento_lancamentos`.`valor_total_real`,
    `vr_pagamento_lancamentos`.`justificativa`,
    `vr_pagamento_lancamentos`.`funcionario_id`,
    `vr_pagamento_lancamentos`.`vr_pagamento_id`,
    `vr_pagamento_lancamentos`.`vr_cartao_id`,
    `vr_pagamento_lancamentos`.`created_at`,
    `vr_pagamento_lancamentos`.`updated_at`,
    `vr_pagamento_lancamentos`.`deleted_at`
FROM `smart`.`vr_pagamento_lancamentos`;

SELECT `vr_pagamentos`.`id`,
    `vr_pagamentos`.`periodo`,
    `vr_pagamentos`.`dias_uteis`,
    `vr_pagamentos`.`valor_total`,
    `vr_pagamentos`.`desconto_total`,
    `vr_pagamentos`.`valor_total_real`,
    `vr_pagamentos`.`empresa_id`,
    `vr_pagamentos`.`vr_tipo_id`,
    `vr_pagamentos`.`avulso`,
    `vr_pagamentos`.`created_at`,
    `vr_pagamentos`.`updated_at`,
    `vr_pagamentos`.`deleted_at`
FROM `smart`.`vr_pagamentos`;

SELECT `vr_tipos`.`id`,
    `vr_tipos`.`nome`,
    `vr_tipos`.`descricao`,
    `vr_tipos`.`ativo`,
    `vr_tipos`.`created_at`,
    `vr_tipos`.`updated_at`,
    `vr_tipos`.`deleted_at`
FROM `smart`.`vr_tipos`;

SELECT `vt_cartoes`.`id`,
    `vt_cartoes`.`numero`,
    `vt_cartoes`.`empresa_id`,
    `vt_cartoes`.`vt_tipo_id`,
    `vt_cartoes`.`ativo`,
    `vt_cartoes`.`created_at`,
    `vt_cartoes`.`updated_at`,
    `vt_cartoes`.`deleted_at`
FROM `smart`.`vt_cartoes`;

SELECT `vt_historicos`.`id`,
    `vt_historicos`.`detalhes`,
    `vt_historicos`.`funcionario_id`,
    `vt_historicos`.`vt_cartao_id`,
    `vt_historicos`.`created_at`,
    `vt_historicos`.`updated_at`,
    `vt_historicos`.`deleted_at`
FROM `smart`.`vt_historicos`;

SELECT `vt_pagamento_lancamentos`.`id`,
    `vt_pagamento_lancamentos`.`passes_dia`,
    `vt_pagamento_lancamentos`.`valor_passe`,
    `vt_pagamento_lancamentos`.`saldo_atual`,
    `vt_pagamento_lancamentos`.`valor_defasagem`,
    `vt_pagamento_lancamentos`.`recarga_sem_monitoria`,
    `vt_pagamento_lancamentos`.`recarga_com_monitoria`,
    `vt_pagamento_lancamentos`.`valor_nf`,
    `vt_pagamento_lancamentos`.`justificativa`,
    `vt_pagamento_lancamentos`.`funcionario_id`,
    `vt_pagamento_lancamentos`.`vt_pagamento_id`,
    `vt_pagamento_lancamentos`.`vt_cartao_id`,
    `vt_pagamento_lancamentos`.`created_at`,
    `vt_pagamento_lancamentos`.`updated_at`,
    `vt_pagamento_lancamentos`.`deleted_at`
FROM `smart`.`vt_pagamento_lancamentos`;

SELECT `vt_pagamentos`.`id`,
    `vt_pagamentos`.`periodo`,
    `vt_pagamentos`.`dias_uteis`,
    `vt_pagamentos`.`dias_defasagem`,
    `vt_pagamentos`.`total_sem_monitoria`,
    `vt_pagamentos`.`total_com_monitoria`,
    `vt_pagamentos`.`total_nf`,
    `vt_pagamentos`.`avulso`,
    `vt_pagamentos`.`empresa_id`,
    `vt_pagamentos`.`vt_tipo_id`,
    `vt_pagamentos`.`created_at`,
    `vt_pagamentos`.`updated_at`,
    `vt_pagamentos`.`deleted_at`
FROM `smart`.`vt_pagamentos`;

SELECT `vt_tipos`.`id`,
    `vt_tipos`.`nome`,
    `vt_tipos`.`ativo`,
    `vt_tipos`.`created_at`,
    `vt_tipos`.`updated_at`,
    `vt_tipos`.`deleted_at`
FROM `smart`.`vt_tipos`;
