# Dashboard

Interface visual construída com Streamlit, conectada diretamente ao PostgreSQL.

## Estrutura

```
dashboard/
├── app.py        # aplicação principal — 4 abas
└── queries.py    # queries SQL e conexão com PostgreSQL
```

## Abas

| Aba | Conteúdo |
|---|---|
| Visão Geral | 8 KPIs do ano atual + histórico completo |
| Evolução | gráfico de linha por indicador |
| Comparações | SELIC × IPCA × Taxa Real e SELIC × CDI |
| Assistente IA | chat em linguagem natural com AI SQL Agent |

## KPIs exibidos

| KPI | Fonte | Cálculo |
|---|---|---|
| Taxa SELIC | `gold_selic_anual.ultimo_selic` | último valor diário do ano |
| CDI | `gold_cdi_anual.ultimo_cdi` | último valor diário do ano |
| Dólar | `gold_cambio_anual.ultimo_cambio` | última cotação do ano |
| Classificação SELIC | `mart_selic_anual` | Alta / Moderada / Baixa |
| IPCA Acumulado no Ano | `gold_ipca_anual.ipca_acumulado` | juros compostos dos meses do ano |
| IPCA Acumulado 12M | `gold_ipca_12m.ipca_12m` | juros compostos dos últimos 12 meses |
| Taxa Real (Ano) | `gold_taxa_real_anual.taxa_real` | SELIC - IPCA acumulado no ano |
| Taxa Real (12M) | calculado na query | SELIC - IPCA 12 meses |

## Como rodar

```bash
docker compose up -d streamlit
```

Acesse em `http://localhost:8501`