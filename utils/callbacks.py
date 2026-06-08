import requests
from config.settings import N8N_WEBHOOK_URL
from utils.logger import logger


def on_failure_callback(context):
    dag_id  = context.get("dag").dag_id
    task_id = context.get("task_instance").task_id
    run_id  = context.get("run_id")
    log_url = context.get("task_instance").log_url

    payload = {
        "dag_id":  dag_id,
        "task_id": task_id,
        "run_id":  run_id,
        "log_url": log_url,
        "status":  "FAILED",
        "emoji":   "🚨",
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        logger.info(f"Alerta de falha enviado ao n8n: {response.status_code}")
    except Exception as e:
        logger.error(f"Erro ao enviar alerta: {e}")


def on_success_callback(context):
    dag_id  = context.get("dag").dag_id
    task_id = context.get("task_instance").task_id
    run_id  = context.get("run_id")

    payload = {
        "dag_id":  dag_id,
        "task_id": task_id,
        "run_id":  run_id,
        "log_url": "",
        "status":  "SUCCESS",
        "emoji":   "✅",
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
        logger.info(f"Alerta de sucesso enviado ao n8n: {response.status_code}")
    except Exception as e:
        logger.error(f"Erro ao enviar alerta: {e}")