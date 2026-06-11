# Config

Configurações centralizadas do projeto.

## Estrutura

```
config/
└── settings.py    # todas as variáveis de configuração do projeto
```

## Variáveis

| Variável | Padrão | Descrição |
|---|---|---|
| `DB_HOST` | `localhost` | Host do PostgreSQL |
| `DB_PORT` | `5432` | Porta do PostgreSQL |
| `DB_NAME` | `bcb_data` | Nome do banco |
| `DB_USER` | `admin` | Usuário |
| `DB_PASSWORD` | `admin` | Senha |
| `KAFKA_HOST` | `localhost:29092` | Broker Kafka |
| `KAFKA_TOPIC` | `selic-stream` | Tópico de streaming |
| `OLLAMA_HOST` | `http://localhost:11434` | Endpoint do Ollama |
| `OLLAMA_MODEL` | `llama3.2` | Modelo LLM |
| `N8N_WEBHOOK_URL` | `http://n8n-bcb:5678/...` | Webhook de alertas |

## Caminhos Delta Lake

```
data/
├── bronze/    # dados brutos da API BCB (Parquet)
├── silver/    # dados limpos e transformados (Delta Lake)
└── gold/      # agregações analíticas (Delta Lake)
```