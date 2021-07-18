#IMPORTANDO AS BIBLIOTECAS

import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import io
#nome da aplicação


st.write("""
# Análises de ações


""")

#criando uma sidebar
st.sidebar.header('Escolha sua ação')

#ler arquivo de ações

multiple_files = st.file_uploader(
    "all_bovespa.",
    accept_multiple_files=True
)

for file in multiple_files:
    file_container = st.beta_expander(
        f"Nome do Arquivo: {file.name} ({file.size})"
    )
    data = io.BytesIO(file.getbuffer())

df = pd.read_csv(data)



df_data = pd.to_datetime(df['data_pregao']).dt.date.drop_duplicates()

min_date = min(df_data)
max_date = max(df_data)

stock = df['sigla_acao'].drop_duplicates()
stoc_choices =  st.sidebar.selectbox('Escolha sua ação',stock)

start_date = st.sidebar.text_input('Digite uma data de inicio', min_date)
end_date = st.sidebar.text_input('Digite uma data de final', max_date)

start = pd.to_datetime(start_date)
end = pd.to_datetime(end_date)

if start > end :
    st.error('Data Final deve ser MAIOR que a data inicial.')


df = df[(df['sigla_acao']== stoc_choices) & (pd.to_datetime(df['data_pregao'])>= start) &(pd.to_datetime(df['data_pregao'])<= end)]

df = df.set_index(pd.DatetimeIndex(df['data_pregao'].values))

#Criando gráficos

st.header('Ação: ' + stoc_choices.upper())
st.write('Preço de Abertura')
st.line_chart(df['preco_abertura'])


st.write('Preço de Fechamento')
st.line_chart(df['preco_fechamento'])



st.write('Volume negociado')
st.line_chart(df['volume'])

rapidaMME = df.preco_fechamento.ewm(span=12).mean()
lentaMME = df.preco_fechamento.ewm(span=26).mean()
MACD = rapidaMME - lentaMME
sinal = MACD.ewm(span=9).mean()
st.write('Sinal de compra MACD')
chart_data = pd.DataFrame(
     np.random.randn(20, 2),
     columns=['stock', 'sinal'])

st.line_chart(chart_data)