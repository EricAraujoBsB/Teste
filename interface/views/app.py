import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date
import sys
import ipeadatapy as ipea

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

def toggle_filter_panel():
    st.session_state.show_filters = not st.session_state.show_filters

def change_page(page_name):
    st.session_state.current_page = page_name

def obter_dados_serie(codigo_serie: str, data_inicio: date, data_fim: date):
    """
    Obtém os dados da série histórica pelo código e intervalo de datas,
    retorna DataFrame com colunas ['DATA', 'VALOR'] filtrado.
    """
    try:
        df = ipea.get_series(codigo_serie)
        df["DATA"] = pd.to_datetime(df["DATA"])
        mask = (df["DATA"] >= pd.to_datetime(data_inicio)) & (df["DATA"] <= pd.to_datetime(data_fim))
        df = df.loc[mask]
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"Erro ao obter dados da série {codigo_serie}: {e}")
        return pd.DataFrame(columns=["DATA", "VALOR"])

def render_dashboard():
    st.markdown("<h3 style='color:white;'>Gov Insights - Relatórios inteligentes IPEA</h3>", unsafe_allow_html=True)

    # Pega filtros armazenados
    codigo_serie = st.session_state.get("filtro_codigo", "12.1.1.01")  # Exemplo padrão
    data_inicio = st.session_state.get("filtro_data_inicio", date(2023, 1, 1))
    data_fim = st.session_state.get("filtro_data_fim", date(2024, 12, 31))

    # Para fins do exemplo, vamos buscar a mesma série duas vezes simulando receitas e despesas,
    # substitua pelos códigos corretos ou pelo filtro real que quiser usar.
    df_receitas = obter_dados_serie(codigo_serie, data_inicio, data_fim)
    df_despesas = obter_dados_serie(codigo_serie, data_inicio, data_fim)  # Troque para código despesa real

    if df_receitas.empty or df_despesas.empty:
        st.warning("Nenhum dado disponível para os filtros aplicados.")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_receitas["DATA"], y=df_receitas["VALOR"], name="Receitas", line=dict(color="#27ae60")))
    fig.add_trace(go.Scatter(x=df_despesas["DATA"], y=df_despesas["VALOR"], name="Despesas", line=dict(color="#c0392b")))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=450,
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# INTERFACE PRINCIPAL
# ==========================

# Layout: Menu | Dashboard | Filtros
col_menu, col_dash, col_filtros = st.columns([1, 5, 2], gap="large")

# MENU LATERAL ESQUERDO
with col_menu:
    st.markdown("### ")
    st.button("🏠 Dashboard", on_click=change_page, args=("Dashboard",))
    st.button("📄 Relatórios", on_click=change_page, args=("Relatórios",))
    st.button("🚨 Alertas", on_click=change_page, args=("Alertas",))
    st.markdown("---")
    st.button("⚙️ Configurações", on_click=change_page, args=("Configurações",))

# CONTEÚDO CENTRAL (Dashboard)
with col_dash:
    if st.session_state.current_page == "Dashboard":
        render_dashboard()
    else:
        st.info(f"Você está na página: {st.session_state.current_page}")

# PAINEL DE FILTROS À DIREITA
if st.session_state.show_filters:
    with col_filtros:
        st.markdown("## Filtros")

        orgao = st.selectbox("Órgão Responsável", ["Banco Central", "IBGE", "IPEA"], key="orgao")
        tema = st.selectbox("Tema da Série", ["Inflação", "Câmbio", "Juros"], key="tema")
        codigo = st.selectbox("Código da Série", ["12.1.1.01", "12.1.2.01", "12.1.3.01"], key="codigo")  # Códigos reais exemplo

        st.markdown("### Período de Análise")
        data_inicio = st.date_input("Data Inicial", value=date(2023, 1, 1), key="data_inicio")
        data_fim = st.date_input("Data Final", value=date(2024, 12, 31), key="data_fim")

        unidade = st.selectbox("Unidade de medida", ["BRL", "USD", "%"], key="unidade")

        if st.button("Buscar"):
            # Salva filtros na sessão
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
