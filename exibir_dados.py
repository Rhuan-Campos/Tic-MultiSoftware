import streamlit as st
import pandas as pd
import requests
from functions import get_data, get_data_by_column, get_data_by_column_value


st.title("Visualizador de Tabelas do Banco de Dados")

#Streamlit básico
st.sidebar.header("Configurações")
table_name = st.sidebar.text_input("Nome da Tabela")
column_name = st.sidebar.text_input("Nome da Coluna")
value = str(st.sidebar.text_input("Valor"))

#Verificar se os campos foram preenchidos
if st.sidebar.button("Carregar Tabela"):
    if table_name and not column_name and not value:
        df = get_data(table_name)
        if not df.empty:
            st.write(f"Dados da Tabela: {table_name}")
            st.dataframe(df)
        else:
            st.write("Nenhum dado encontrado ou erro ao carregar a tabela.")
    else:
        if column_name and not value:
            df = get_data_by_column(table_name, column_name)
        elif column_name and value:
            df = get_data_by_column_value(table_name, column_name, value)
        else:
            df = get_data(table_name)
        
        if not df.empty:
            st.write(f"Dados da Tabela: {table_name}")
            st.dataframe(df)
        else:
            st.write("Nenhum dado encontrado ou erro ao carregar a tabela.")