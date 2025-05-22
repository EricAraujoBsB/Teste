import streamlit as st
from datetime import date

# Configurações da página
st.set_page_config(page_title="GovInsights", layout="wide", page_icon="📊")

# Inicializa estado do menu lateral direito
if "show_filters" not in st.session_state:
    st.session_state.show_filters = True

# Função para esconder/mostrar painel lateral
def toggle_filter_panel():
    st.session_state.show_filters = not st.session_state.show_filters

# Colunas principais da interface (Dashboard | Filtros)
col_dashboard, col_filters = st.columns([4, 1], gap="large")

# Coluna principal: dashboard de dados
with col_dashboard:
    st.markdown("<h3 style='color:white;'>Relatórios inteligentes IPEA</h3>", unsafe_allow_html=True)
    
    st.info("Gráfico ou cards aqui...")

# Coluna lateral direita: painel de filtros
if st.session_state.show_filters:
    with col_filters:
        st.markdown("## Filtros")
        orgao = st.selectbox("Órgão Responsável", ["Banco Central", "IBGE", "IPEA"])
        tema = st.selectbox("Tema da Série", ["Inflação", "Câmbio", "Juros"])
        codigo = st.selectbox("Código da Série", ["IPCA-15", "USD-BRL", "Selic"])

        st.markdown("### Período de Análise")
        data_inicio = st.date_input("Data Inicial", value=date(2023, 1, 1))
        data_fim = st.date_input("Data Final", value=date(2024, 12, 31))

        unidade = st.selectbox("Unidade de medida desejada", ["BRL", "USD", "Percentual"])

        if st.button("Buscar"):
            toggle_filter_panel()  # Recolhe o painel

            # Armazena valores em variáveis de sessão
            st.session_state.filtro_orgao = orgao
            st.session_state.filtro_tema = tema
            st.session_state.filtro_codigo = codigo
            st.session_state.filtro_data_inicio = data_inicio
            st.session_state.filtro_data_fim = data_fim
            st.session_state.filtro_unidade = unidade

            st.success("Filtros aplicados com sucesso!")

# Botão para mostrar novamente os filtros, se oculto
else:
    with col_filters:
        if st.button("Mostrar Filtros"):
            toggle_filter_panel()
