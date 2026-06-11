# Processing

Camadas Bronze, Silver e Gold do pipeline Medallion.

## Estrutura

```
processing/
├── spark_session.py    # SparkSession com Delta Lake, PostgreSQL e Kafka
├── bronze_layer.py     # API BCB → Parquet
├── silver_layer.py     # Parquet → Delta Lake limpo
├── gold_layer.py       # Delta Lake → agregações analíticas
└── quality_checks.py   # validação de DataFrames
```

## Pipeline

```
bronze_layer → silver_layer → gold_layer
```

## Transformações por camada

**Bronze** — dados brutos da API BCB salvos como Parquet sem transformação.

**Silver** — limpeza e tipagem:
- `data`: string → DateType
- `valor`: string → DoubleType
- SELIC e CDI: anualização por juros compostos `((1 + taxa/100)^252 - 1) * 100`

**Gold** — agregações analíticas por ano:

| Tabela | Campos | Cálculo |
|---|---|---|
| `selic_anual` | media, max, min, ultimo_selic | último valor diário do ano |
| `ipca_anual` | media_ipca, ipca_acumulado | acumulado por juros compostos |
| `ipca_12m` | ipca_12m | juros compostos dos últimos 12 meses |
| `cambio_anual` | media, max, min, ultimo_cambio | último valor diário do ano |
| `cdi_anual` | media_cdi, ultimo_cdi | último valor diário do ano |
| `taxa_real_anual` | taxa_real | ultimo_selic - ipca_acumulado |