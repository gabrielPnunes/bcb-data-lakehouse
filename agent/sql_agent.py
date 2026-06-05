from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain.chains import create_sql_query_chain
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
    include_tables=["mart_selic_anual"],
)

llm = OllamaLLM(
    model="llama3.2",
    base_url=OLLAMA_HOST,
)

chain = create_sql_query_chain(llm, db)


def ask(question: str) -> str:
    try:
        logger.info(f"Pergunta recebida: {question}")

        sql = chain.invoke({"question": question})
        logger.info(f"SQL gerado: {sql}")

        result = db.run(sql)
        logger.info(f"Resultado: {result}")

        answer_prompt = PromptTemplate.from_template("""
Você é um analista de dados do Banco Central do Brasil.

Pergunta: {question}
SQL executado: {sql}
Resultado: {result}

Responda em português de forma clara e objetiva, sem mencionar o SQL.
""")

        answer_chain = answer_prompt | llm | StrOutputParser()

        return answer_chain.invoke({
            "question": question,
            "sql": sql,
            "result": result,
        })

    except Exception as e:
        logger.error(f"Erro no agente: {e}")
        return f"Não foi possível responder: {e}"