import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date
import sys
import ipeadatapy as ipea

# sys.path.insert(0, '../teste/services')
# from search import filtro  # Deve retornar um DataFrame com colunas: Meses, Receitas, Despesas

# Configuração da página
st.set_page_config(page_title="GovInsights", layout="wide", page_icon="📊")

# ==========================
# ESTADOS DE SESSÃO
# ==========================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "show_filters" not in st.session_state:
    st.session_state.show_filters = True

# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def filtro(phrase: str):
    # Retorna um dataframe contendo as series com dados financeiros do IPEA de acordo com a string parametrizada referente ao órgão procurado.

    # Caso a busca não seja bem sucedida sera retornado uma string "Não Encontrado".

    series = ipea.metadata()
    series = series[series["MEASURE"].str.contains("\\$")]
    series = pd.concat([series[series["SOURCE ACRONYM"].str.lower().str.contains(phrase.lower())],
                        series[series["SOURCE"].str.lower().str.contains(phrase.lower())]])
    series = series.sort_values(by='CODE').drop_duplicates()
    return "Não Encontrado" if series.empty else series

def toggle_filter_panel():
    st.session_state.show_filters = not st.session_state.show_filters

def change_page(page_name):
    st.session_state.current_page = page_name

def render_dashboard():
    st.markdown("<h3 style='color:white;'>Gov Insights - Relatórios inteligentes IPEA</h3>", unsafe_allow_html=True)
    
    # Obtém os dados filtrados da função filtro()
    df = filtro("IBGE")

    if df is None or df.empty:
        st.warning("Nenhum dado disponível para os filtros aplicados.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Meses"], y=df["Receitas"], name="Receitas", line=dict(color="#27ae60")))
    fig.add_trace(go.Scatter(x=df["Meses"], y=df["Despesas"], name="Despesas", line=dict(color="#c0392b")))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# INTERFACE PRINCIPAL
# ==========================

# Três colunas: Menu | Dashboard | Filtros
col_menu, col_dash, col_filtros = st.columns([1, 5, 2], gap="large")

# 1️⃣ MENU LATERAL ESQUERDO
with col_menu:
    st.markdown("### ")
    st.button("🏠 Dashboard", on_click=change_page, args=("Dashboard",))
    st.button("📄 Relatórios", on_click=change_page, args=("Relatórios",))
    st.button("🚨 Alertas", on_click=change_page, args=("Alertas",))
    st.markdown("---")
    st.button("⚙️ Configurações", on_click=change_page, args=("Configurações",))

# 2️⃣ CONTEÚDO CENTRAL (DASHBOARD)
with col_dash:
    if st.session_state.current_page == "Dashboard":
        render_dashboard()
    else:
        st.info(f"Você está na página: {st.session_state.current_page}")

# 3️⃣ PAINEL DE FILTROS À DIREITA
if st.session_state.show_filters:
    with col_filtros:
        st.markdown("## Filtros")

        orgao = st.selectbox("Órgão Responsável", ["Banco Central", "IBGE", "IPEA"], key="orgao")
        tema = st.selectbox("Tema da Série", ["Inflação", "Câmbio", "Juros"], key="tema")
        codigo = st.selectbox("Código da Série", ["IPCA-15", "USD-BRL", "Selic"], key="codigo")

        st.markdown("### Período de Análise")
        data_inicio = st.date_input("Data Inicial", value=date(2023, 1, 1), key="data_inicio")
        data_fim = st.date_input("Data Final", value=date(2024, 12, 31), key="data_fim")

        unidade = st.selectbox("Unidade de medida", ["BRL", "USD", "%"], key="unidade")

        if st.button("Buscar"):
            # Armazenando filtros
            st.session_state.filtro_orgao = orgao
            st.session_state.filtro_tema = tema
            st.session_state.filtro_codigo = codigo
            st.session_state.filtro_data_inicio = data_inicio
            st.session_state.filtro_data_fim = data_fim
            st.session_state.filtro_unidade = unidade

            toggle_filter_panel()
            st.experimental_rerun()
else:
    with col_filtros:
        if st.button("Mostrar Filtros"):
            toggle_filter_panel()
