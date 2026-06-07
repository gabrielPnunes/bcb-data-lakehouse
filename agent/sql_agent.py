from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from utils.logger import logger
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_URI = f"postgresql+psycopg2://admin:admin@{DB_HOST}:5432/bcb_data"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

db = SQLDatabase.from_uri(
    DB_URI,
    schema="analytics",
    view_support=True,
    include_tables=[
        "mart_selic_anual",
        "mart_indicadores_anual",
    ],
)

llm = OllamaLLM(
    model="llama3.2",
    base_url=OLLAMA_HOST,
)

sql_prompt = PromptTemplate.from_template("""
Você é um especialista em SQL e PostgreSQL.
Dado o schema da tabela abaixo, gere APENAS o SQL para responder a pergunta.
Retorne somente o SQL, sem explicações, sem markdown, sem backticks.

Schema:
{schema}

Pergunta: {question}

SQL:
""")

answer_prompt = PromptTemplate.from_template("""
Você é um analista de dados do Banco Central do Brasil.
Responda de forma curta e direta em português, usando apenas os dados fornecidos.
Não especule sobre o futuro. Não mencione o SQL.

Pergunta: {question}
Resultado da consulta: {result}

Resposta:
""")


def ask(question: str) -> str:
    try:
        logger.info(f"Pergunta recebida: {question}")

        schema = db.get_table_info()

        sql_chain = sql_prompt | llm | StrOutputParser()
        sql = sql_chain.invoke({
            "schema": schema,
            "question": question,
        }).strip()

        logger.info(f"SQL gerado: {sql}")

        result = db.run(sql)
        logger.info(f"Resultado: {result}")

        answer_chain = answer_prompt | llm | StrOutputParser()
        return answer_chain.invoke({
            "question": question,
            "result": result,
        })

    except Exception as e:
        logger.error(f"Erro no agente: {e}")
        return f"Não foi possível responder: {e}"