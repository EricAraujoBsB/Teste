import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import random
# import pathlib

import sys
sys.path.insert(0, '../teste/services')
from search import filtro

# from alertas import alertas_page
# from configuracoes import configuracoes_page
# from relatorios import relatorios_page
# from analises import analises_page
# from dados import dados_page
# from user import user_page


# Configuração da página
st.set_page_config(
    page_title="GovInsights",
    layout="wide",
    page_icon="📊"
)

# Estilo CSS
with open("./interface/views/styles/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Estado da sessão para controlar a página atual
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Função para mudar de página
def change_page(page_name):
    st.session_state.current_page = page_name

# Sidebar

html_code = """
<div style="width: 250px; position: fixed; top: 0; left: 0; height: 100%; background-color: #f7f7f7; padding-top: 20px; border-right: 2px solid #ddd;">

    <h2 style="text-align: center; color: #333;">Gov Insights</h2>
    
    <input type="text" placeholder="🔍 Search for..." style="width: 100%; padding: 8px; margin: 8px 0; box-sizing: border-box;">

    <h3 style="color: #333;">Navegação</h3>

    <!-- Buttons for navigation -->
    <button onclick="window.location.href='/dashboard'"; style="display: block; width: 100%; padding: 12px; margin: 8px 0; text-align: center; background-color: #007bff; color: white; border: none; cursor: pointer; border-radius: 5px;">
        Dashboard
    </button>
    <button onclick="window.location.href='/relatorios'"; style="display: block; width: 100%; padding: 12px; margin: 8px 0; text-align: center; background-color: #007bff; color: white; border: none; cursor: pointer; border-radius: 5px;">
        Exportar Relatórios
    </button>
    <button onclick="window.location.href='/alertas'"; style="display: block; width: 100%; padding: 12px; margin: 8px 0; text-align: center; background-color: #007bff; color: white; border: none; cursor: pointer; border-radius: 5px;">
        Alertas
    </button>

    <div style="margin: 20px 0; border-top: 1px solid #ccc;"></div>

    <button onclick="window.location.href='/configuracoes'"; style="display: block; width: 100%; padding: 12px; margin: 8px 0; text-align: center; background-color: #007bff; color: white; border: none; cursor: pointer; border-radius: 5px;">
        Configurações
    </button>

</div>
"""
components.html(html_code, height=800)
# with st.sidebar:
#     st.title("Gov Insights")
    
#     st.text_input("🔍 Search for...")
#     st.markdown("### Navegação")
    
#     # Botões de navegação
    
#     if st.button("Dashboard"):
#         change_page("Dashboard")
#     if st.button("Exportar Relatórios"):
#         change_page("Relatórios")
#     if st.button("Alertas"):
#         change_page("Alertas")

    
#     st.markdown("---")


#     if st.button("Configurações"):
#         change_page("Configurações")


# Funções simuladas
def get_total_receitas(): return 50800, 28.4
def get_total_despesas(): return 23600, -12.6
def get_alertas_ativos(): return 3, 3.1
def get_series_temporais():
    meses = pd.date_range("2023-01-01", periods=12, freq="M")
    receitas = [random.randint(80, 240) for _ in range(12)]
    despesas = [random.randint(60, 180) for _ in range(12)]
    return pd.DataFrame({"Meses": meses, "Receitas": receitas, "Despesas": despesas})
def get_valor_indicador(): return 23648
def get_gauge_value(): return 65

# Página principal
def main_page():
    # Cabeçalho
    st.markdown("""
    <div class="header-ipea">
        <h3 class="titulo-ipea">Relatórios inteligentes IPEA</h3>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principais
    col1, col2, col3 = st.columns(3)
    receitas, receitas_var = get_total_receitas()
    despesas, despesas_var = get_total_despesas()
    alertas, alertas_var = get_alertas_ativos()

    # Card 1
    with col1:
        st.markdown(f"""
        <div class="card-metrica">
            <div class="card-topo"><span class="icon">👤</span><span class="titulo">Total de receitas</span></div>
            <div class="valor">{receitas:,}K</div>
            <div class="variacao {'positivo' if receitas_var >= 0 else 'negativo'}">{'▲' if receitas_var >= 0 else '▼'} {abs(receitas_var):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2
    with col2:
        st.markdown(f"""
        <div class="card-metrica">
            <div class="card-topo"><span class="icon">👁️</span><span class="titulo">Total de Despesas</span></div>
            <div class="valor">{despesas:,}K</div>
            <div class="variacao {'positivo' if despesas_var >= 0 else 'negativo'}">{'▲' if despesas_var >= 0 else '▼'} {abs(despesas_var):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3
    with col3:
        st.markdown(f"""
        <div class="card-metrica">
            <div class="card-topo"><span class="icon">➕</span><span class="titulo">Alertas Ativos</span></div>
            <div class="valor">{alertas}</div>
            <div class="variacao {'positivo' if alertas_var >= 0 else 'negativo'}">{'▲' if alertas_var >= 0 else '▼'} {abs(alertas_var):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## ")

    # Gráfico e Indicadores
    col4, col5 = st.columns([3, 2])
    df = get_series_temporais()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Meses"], y=df["Receitas"], name="Receitas", line=dict(color="#A020F0")))
    fig.add_trace(go.Scatter(x=df["Meses"], y=df["Despesas"], name="Despesas", line=dict(color="#00CFFF")))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    col4.plotly_chart(fig, use_container_width=True)

    with col5:
        st.markdown(f"""
        <div class='painel'>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque urna mi, varius nec tincidunt sed.</p>
        <h2 class='valor-indicador'>{get_valor_indicador():,}</h2>
        </div>
        """, unsafe_allow_html=True)

        gauge_value = get_gauge_value()
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number", value=gauge_value, title={'text': ""},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#555555"},
                   'steps': [{'range': [0, 50], 'color': "#e0e0e0"}, {'range': [50, 100], 'color': "#b0b0b0"}],
                   'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': gauge_value}}
        ))
        gauge_fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=250, width=250, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#333333"))
        st.plotly_chart(gauge_fig, use_container_width=True)



# Outras páginas 


# Renderização condicional da página

# if st.user.is_logged_in:
#     if st.session_state.current_page == "Dashboard":
#         main_page()
        
#     elif st.session_state.current_page == "Relatórios":
#         relatorios_page()
#     elif st.session_state.current_page == "Alertas":
#         alertas_page()
#     elif st.session_state.current_page == "Análises inteligentes":
#         analises_page()
#     elif st.session_state.current_page == "Dados":
#         dados_page()
#     elif st.session_state.current_page == "User":
#         user_page()
#     elif st.session_state.current_page == "Configurações":
#         configuracoes_page()

# else:
#     st.title("Logue para usar aplicação.")