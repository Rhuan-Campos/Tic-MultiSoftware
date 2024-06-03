import streamlit as st
import pandas as pd
import requests
import altair as alt

# Configuração da página
image_logo = "assets/MultiMDFe.png"
st.set_page_config(page_title="MultiMDFe", page_icon=image_logo, layout="wide")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    st.markdown(" ")
with c2: 
    st.image(image_logo, width=200)
with c3:
    st.markdown(" ")

# Selecionar data e hora
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Selecione a data inicial")
with col2:
    end_date = st.date_input("Selecione a data final")

def get_data_by_column(table_name, column_name):
    try:
        response = requests.get(f"http://127.0.0.1:8501/get-list/{table_name}/{column_name}")
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

table_name = "dbo.T_MDFE"
column_name = "dbo.MDF_DATAEMISSAO"
df = get_data_by_column(table_name, column_name)

# Verificar se há dados
if df.empty:
    st.write("Nenhum dado encontrado.")
else:
    # Converter a coluna de data para datetime
    df['dbo.MDF_DATAEMISSAO'] = pd.to_datetime(df['dbo.MDF_DATAEMISSAO'], format='%Y/%m/%d %H:%M:%S')

    # Filtrar dados por data selecionada
    filtered_df = df[(df['dbo.MDF_DATAEMISSAO'] >= pd.to_datetime(start_date)) & (df['dbo.MDF_DATAEMISSAO'] <= pd.to_datetime(end_date))]

    # Verificar se há dados no período selecionado
    if filtered_df.empty:
        st.write("Nenhum dado encontrado para o período selecionado.")
    else:
        # Gráfico
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x='dbo.MDF_DATAEMISSAO:T',
            y=alt.Y('count()', title='Contagem'),
            tooltip=['dbo.MDF_DATAEMISSAO', 'count()']
        ).properties(
            title='Notas Emitidas por Período',
            width=800,
            height=400
        ).interactive()

        st.altair_chart(chart, use_container_width=True)

