import streamlit as st
import requests
import pandas as pd
import altair as alt

image_logo = "assets/MultiCTe.png"
st.set_page_config(page_title="MultiCTe", page_icon=image_logo, layout="wide")

# Exibir o logo no centro
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.markdown(" ")
with c2:
    st.image(image_logo)
with c3:
    st.markdown(" ")

# Seleção de datas
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Selecione a data inicial")
with col2:
    end_date = st.date_input("Selecione a data final")

def get_data_by_column(table_name, column_name):
    try:
        response = requests.get(f"http://127.0.0.1:8000/get-list/{table_name}/{column_name}")
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except requests.exceptions.HTTPError as err:
        st.error(f"Erro HTTP: {err}")
    except requests.exceptions.RequestException as err:
        st.error(f"Erro ao fazer a requisição: {err}")
    except Exception as err:
        st.error(f"Erro: {err}")
    return pd.DataFrame()

table_name = "T_CTE"
column_name = "CON_DATAHORAEMISSAO"
df = get_data_by_column(table_name, column_name)

# Verificar se há dados
if df.empty:
    st.write("Nenhum dado encontrado.")
else:
    # Converter a coluna de data para datetime
    df['CON_DATAHORAEMISSAO'] = pd.to_datetime(df['CON_DATAHORAEMISSAO'])

    # Filtrar dados por data selecionada
    filtered_df = df[(df['CON_DATAHORAEMISSAO'] >= pd.to_datetime(start_date)) & (df['CON_DATAHORAEMISSAO'] <= pd.to_datetime(end_date))]

    # Verificar se há dados no período selecionado
    if filtered_df.empty:
        st.write("Nenhum dado encontrado para o período selecionado.")
    else:
        # Criar gráfico de barras usando Altair
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x='CON_DATAHORAEMISSAO:T',
            y='count:Q',
            tooltip=['CON_DATAHORAEMISSAO', 'count']
        ).properties(
            title='Notas Emitidas por Período',
            width=800,
            height=400
        ).interactive()

        # Exibir gráfico
        st.altair_chart(chart, use_container_width=True)
