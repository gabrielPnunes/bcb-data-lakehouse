import os

DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = int(os.getenv("DB_PORT", 5432))
DB_NAME     = os.getenv("DB_NAME", "bcb_data")
DB_USER     = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")

DB_CONFIG = {
    "host":     DB_HOST,
    "port":     DB_PORT,
    "dbname":   DB_NAME,
    "user":     DB_USER,
    "password": DB_PASSWORD,
}

JDBC_URL = f"jdbc:postgresql://postgres-bcb:{DB_PORT}/{DB_NAME}"

JDBC_PROPS = {
    "user":     DB_USER,
    "password": DB_PASSWORD,
    "driver":   "org.postgresql.Driver",
}

BASE_PATH = "file:///app/data"

BRONZE = {
    "selic":  f"{BASE_PATH}/bronze/selic",
    "ipca":   f"{BASE_PATH}/bronze/ipca",
    "cambio": f"{BASE_PATH}/bronze/cambio",
    "cdi":    f"{BASE_PATH}/bronze/cdi",
}

SILVER = {
    "selic":  f"{BASE_PATH}/silver/selic",
    "ipca":   f"{BASE_PATH}/silver/ipca",
    "cambio": f"{BASE_PATH}/silver/cambio",
    "cdi":    f"{BASE_PATH}/silver/cdi",
}

GOLD = {
    "selic_anual":     f"{BASE_PATH}/gold/selic_anual",
    "ipca_anual":      f"{BASE_PATH}/gold/ipca_anual",
    "cambio_anual":    f"{BASE_PATH}/gold/cambio_anual",
    "cdi_anual":       f"{BASE_PATH}/gold/cdi_anual",
    "taxa_real_anual": f"{BASE_PATH}/gold/taxa_real_anual",
}

KAFKA_HOST  = os.getenv("KAFKA_HOST", "localhost:29092")
KAFKA_TOPIC = "selic-stream"

OLLAMA_HOST  = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = "llama3.2"

N8N_WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "http://n8n-bcb:5678/webhook/airflow-failure"
)
