# BCB Data Lakehouse

> Pipeline de Engenharia de Dados com arquitetura Medalhão, processamento distribuído com Apache Spark e persistência em PostgreSQL, utilizando dados econômicos públicos do Banco Central do Brasil.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white
)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.x-E25A1C?style=flat-square&logo=apachespark&logoColor=white
)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white
)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white
)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square
)

</div>

---

## Sobre o Projeto

O **BCB Data Lakehouse** é um projeto de Engenharia de Dados construído para simular um ambiente profissional de ingestão, transformação e consumo analítico de dados econômicos públicos do [Banco Central do Brasil](https://dadosabertos.bcb.gov.br/).

O projeto aplica o padrão **Lakehouse** com arquitetura Medalhão (Bronze, Silver, Gold), combinando a flexibilidade de um Data Lake com a estrutura analítica de um Data Warehouse. Todo o ambiente roda localmente via Docker, sendo facilmente replicável e escalável para nuvem.

**Motivações do projeto:**

- Praticar Engenharia de Dados em um ambiente realista, com dados reais de produção
- Construir portfólio técnico com ferramentas relevantes no mercado
---

O fluxo de dados percorre quatro estágios:

1. **Ingestão** -- consumo automático da API pública do BCB via HTTP
2. **Bronze** -- armazenamento raw em Parquet, sem transformações, preservando a fonte original
3. **Silver** -- limpeza, tipagem e padronização dos dados com PySpark
4. **Gold** -- agregações e métricas de negócio prontas para consumo analítico
5. **Serving** -- carga final no PostgreSQL para consultas SQL e integração com ferramentas de BI

---

## Camadas do Pipeline

### Bronze -- Ingestão Raw

- Dados coletados diretamente da API do BCB sem modificações
- Armazenados em Parquet para eficiência de leitura e compressão
- Preservam o estado original dos dados para auditoria e reprocessamento

### Silver -- Limpeza e Tipagem

- Cast de tipos (`string` para `date`, `double`, etc.)
- Remoção de nulos e registros inconsistentes
- Padronização de nomes de colunas

```
root
 |-- data:  date   (nullable = true)
 |-- valor: double (nullable = true)
```

### Gold -- Camada Analítica

- Agregações temporais (médias, variações, janelas)
- Métricas prontas para consumo por dashboards e relatórios
- Modelagem orientada a perguntas de negócio

---

## Tecnologias

| Categoria | Ferramentas |
|---|---|
| Linguagem | Python 3.11, SQL |
| Processamento | Apache Spark, PySpark |
| Armazenamento | PostgreSQL, Parquet |
| Infraestrutura | Docker, Docker Compose |
| Fonte de Dados | API Pública BCB |
| Bibliotecas | requests, pandas, pyspark, psycopg2 |

---

## Estrutura do Repositório

```
bcb-data-lakehouse/
│
├── data/
│   ├── bronze/          # Dados raw (Parquet)
│   ├── silver/          # Dados limpos e tipados (Parquet)
│   └── gold/            # Dados agregados (Parquet)
│
├── ingestion/
│   └── bcb_api.py       # Consumo da API do Banco Central
│
├── processing/
│   ├── bronze_layer.py  # Ingestão para a camada Bronze
│   ├── silver_layer.py  # Transformações da camada Silver
│   └── gold_layer.py    # Agregações da camada Gold
│
├── storage/
│   └── postgres_loader.py  # Carga no PostgreSQL
│
├── docker/
│   └── docker-compose.yml  # Orquestração dos containers
│
├── requirements.txt
└── README.md
```

---

## Como Executar

### Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/seuusuario/bcb-data-lakehouse.git
cd bcb-data-lakehouse
```

### 2. Criar e ativar ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Subir a infraestrutura Docker

```bash
cd docker
docker compose up -d
```

Aguarde os containers inicializarem. Para verificar o status:

```bash
docker compose ps
```

### 5. Executar o pipeline

Execute cada etapa na ordem abaixo:

```bash
# Ingestão da API
python -m ingestion.bcb_api

# Bronze Layer
python -m processing.bronze_layer

# Silver Layer
python -m processing.silver_layer

# Gold Layer
python -m processing.gold_layer
```

### 6. Carregar no PostgreSQL

Acesse o container Spark e execute o loader:

```bash
docker exec -it spark-bcb bash
cd /app
python3 -m storage.postgres_loader
```

---

## Exemplo de Saída

Amostra dos dados processados na camada Silver:

```
+----------+----------+
|      data|     valor|
+----------+----------+
|2016-05-27|  0.052531|
|2016-05-30|  0.052531|
|2016-05-31|  0.052531|
+----------+----------+
```

---

## Serviços Docker

| Serviço    | Porta | Acesso |
|------------|-------|--------|
| PostgreSQL | 5432  | `localhost:5432` |
| pgAdmin    | 5050  | `http://localhost:5050` |
| Spark UI   | 8080  | `http://localhost:8080` |

**Credenciais locais (desenvolvimento):**

| Serviço    | Usuário / Email         | Senha  | Database  |
|------------|-------------------------|--------|-----------|
| PostgreSQL | `admin`                 | `admin`| `bcb_data`|
| pgAdmin    | `admin@admin.com`       | `admin`| --        |
---