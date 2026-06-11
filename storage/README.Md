# Storage

Carga dos dados da camada Gold para o PostgreSQL.

## Estrutura

```
storage/
├── postgres_loader.py    # Gold (Delta Lake) → PostgreSQL via JDBC
└── database.py           # utilitários de conexão
```

## Por que DELETE em vez de TRUNCATE

O dbt cria views no schema `analytics` que dependem das tabelas Gold no schema `public`. O PostgreSQL não permite `TRUNCATE` em tabelas com objetos dependentes sem `CASCADE` — que derrubaria as views. O `DELETE` limpa os dados sem afetar a estrutura, preservando as views do dbt.

## Fluxo

```
Gold (Delta Lake) → DELETE tabela → INSERT via JDBC → PostgreSQL
```

## Por que o truncate falhava silenciosamente antes

O `DB_CONFIG` usava `os.getenv("DB_HOST", "localhost")` mas o `JDBC_URL` estava hardcoded como `postgres-bcb`. Quando o container do Airflow não tinha `DB_HOST` definido, o `truncate_table` conectava em `localhost` (inexistente no Docker), falhava, e o `except` silencioso escondia o erro. O `append` acumulava duplicatas a cada run. O fix foi centralizar tudo no `config/settings.py` e garantir `DB_HOST=postgres-bcb` no `docker-compose.yml`.

## Tabelas carregadas

| Tabela | Fonte | Conteúdo |
|---|---|---|
| `gold_selic_anual` | `gold/selic_anual` | média, max, min, último valor diário |
| `gold_ipca_anual` | `gold/ipca_anual` | média mensal, acumulado por juros compostos |
| `gold_ipca_12m` | `gold/ipca_12m` | IPCA acumulado últimos 12 meses |
| `gold_cambio_anual` | `gold/cambio_anual` | média, max, min, último valor diário |
| `gold_cdi_anual` | `gold/cdi_anual` | média, último valor diário |
| `gold_taxa_real_anual` | `gold/taxa_real_anual` | SELIC - IPCA acumulado |

## Como rodar

```bash
docker exec -it airflow-bcb bash
cd /app
python3 -m storage.postgres_loader
```