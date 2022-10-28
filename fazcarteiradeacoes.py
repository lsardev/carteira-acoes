# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import fundamentus

df = fundamentus.get_resultado()

perfil = df[df['pl'] > 0]
perfil = perfil[perfil['pl'] < 5.38]
perfil = perfil[perfil['roe'] > 0.50]
perfil = perfil[perfil['dy'] > 0.08]


print(perfil)

import streamlit as st
from datetime import date
import yfinance as yf
from plotly import graph_objs as go
import numpy 
numpy.random.BitGenerator = numpy.random.bit_generator.BitGenerator

codigos = perfil.index

DATA_INICIO = '2017-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d')

st.title("Análise de ações")
st.sidebar.header('Escolha a ação')

acao_escolhida = st.sidebar.selectbox('Escolha uma ação: ', codigos)

df_acao = perfil.index == acao_escolhida
acao_para_yfinance = acao_escolhida + '.SA'

def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM)
    df.reset_index(inplace=True)
    return df

df_valores = pegar_valores_online(acao_para_yfinance)

st.subheader('Tabela de valores - ' + acao_escolhida)
st.write(df_valores.tail(10))

#plotar grafico
st.subheader('Gráfico de preços - ' + acao_escolhida)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'],
                        y=df_valores['Close'],
                        name='Preço Fechamento',
                        line_color='blue'))
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Open'],
                         name='Preço Abertura',
                         line_color='green'))

st.plotly_chart(fig)

col1, col2, col3 = st.columns(3)
col1.metric("Índice P/L", value=perfil[perfil['pl'] == acao_escolhida]["pl"])
col2.metric("Dividend Yield", value=perfil[perfil['dy'] == acao_escolhida]["dy"])
col3.metric("ROE", value=perfil[perfil['roe'] == acao_escolhida]["roe"])





