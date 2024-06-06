import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from calcularCSV import filtrar_por_periodo, calcular_diferenca_tempo

dataFrame = st.session_state['data']

# Converter as colunas de data e hora para o tipo datetime
dataFrame['MDF_DATA_EMISSAO'] = pd.to_datetime(dataFrame['MDF_DATA_EMISSAO'])
dataFrame['MDF_DATA_AUTORIZACAO'] = pd.to_datetime(dataFrame['MDF_DATA_AUTORIZACAO'])

# Calcular o tempo de autorização em minutos
calcular_diferenca_tempo(dataFrame, 'MDF_DATA_EMISSAO', 'MDF_DATA_AUTORIZACAO', 'Tempo_Autorizacao')
dataFrame['Tempo_Autorizacao_Minutos'] = dataFrame['Tempo_Autorizacao'].dt.total_seconds() / 60
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Selecione a data inicial")
with col2:
    end_date = st.date_input("Selecione a data final")

st.title('Análise do Tempo de Autorização de MDF')

# Filtrar dados pelo período selecionado
df_filtrado = filtrar_por_periodo(dataFrame, 'MDF_DATA_EMISSAO', start_date, end_date)

# Estatísticas descritivas
st.write("Estatísticas Descritivas", df_filtrado['Tempo_Autorizacao_Minutos'].describe())
#Gráfico de distribuição do tempo de autorização usando Matplotlib
plt.figure(figsize=(10, 6))
plt.hist(df_filtrado['Tempo_Autorizacao_Minutos'], bins=50, edgecolor='black')
plt.title('Distribuição do Tempo de Autorização')
plt.xlabel('Tempo de Autorização (minutos)')
plt.ylabel('Frequência')
st.pyplot(plt)