# Airflow

Orquestração do pipeline de dados com Apache Airflow.

## Estrutura

```
airflow/
└── dags/
    └── bcb_pipeline.py
```

## Pipeline

```
bronze_layer → silver_layer → gold_layer → load_postgres → dbt_run → dbt_test
```

| Task | Comando | Descrição |
|---|---|---|
| `bronze_layer` | `python3 -m processing.bronze_layer` | API BCB → Parquet |
| `silver_layer` | `python3 -m processing.silver_layer` | Parquet → Delta Lake |
| `gold_layer` | `python3 -m processing.gold_layer` | Delta Lake → agregações |
| `load_postgres` | `python3 -m storage.postgres_loader` | Delta Lake → PostgreSQL |
| `dbt_run` | `dbt run --profiles-dir /app/bcb_dbt` | cria views analíticas |
| `dbt_test` | `dbt test --profiles-dir /app/bcb_dbt` | valida qualidade |

## Configurações

- Agendamento: `@daily`
- Retries: 3
- Alertas: Telegram via n8n em caso de falha ou sucesso

## Como acessar

```
http://localhost:8081
usuário: admin
senha:   admin
```

## Como disparar manualmente

```bash
docker exec -it airflow-bcb bash -c "airflow dags trigger bcb_lakehouse_pipeline"
```