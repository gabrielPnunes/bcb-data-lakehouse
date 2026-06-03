# BCB Data Lakehouse

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white
)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-E25A1C?style=flat&logo=apachespark&logoColor=white
)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-3.2-003366?style=flat&logo=delta&logoColor=whit
)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9-017CEE?style=flat&logo=apacheairflow&logoColor=white
)
![dbt](https://img.shields.io/badge/dbt-1.11-FF694B?style=flat&logo=dbt&logoColor=white
)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white
)
![Docker](https://img.shields.io/badge/Docker-blue?style=flat&logo=docker&logoColor=white
)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white
)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white
)

Pipeline moderno de engenharia de dados construído sobre indicadores econômicos do Banco Central do Brasil.

## Visão Geral

Projeto end-to-end de engenharia de dados que ingere, processa e disponibiliza indicadores econômicos do BCB em uma arquitetura Lakehouse moderna com orquestração, qualidade de dados, modelagem analítica e dashboard interativo.

## Arquitetura

```
API BCB
   │
   ▼
Bronze Layer (Parquet)
   │
   ▼
Silver Layer (Delta Lake) ── transformações e limpeza
   │
   ▼
Gold Layer (Delta Lake) ── agregações analíticas
   │
   ▼
PostgreSQL ── carga via JDBC
   │
   ▼
dbt ── modelagem, testes e documentação
   │
   ▼
Streamlit ── dashboard interativo
```

O pipeline completo é orquestrado pelo Apache Airflow com execução diária automática.

## Stack

### Data Engineering
| Tecnologia | Uso |
|---|---|
| Python | linguagem principal |
| Apache Spark / PySpark | processamento distribuído |
| Delta Lake | formato de armazenamento ACID |
| Apache Airflow | orquestração do pipeline |
| dbt | modelagem e testes SQL |
| PostgreSQL | banco analítico |
| Docker | containerização |

### Visualização
| Tecnologia | Uso |
|---|---|
| Streamlit | dashboard interativo |
| Plotly | gráficos |

## Estrutura do Projeto

```
bcb-data-lakehouse/
│
├── airflow/
│   └── dags/               # DAGs do Airflow
│
├── bcb_dbt/                # projeto dbt
│   └── models/
│       ├── staging/        # camada staging
│       └── marts/          # camada analítica
│
├── dashboard/              # aplicação Streamlit
│
├── docker/                 # infraestrutura Docker
│   ├── airflow/
│   ├── spark/
│   └── streamlit/
│
├── ingestion/              # scripts de ingestão da API BCB
│
├── processing/             # camadas Bronze, Silver e Gold
│
├── storage/                # carga para PostgreSQL
│
├── utils/                  # utilitários compartilhados
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Pipeline

```
bronze_layer → silver_layer → gold_layer → load_postgres → dbt_run → dbt_test
```

| Task | Descrição |
|---|---|
| `bronze_layer` | ingere CSV da API BCB e salva em Parquet |
| `silver_layer` | limpa, tipifica e anualiza a taxa SELIC |
| `gold_layer` | agrega média anual por ano |
| `load_postgres` | carrega Gold no PostgreSQL via JDBC |
| `dbt_run` | executa models staging e marts |
| `dbt_test` | valida qualidade dos dados |

## Como Rodar

### Pré-requisitos

- Docker Desktop
- Python 3.12+
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/gabrielPnunes/bcb-data-lakehouse.git
cd bcb-data-lakehouse
```

### 2. Subir os containers

```bash
cd docker
docker compose up -d --build
```

### 3. Acessar os serviços

| Serviço | URL | Credenciais |
|---|---|---|
| Airflow | http://localhost:8081 | admin / admin |
| pgAdmin | http://localhost:5050 | admin@admin.com / admin |
| Streamlit | http://localhost:8501 | — |
| Spark UI | http://localhost:8080 | — |

### 4. Disparar o pipeline

```bash
docker exec -it airflow-bcb bash -c "airflow dags trigger bcb_lakehouse_pipeline"
```

### 5. Acompanhar execução

```bash
docker exec -it airflow-bcb bash -c "airflow tasks states-for-dag-run bcb_lakehouse_pipeline <run_id>"
```

## Modelagem dbt

```
gold_selic_anual (PostgreSQL)
        │
        ▼
stg_selic_anual         ── padronização e arredondamento
        │
        ▼
mart_selic_anual        ── classificação Alta / Moderada / Baixa
```

## Indicadores Disponíveis

| Indicador | Fonte | Granularidade |
|---|---|---|
| Taxa SELIC | BCB | diária → anual |


## Autor

Desenvolvido por **Gabriel Pereira Nunes**

Estudante de Data Science e Inteligência Artificial — IESB Brasília  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Gabriel%20Pereira%20Nunes-0A66C2?style=flat&logo=linkedin&logoColor=white)](www.linkedin.com/in/gabriel-pereirann)
[![GitHub](https://img.shields.io/badge/GitHub-gabrielPnunes-181717?style=flat&logo=github&logoColor=white)](https://github.com/gabrielPnunes)