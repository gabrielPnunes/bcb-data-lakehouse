# Docker

Infraestrutura completa do projeto via Docker Compose.

## Serviços

| Container | Imagem | Porta | Descrição |
|---|---|---|---|
| `postgres-bcb` | postgres:16 | 5432 | banco de dados principal |
| `pgadmin-bcb` | dpage/pgadmin4 | 5050 | interface visual do PostgreSQL |
| `airflow-bcb` | custom | 8081 | orquestrador do pipeline |
| `spark-bcb` | custom | 8080, 7077 | processamento distribuído |
| `streamlit-bcb` | custom | 8501 | dashboard interativo |
| `kafka-bcb` | confluentinc/cp-kafka | 9092, 29092 | streaming |
| `zookeeper-bcb` | confluentinc/cp-zookeeper | 2181 | coordenador do Kafka |
| `n8n-bcb` | n8nio/n8n | 5678 | automação e alertas |

## Como subir tudo

```bash
cd docker
docker compose up -d
```

## Volumes persistentes

| Volume | Conteúdo |
|---|---|
| `postgres_data` | dados do PostgreSQL |
| `n8n_data` | workflows do n8n |

## Observações

O Airflow recebe `DB_HOST=postgres-bcb` via environment para que o `psycopg2` conecte corretamente ao PostgreSQL dentro da rede Docker. Sem essa variável, o fallback `localhost` causa falhas silenciosas no `postgres_loader`.