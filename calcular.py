# import streamlit as st
# import pandas as pd
# import numpy as np
# import requests

# # Função para obter uma coluna específica da tabela
# def get_data_by_column(table_name, column_name):
#     try:
#         response = requests.get(f"http://127.0.0.1:8000/get-list/{table_name}/{column_name}")
#         response.raise_for_status()  
#         data = response.json()
#         return pd.DataFrame(data)
#     except requests.exceptions.HTTPError as err:
#         st.error(f"Erro HTTP: {err}")
#     except requests.exceptions.RequestException as err:
#         st.error(f"Erro ao fazer a requisição: {err}")
#     except Exception as err:
#         st.error(f"Erro: {err}")
#     return pd.DataFrame()   

# # Função para detectar outliers usando percentis
# def detect_outliers_percentile(data, threshold_lower=5, threshold_upper=95):

#     Q1 = np.percentile(data, threshold_lower)
#     Q3 = np.percentile(data, threshold_upper)
#     IQR = Q3 - Q1
#     limite_inferior = Q1 - 1.5 * IQR
#     limite_superior = Q3 + 1.5 * IQR
    
#     outliers = data[(data < limite_inferior) | (data > limite_superior)]
    
#     return outliers

# # Obter as colunas 'EMISSAO' e 'AUTORIZAÇÂO'
# emissao_df = get_data_by_column('sua_tabela', 'EMISSAO')
# autorizacao_df = get_data_by_column('sua_tabela', 'AUTORIZAÇÂO')

# # Verificar se os dados foram obtidos corretamente
# st.write("Dados de EMISSAO:", emissao_df)
# st.write("Dados de AUTORIZAÇÂO:", autorizacao_df)

# # Combinar as colunas em um único DataFrame
# df = pd.concat([emissao_df, autorizacao_df], axis=1)
# df.columns = ['EMISSAO', 'AUTORIZAÇÂO']

# # Converter as colunas para o formato de data/hora
# df['EMISSAO'] = pd.to_datetime(df['EMISSAO'])
# df['AUTORIZAÇÂO'] = pd.to_datetime(df['AUTORIZAÇÂO'])

# # Calcular o tempo entre emissão e autorização em horas
# df['TEMPO'] = (df['AUTORIZAÇÂO'] - df['EMISSAO']).dt.total_seconds() / 3600

# # Verificar os dados calculados
# st.write("Dados combinados e calculados:", df)

# # Detectar outliers usando percentis
# outliers_percentil = detect_outliers_percentile(df['TEMPO'])

# # Calcular estatísticas descritivas
# media = df['TEMPO'].mean()
# mediana = df['TEMPO'].median()
# desvio_padrao = df['TEMPO'].std()

# # Exibir estatísticas e outliers
# st.write(f"Média: {media} horas")
# st.write(f"Mediana: {mediana} horas")
# st.write(f"Desvio Padrão: {desvio_padrao} horas")
# st.write("Outliers detectados:", outliers_percentil)


# # Identificar outliers usando o método do IQR
# Q1 = df['TEMPO'].quantile(0.25)
# Q3 = df['TEMPO'].quantile(0.75)
# IQR = Q3 - Q1
# limite_inferior = Q1 - 1.5 * IQR
# limite_superior = Q3 + 1.5 * IQR
# outliers = df[(df['TEMPO'] < limite_inferior) | (df['TEMPO'] > limite_superior)]

# st.write(f"Média: {media} horas")
# st.write(f"Mediana: {mediana} horas")
# st.write(f"Desvio Padrão: {desvio_padrao} horas")
# st.write("Outliers detectados:", outliers)
