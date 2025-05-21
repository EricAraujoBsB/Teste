# importar bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yfinance


#criar funções

    #cotações do itau

@st.cache_data
def carregar_dados(empresa): 
    dados_acao = yf.Ticker(empresa)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    return cotacoes_acao



dados = carregar_dados("ITUB4.SA")
print(dados)


#prepara as visualizações

#criar interface visual do streamlit 

st.write("""
# app preço de ações
o grafico abaixo representa a evolução...
""") #markdown