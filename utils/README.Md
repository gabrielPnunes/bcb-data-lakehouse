# Utils

Utilitários compartilhados por todo o projeto.

## Estrutura

```
utils/
├── logger.py      # logging centralizado
└── callbacks.py   # callbacks do Airflow
```

## logger

Formato padrão de todos os logs do projeto:

```
2026-06-10 14:00:00,000 | INFO | mensagem
```

## callbacks

Dois callbacks registrados em todas as tasks da DAG:

- `on_success_callback` — envia webhook ao n8n com status `SUCCESS`
- `on_failure_callback` — envia webhook ao n8n com status `FAILED`

O n8n recebe o webhook e encaminha a notificação para o Telegram.