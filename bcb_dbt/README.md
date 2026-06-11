# BCB dbt

Modelagem analítica, testes de qualidade e documentação automática.

## Estrutura

```
bcb_dbt/
├── models/
│   ├── staging/
│   │   ├── sources.yml
│   │   ├── stg_selic_anual.sql
│   │   ├── stg_ipca_anual.sql
│   │   ├── stg_cambio_anual.sql
│   │   └── stg_cdi_anual.sql
│   └── marts/
│       ├── mart_selic_anual.sql
│       └── mart_indicadores_anual.sql
└── profiles.yml
```

## Lineage

```
public.gold_* (tabelas brutas do PostgreSQL)
        ↓
analytics.stg_* (padronização e arredondamento)
        ↓
analytics.mart_* (modelo analítico final)
```

## Testes

| Teste | Modelo | Coluna |
|---|---|---|
| `unique` | `stg_selic_anual` | `ano` |
| `not_null` | `stg_selic_anual` | `ano`, `media_selic` |
| `unique` | `mart_selic_anual` | `ano` |
| `not_null` | `mart_selic_anual` | `ano` |
| `accepted_values` | `mart_selic_anual` | `classificacao_selic` |

## Como rodar

```bash
docker exec -it airflow-bcb bash
cd /app/bcb_dbt
dbt run --profiles-dir /app/bcb_dbt
dbt test --profiles-dir /app/bcb_dbt
dbt docs generate --profiles-dir /app/bcb_dbt
```