# Função para obter toda a tabela
import streamlit as st
import pandas as pd
import requests

def get_data(table_name):
    try:
        response = requests.get(f"http://127.0.0.1:8000/get-list/{table_name}")
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

# Função para obter uma coluna específica da tabela
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

# Função para obter dados de uma coluna específica com um valor específico
def get_data_by_column_value(table_name, column_name, value):
    try:
        response = requests.get(f"http://127.0.0.1:8000/get-list/{table_name}/{column_name}/{value}")
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
