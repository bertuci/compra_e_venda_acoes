# -*- coding: utf-8 -*-

#importando as bibliotecas

from matplotlib.pyplot import text
import yfinance as yf
import pandas as pd
import numpy as np
import os.path 
import telegram 

pd.options.mode.chained_assignment = None


#escolher uma ação
wege = yf.Ticker('WEGE3.SA')

#escolher inteervalo de dados
wege_dia = wege.history(period='id', interval='5m')


#pegar preço de fechamento
wege_dia = wege_dia.Close


#transformando em dataframe
df_wege_dia = pd.DataFrame(wege_dia)


#reset index
df_wege_dia.reset_index(inplace=True)

#pegar o ultimo valor negociado
wege_dia_ultimo_preco = df_wege_dia.tail(1)

#renomear as colunas
wege_dia_ultimo_preco.rename(columns={'Datetime':'data_pregao', 'Close':'preco_fechamento'}, inplace=True)



#Ajustar a data
wege_dia_ultimo_preco['data_pregao']=pd.to_datetime(wege_dia_ultimo_preco['data_pregao'], format='%Y-%m-%d')

#Usar o data frame historico e pegar apenas o preço de fechamento e data pregão

if os.path.isfile('wege.csv'):
    df_wege = pd.read_csv('wege.csv', delimiter=';')
else:
    df = pd.read_csv('all_bovesta.csv', delimiter=';') #colocar aqui o seu arquivo do bovespa
    df_wege = df[df['silga_acao']=='WEGE3']
    df_wege = df_wege[['data_pregao', 'preco_fechamento']]

#Ajustar a data
df_wege['data_pregao']=pd.to_datetime(df_wege['data_pregao'], format='%Y-%m-%d')

#Retirar a ultima data que queremos calcular
df_remove = df_wege.loc[(df_wege['data_pregao'] == pd.to_datetime('today').normalize())]

df_wege = df_wege.drop(df_wege.index)


#append data atual
df_wege_total = df_wege.append(wege_dia_ultimo_preco)


#Ajuste data atual

df_wege_total['data_pregao']=pd.to_datetime(df_wege_total['data_pregao'], utc=True).dt.date

df_wege_total.to_csv('wege.csv', sep=';', index=False)

#Calcular MACD

rapidaMME=df_wege_total.preco_fechamento.ewm(span=12).mean()

lentaMME = df_wege_total.preco_fechamento.ewm(span=26).mean()

MACD= rapidaMME - lentaMME

sinal=MACD.ewm(span=9).mean()

df_wege_total['MACD'] = MACD
df_wege_total['sinal'] = sinal


#Ajuste de indx e retirar o campo data pregão

df_wege_total = df_wege_total.set_index(pd.DatetimeIndex(df_wege_total['data_pregao'].values))
df_wege_total = df_wege_total.drop('data_pregao',1)


# Criar codigo para verificar a compra ou a venda

df_wege_total['flag']=''
df_wege_total['preco_compra']=np.nan
df_wege_total['preco_venda']=np.nan



for i in range(1, len(df_wege_total.sinal)):
    if df_wege_total['MACD'][i] > df_wege_total['sinal'][i]:
        if df_wege_total['flag'][i-1] == 'c':
            df_wege_total['flag'][i]='C'
        else:
            df_wege_total['flag'][i]='C'
            df_wege_total['preco_compra'][i] = df_wege_total['preco_fechamento'][i]
        


    elif df_wege_total['MACD'][i] < df_wege_total['sinal'][i]:
        if df_wege_total['flag'][i-1] =='V':
            df_wege_total['flag'][i]='V'
        else:
            df_wege_total['flag'][i]='V'
            df_wege_total['preco_venda'][i] = df_wege_total['preco_fechamento'][i]


#Verifica os 2 ultimos dias
hoje = df_wege_total.flag[-1]
ontem = df_wege_total.flag[-2]

flag= hoje
preco_fechamento = round(df_wege_total.preco_fechamento.tail(1)[-1],2)

print(flag, preco_fechamento)


my_token = '1840232813:AAHxoVmcDWHK3jAxiTWsMqTsiw9vTHaICpY'
chat_id = '-476980685'

def envia_mensagem(msg, chat_id, token=my_token):
    bot=telegram.Bot(token = token)
    bot.SendMessage(chat_id = chat_id, text=msg)

msg = f'WEGE3 (WEGE), {flag} preço de fechamento: {preco_fechamento}'

if ontem == hoje:
    envia_mensagem(msg, chat_id, my_token)

