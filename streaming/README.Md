# Streaming

Processamento em tempo real com Kafka e Spark Structured Streaming.

## Estrutura

```
streaming/
├── producer.py    # PostgreSQL → Kafka
└── consumer.py    # Kafka → Delta Lake
```

## Fluxo

```
gold_selic_anual (PostgreSQL)
    ↓ producer.py
Kafka tópico: selic-stream
    ↓ consumer.py (Spark Structured Streaming)
data/streaming/selic (Delta Lake)
```

## Como rodar

Terminal 1:
```bash
docker exec -it airflow-bcb bash
python3 -m streaming.consumer
```

Terminal 2:
```bash
python3 -m streaming.producer
```