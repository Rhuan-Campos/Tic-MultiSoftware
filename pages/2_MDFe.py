import streamlit as st
import pandas as pd
import altair as alt
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from calcularCSV import filtrar_por_periodo, calcular_diferenca_tempo, encontrar_e_mostrar_outliers

image_logo = "assets/MultiMDFe.png"
st.set_page_config(page_title="MultiCTe", page_icon=image_logo, layout="wide")


c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.markdown(" ")
with c2:
    st.image(image_logo)
with c3:
    st.markdown(" ")
    

dataFrame = st.session_state['data']

# Converter as colunas de data e hora para o tipo datetime
dataFrame['MDF_DATA_EMISSAO'] = pd.to_datetime(dataFrame['MDF_DATA_EMISSAO'])
dataFrame['MDF_DATA_AUTORIZACAO'] = pd.to_datetime(dataFrame['MDF_DATA_AUTORIZACAO'])

# minutos
calcular_diferenca_tempo(dataFrame, 'MDF_DATA_EMISSAO', 'MDF_DATA_AUTORIZACAO', 'Tempo_Autorizacao')
dataFrame['Tempo_Autorizacao_Minutos'] = dataFrame['Tempo_Autorizacao'].dt.total_seconds() / 60

# selecionar o período por datas
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Selecione a data inicial")
with col2:
    end_date = st.date_input("Selecione a data final")

# Filtrar dados pelo período selecionado
df_filtrado = filtrar_por_periodo(dataFrame, 'MDF_DATA_EMISSAO', start_date, end_date)

# Filtrar dados para que o eixo Y seja de 0 a 5 minutos
df_filtrado = df_filtrado[(df_filtrado['Tempo_Autorizacao_Minutos'] >= 0) & (df_filtrado['Tempo_Autorizacao_Minutos'] <= 5)]

# Encontrar e exibir outliers
outliers = encontrar_e_mostrar_outliers(df_filtrado, 'Tempo_Autorizacao_Minutos')

# Gráfico de média e Gráfico de outliers 
graph1, graph2= st.columns([1, 1])
with graph1:
    st.line_chart(df_filtrado[['MDF_DATA_EMISSAO', 'Tempo_Autorizacao_Minutos']].set_index('MDF_DATA_EMISSAO'))
with graph2:
    if not outliers.empty:
        scatter_chart = alt.Chart(outliers).mark_point(color='red').encode(
            x='MDF_DATA_EMISSAO:T',
            y='Tempo_Autorizacao_Minutos:Q'
        ).properties(
            width=600,
            height=400,
            title='Outliers de Tempo de Autorização'
    )
        st.altair_chart(scatter_chart)
    else:
        st.write("Nenhum outlier encontrado no período selecionado.")
    # Calcular a média do tempo de autorização
    media_tempo_autorizacao_total = df_filtrado['Tempo_Autorizacao_Minutos'].mean()
    # Definir um limite para alerta (exemplo: 1.5 vezes a média)
    limite_alerta = 2.0 * media_tempo_autorizacao_total
    # Verificar quais dias ou períodos específicos estão fora do limite
    fora_da_media = df_filtrado[df_filtrado['Tempo_Autorizacao_Minutos'] > limite_alerta]
    # Exibir alerta se houver tempos de autorização fora da média
if not fora_da_media.empty:
    st.warning("Atenção! Tempos de autorização estão muito fora da média (acima de {:.2f} minutos):".format(limite_alerta))
#    for index, row in fora_da_media.iterrows():
#        st.write(f"Data: {row['MDF_DATA_EMISSAO'].strftime('%Y-%m-%d %H:%M:%S')}, Tempo de Autorização: {row['Tempo_Autorizacao_Minutos']:.2f} minutos")

