# Agent

AI SQL Agent que responde perguntas em linguagem natural sobre os dados econômicos.

## Estrutura

```
agent/
└── sql_agent.py
```

## Como funciona

```
Pergunta em português
    ↓
LLM gera SQL (llama3.2 via Ollama)
    ↓
Query executada no PostgreSQL (schema analytics)
    ↓
LLM formula resposta em português
```

## Exemplo

```
Pergunta:  qual foi a taxa real de juros em 2022?
SQL gerado: SELECT taxa_real FROM analytics.mart_indicadores_anual WHERE ano = 2022;
Resposta:  Em 2022, a taxa real de juros foi de 8.65%.
```

## Requisitos

- Ollama rodando em `http://localhost:11434`
- Modelo instalado: `ollama pull llama3.2`