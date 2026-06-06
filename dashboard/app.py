import sys
sys.path.append('/app')

import streamlit as st
import plotly.express as px
from queries import get_selic_anual, get_selic_raw
from agent.sql_agent import ask

from agent.sql_agent import ask

st.set_page_config(
    page_title="BCB Data Lakehouse",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 BCB Data Lakehouse")
st.caption("Indicadores Econômicos do Banco Central do Brasil")

tab1, tab2 = st.tabs(["📊 Dashboard", "🤖 Assistente IA"])

with tab1:
    df_mart = get_selic_anual()
    df_raw  = get_selic_raw()

    col1, col2, col3 = st.columns(3)

    with col1:
        ultima = df_mart.iloc[-1]
        st.metric(
            label="Último ano disponível",
            value=str(int(ultima["ano"])),
        )

    with col2:
        st.metric(
            label="Média SELIC",
            value=f"{ultima['media_selic']:.2f}%",
        )

    with col3:
        st.metric(
            label="Classificação",
            value=ultima["classificacao_selic"],
        )

    st.divider()

    st.subheader("Evolução da Taxa SELIC")

    fig = px.line(
        df_raw,
        x="ano",
        y="media_selic",
        markers=True,
        labels={"ano": "Ano", "media_selic": "Média SELIC (%)"},
    )

    fig.update_layout(
        xaxis=dict(dtick=1),
        yaxis_ticksuffix="%",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Classificação por Ano")

    fig2 = px.bar(
        df_mart,
        x="ano",
        y="media_selic",
        color="classificacao_selic",
        color_discrete_map={
            "Alta":     "#ef4444",
            "Moderada": "#f59e0b",
            "Baixa":    "#22c55e",
        },
        labels={
            "ano":                 "Ano",
            "media_selic":         "Média SELIC (%)",
            "classificacao_selic": "Classificação",
        },
    )

    fig2.update_layout(
        xaxis=dict(dtick=1),
        yaxis_ticksuffix="%",
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Tabela Completa")
    st.dataframe(df_mart, use_container_width=True)

with tab2:
    st.subheader("🤖 Assistente de Dados")
    st.caption("Faça perguntas sobre os indicadores econômicos em linguagem natural.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ex: qual foi a média da SELIC em 2022?"):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando os dados..."):
                response = ask(prompt)
            st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
        })