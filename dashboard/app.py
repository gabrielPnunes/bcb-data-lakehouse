import sys
sys.path.append('/app')

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from queries import get_indicadores, get_kpis_ano_atual
from agent.sql_agent import ask

st.set_page_config(
    page_title="BCB Data Lakehouse",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 BCB Data Lakehouse")
st.caption("Indicadores Econômicos do Banco Central do Brasil")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral",
    "📈 Evolução",
    "🔍 Comparações",
    "🤖 Assistente IA",
])

df   = get_indicadores()
kpis = get_kpis_ano_atual()

with tab1:
    st.subheader("Indicadores do Ano Atual")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Taxa SELIC", f"{kpis['ultimo_selic'].iloc[0]:.2f}%")
    with col2:
        st.metric("CDI", f"{kpis['ultimo_cdi'].iloc[0]:.2f}%")
    with col3:
        st.metric("Dólar Última Cotação", f"R$ {kpis['ultimo_cambio'].iloc[0]:.2f}")
    with col4:
        ultimo = df[df["ano"] == df["ano"].max()].iloc[0]
        st.metric("Classificação SELIC", ultimo["classificacao_selic"])

    st.divider()

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            "IPCA Acumulado no Ano",
            f"{kpis['ipca_acumulado'].iloc[0]:.2f}%",
            help="Juros compostos dos meses do ano atual."
        )
    with col6:
        st.metric(
            "IPCA Acumulado 12 Meses",
            f"{kpis['ipca_12m'].iloc[0]:.2f}%",
            help="Juros compostos dos últimos 12 meses."
        )
    with col7:
        st.metric(
            "Taxa Real (Ano)",
            f"{kpis['taxa_real_ano'].iloc[0]:.2f}%",
            help="SELIC - IPCA acumulado no ano."
        )
    with col8:
        st.metric(
            "Taxa Real (12M)",
            f"{kpis['taxa_real_12m'].iloc[0]:.2f}%",
            help="SELIC - IPCA acumulado 12 meses."
        )

    st.divider()
    st.subheader("Histórico Completo")
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("Evolução dos Indicadores")

    indicador = st.selectbox(
        "Selecione o indicador",
        ["SELIC", "IPCA", "CDI", "Câmbio USD/BRL", "Taxa Real"],
    )

    col_map = {
        "SELIC":          "media_selic",
        "IPCA":           "media_ipca",
        "CDI":            "media_cdi",
        "Câmbio USD/BRL": "media_cambio",
        "Taxa Real":      "taxa_real",
    }

    fig = px.line(
        df,
        x="ano",
        y=col_map[indicador],
        markers=True,
        labels={"ano": "Ano", col_map[indicador]: indicador},
    )

    fig.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Comparações")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["ano"], y=df["media_selic"], name="SELIC", mode="lines+markers"))
    fig2.add_trace(go.Scatter(x=df["ano"], y=df["media_ipca"],  name="IPCA",  mode="lines+markers"))
    fig2.add_trace(go.Scatter(x=df["ano"], y=df["taxa_real"],   name="Taxa Real", mode="lines+markers", line=dict(dash="dash")))
    fig2.update_layout(title="SELIC × IPCA × Taxa Real", xaxis=dict(dtick=1), yaxis_ticksuffix="%")
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df["ano"], y=df["media_selic"], name="SELIC", mode="lines+markers"))
    fig3.add_trace(go.Scatter(x=df["ano"], y=df["media_cdi"],   name="CDI",   mode="lines+markers"))
    fig3.update_layout(title="SELIC × CDI", xaxis=dict(dtick=1), yaxis_ticksuffix="%")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("🤖 Assistente de Dados")
    st.caption("Faça perguntas sobre os indicadores econômicos em linguagem natural.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ex: qual foi a taxa real de juros em 2022?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consultando os dados..."):
                response = ask(prompt)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})