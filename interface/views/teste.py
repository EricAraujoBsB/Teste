import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random
import pathlib
import requests
import plotly.graph_objects as go
import sys

# from alertas import alertas_page
# from configuracoes import configuracoes_page
# from relatorios import relatorios_page
# from analises import analises_page
# from dados import dados_page
# from user import user_page
import ipeadatapy as ipea

sys.path.insert(0, '../../services')
from search import theme, organization, code, sidebar  # endpoints do backend



# Configuração da página
st.set_page_config(
    page_title="IPEA",
    layout="wide",
    page_icon="📊"
)

# Estilo CSS
with open("styles/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Estado da sessão para controlar a página atual
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"


# Função para mudar de página
def change_page(page_name):
    st.session_state.current_page = page_name


# Sidebar
with st.sidebar:
    global buscarSerie, df, select
    st.title("Filtros")
    opcaoBusca = st.pills("Pesquisar por:", ["Órgão", "Tema", "Código"])
    if opcaoBusca == "Órgão":
        select = sidebar(opcaoBusca)
        buscarSerie = ""
        orgao = st.selectbox("Selecione o Órgão desejado", select, key="orgao")
        # buscarSerie = st.text_input("🔍 Busque uma série por nome, tema ou palavra-chave",
        #                             placeholder="Ex: setor público consolidado")
        # if buscarSerie != "":
        #     buscarSerie = st.selectbox("Selecione", organization(buscarSerie))

    elif opcaoBusca == "Tema":

        buscarSerie = ""
        buscarSerie = st.text_input("🔍 Busque uma série por nome, tema ou palavra-chave",
                                    placeholder="Ex: setor público consolidado")
        if buscarSerie != "":
            buscarSerie = st.selectbox("Selecione", theme(buscarSerie))
    elif opcaoBusca == "Código":

        buscarSerie = ""
        buscarSerie = st.text_input("🔍 Busque uma série por nome, tema ou palavra-chave",
                                    placeholder="Ex: setor público consolidado")
        if buscarSerie != "":
            buscarSerie = st.selectbox("Selecione", code(buscarSerie))

    st.markdown("### Navegação")

    # Botões de navegação
    if st.button("Dashboard"):
        change_page("Dashboard")
    if st.button("Relatórios"):
        change_page("Relatórios")


# Página principal
def main_page():
    global buscarSerie
    # Cabeçalho
    st.markdown("""
    <div class="header-ipea">
        <h3 class="titulo-ipea">Relatórios inteligentes IPEA</h3>
    </div>
    """, unsafe_allow_html=True)

    # Gráfico e Indicadores
    col1, col2 = st.columns(2)
    with col1:
        try:
            # Filtra as séries que contêm o termo digitado
            dataframe = pd.DataFrame(dict(VALUE=ipea.timeseries(buscarSerie).iloc[:, -1]))

            st.line_chart(dataframe)

            with col2:
                st.markdown("""
                    <style>
                    .card-metrica {
                        height: 100vh;
                        max-width: 700px; /* limite máximo para largura confortável */
                        width: 100%;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                        background-color: inherit;
                        padding: 20px;
                        border-radius: 10px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        box-sizing: border-box;
                        margin: auto; /* centraliza horizontalmente */
                    }
                    .card-topo .titulo {
                        font-weight: bold;
                        font-size: 20px;
                        color: inherit;
                    }
                    .valor, .variacao {
                        margin-top: 10px;
                        font-size: 16px;
                        color: inherit;
                    }
                    /* Div de altura 50vh, mesma largura e estilo do card-metrica */
                    .half-height-div {
                        height: 50vh;
                        max-width: 700px;  /* mesmo max-width do card */
                        width: 100%;
                        background-color: inherit;
                        padding: 20px;
                        border-radius: 10px;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        box-sizing: border-box;
                        margin: 20px auto; /* centraliza horizontalmente com espaçamento vertical */
                        overflow: auto; /* scroll interno se precisar */
                        font-size: 16px;
                        line-height: 1.6;
                        color: inherit;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # Div com altura 50vh, mesma largura e estilo do card
                st.markdown(f"""
                    <div class="half-height-div">
                        <h2>Relatório</h2>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
                        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

                        Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. 
                        Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. 
                        Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est. 
                        Mauris placerat eleifend leo.
                    </div>
                """, unsafe_allow_html=True)

        except:
            st.write("Busque uma série válida")


# Outras páginas


# Renderização condicional da página
if st.session_state.current_page == "Dashboard":
    main_page()

# elif st.session_state.current_page == "Relatórios":
#     relatorios_page()
# elif st.session_state.current_page == "Alertas":
#     alertas_page()
# elif st.session_state.current_page == "Análises inteligentes":
#     analises_page()
# elif st.session_state.current_page == "Dados":
#     dados_page()
# elif st.session_state.current_page == "User":
#     user_page()
# elif st.session_state.current_page == "Configurações":
#     configuracoes_page()