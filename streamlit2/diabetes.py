#

import streamlit as st
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing   import RobustScaler, MinMaxScaler
from imblearn.over_sampling  import SMOTE
#TITULO

st.write("""
# Prevendo Diabetes \n
utilizando machine learning para prever diabetes
""")

#dataset
df = pd.read_csv('D:/Profile/OneDrive - Imagem Geosistemas e Comércio LTDA/Desktop/streamlit2/diabetes.csv')

#cabeçalho

st.subheader('Informações dos dados')

#nome do usuário

user_input = st.sidebar.text_input('Digite seu nome')

st.write('Paciente: ', user_input)

#dados de entrada
x = df.drop(['Outcome'],1) #vamos dropar o campo que queremos prever
y = df['Outcome']
#separar dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size= 0.2, random_state=42)


#dados dos usuários com a função
def get_user_data():
    pergnancis = st.sidebar.slider('Gravidez', 0, 15, 1)
    glucose = st.sidebar.slider('Glicose', 0, 200, 110)
    blood_pressure = st.sidebar.slider('Pressão sanguinea', 0, 122, 72)
    skin_thickness = st.sidebar.slider('Espessura da pele', 0, 99, 20)
    insulin = st.sidebar.slider('Insuluna',0, 900, 30)
    bmi = st.sidebar.slider('Indice de Massa Corporal', 0.0, 70.0, 15.0)
    dpf = st.sidebar.slider('Historico familiar de diabetes', 0.0, 3.0, 0.0)
    age = st.sidebar.slider('Idade', 15,100, 21)

    user_data = {'gravidez': pergnancis,
    'Glicose':glucose,
    'Pressão sanguinea':blood_pressure,
    'Espessura da pele': skin_thickness,
    'Insulina':insulin,
    'Indice de massa Corporea': bmi,
    'Historico familiar de diabetes':dpf,
    'Idade':age}

    features = pd.DataFrame(user_data, index=[0])

    return  features

user_input_variables = get_user_data()

#GRAFICO
graf = st.bar_chart(user_input_variables)

#criando o modelo de machine learning
st.subheader('Dados do usuário')
st.write(user_input_variables)


dtc = DecisionTreeClassifier(criterion='entropy', max_depth=3, min_samples_split=8)
dtc.fit(X_train, y_train)

#Acuraria do modelo
st.subheader('Acuracia do modelo')
st.write(accuracy_score(y_test, dtc.predict(X_test)) * 100)

#Previsão
prediction = dtc.predict(user_input_variables)

#mostrando a previsão se vier 0 ele não tem se vier 1 ele tem

st.subheader('Previsão: ')
st.write(prediction)
