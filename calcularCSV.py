import pandas as pd
import streamlit as st

# Supomos que o DataFrame já está carregado em st.session_state['data']
df = st.session_state['data']

# Converter as colunas de data e hora para o tipo datetime
df['MDF_DATA_EMISSAO'] = pd.to_datetime(df['MDF_DATA_EMISSAO'])
df['MDF_DATA_AUTORIZACAO'] = pd.to_datetime(df['MDF_DATA_AUTORIZACAO'])
#df.info()  Ver se está convertendo certo

# Calcular o tempo de autorização em minutos
df['Tempo_Autorizacao_Minutos'] = (df['MDF_DATA_AUTORIZACAO'] - df['MDF_DATA_EMISSAO']).dt.total_seconds() / 60

# Estatísticas Descritivas
#estatisticas_descritivas = df['Tempo_Autorizacao_Minutos'].describe()
#st.write("Estatísticas Descritivas:", estatisticas_descritivas)

# Funções de manipulação de dados
def validar_e_formatar_data(data_str):
    try:
        data_obj = pd.to_datetime(data_str)
        return data_obj.strftime('%d/%m/%Y %H:%M:%S')
    except ValueError:
        return None

def calcular_diferenca_tempo(df, col_start, col_end, nova_coluna):
    df[nova_coluna] = (pd.to_datetime(df[col_end]) - pd.to_datetime(df[col_start]))

def filtrar_por_ano(df, coluna_data, ano):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    return df[df[coluna_data].dt.year == ano]

def filtrar_por_semestre(df, coluna_data, ano, semestre, nova_coluna):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    meses_primeiro_semestre = [1, 2, 3, 4, 5, 6]
    meses_segundo_semestre = [7, 8, 9, 10, 11, 12]
    if semestre == 1:
        meses_semestre = meses_primeiro_semestre
    elif semestre == 2:
        meses_semestre = meses_segundo_semestre
    else:
        raise ValueError("Semestre deve ser 1 ou 2")
    filtro = (df[coluna_data].dt.year == ano) & (df[coluna_data].dt.month.isin(meses_semestre))
    df_filtrado = df[filtro].copy()
    df_filtrado[nova_coluna] = True
    return df_filtrado

def filtrar_por_trimestre(df, coluna_data, ano, trimestre):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    meses_primeiro_trimestre = [1, 2, 3]
    meses_segundo_trimestre = [4, 5, 6]
    meses_terceiro_trimestre = [7, 8, 9]
    meses_quarto_trimestre = [10, 11, 12]
    if trimestre == 1:
        meses_trimestre = meses_primeiro_trimestre
    elif trimestre == 2:
        meses_trimestre = meses_segundo_trimestre
    elif trimestre == 3:
        meses_trimestre = meses_terceiro_trimestre
    elif trimestre == 4:
        meses_trimestre = meses_quarto_trimestre
    else:
        raise ValueError("Trimestre deve ser 1, 2, 3 ou 4")
    df_filtrado = df[(df[coluna_data].dt.year == ano) & (df[coluna_data].dt.month.isin(meses_trimestre))]
    return df_filtrado

def filtrar_por_mes(df, coluna_data, ano, mes):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    return df[(df[coluna_data].dt.month == mes) & (df[coluna_data].dt.year == ano)]

def filtrar_por_hora(df, coluna_data, ano, mes, dia, hora):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    return df[(df[coluna_data].dt.year == ano) &
                (df[coluna_data].dt.month == mes) &
                (df[coluna_data].dt.day == dia) &
                (df[coluna_data].dt.hour == hora)]

def filtrar_por_periodo(df, coluna_data, data_inicio, data_fim):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    return df[(df[coluna_data] >= data_inicio) & (df[coluna_data] <= data_fim)]

def criar_colunas_ano_semestre_mes(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    df['Ano'] = df[coluna_data].dt.year
    df['Semestre'] = df[coluna_data].dt.quarter
    df['Mes'] = df[coluna_data].dt.month
    return df

# Aplicar validação e formatação de data
df['MDF_DATA_EMISSAO'] = df['MDF_DATA_EMISSAO'].apply(validar_e_formatar_data)
df['MDF_DATA_AUTORIZACAO'] = df['MDF_DATA_AUTORIZACAO'].apply(validar_e_formatar_data)

# Calcular o tempo
calcular_diferenca_tempo(df, 'MDF_DATA_EMISSAO', 'MDF_DATA_AUTORIZACAO', 'Tempo_Autorizacao')

# Converter a diferença de tempo para minutos para o histograma
df['Tempo_Autorizacao_Minutos'] = df['Tempo_Autorizacao'].dt.total_seconds() / 60

# Histograma para visualização usando Streamlit
#st.write("Histograma do Tempo de Autorização")
#st.bar_chart(df['Tempo_Autorizacao_Minutos'].value_counts().sort_index())

# Filtrar valores negativos e outliers (limitar ao intervalo razoável de 0 a 100 minutos)
df_filtrado = df[(df['Tempo_Autorizacao_Minutos'] >= 0) & (df['Tempo_Autorizacao_Minutos'] <= 100)]

# Recalcular as estatísticas descritivas
estatisticas_descritivas_filtradas = df_filtrado['Tempo_Autorizacao_Minutos'].describe()

# Novo histograma para visualização usando Streamlit
#st.write("Novo Histograma do Tempo de Autorização (Filtrada)")
#st.bar_chart(df_filtrado['Tempo_Autorizacao_Minutos'].value_counts().sort_index())

# Imprimir estatísticas descritivas filtradas
#st.write("Estatísticas descritivas filtradas:")
#st.write(estatisticas_descritivas_filtradas)

# Nova Análise Mensal
filtrado_Mes = filtrar_por_mes(df_filtrado, 'MDF_DATA_EMISSAO', 2020, 3)
#st.write("Nova Análise Mensal:")
#st.write(filtrado_Mes)

# Nova Análise Trimestral
filtrado_Tri = filtrar_por_trimestre(df_filtrado, 'MDF_DATA_EMISSAO', 2020, 1)
#st.write("Nova Análise Trimestral:")
#st.write(filtrado_Tri)

# Nova Análise Semestral
filtrado_Semestral = filtrar_por_semestre(df_filtrado, 'MDF_DATA_EMISSAO', 2020, 1, 'Semestre')
#st.write("Nova Análise Semestral:")
#st.write(filtrado_Semestral)

# Nova Análise Anual
filtrado_Anual = filtrar_por_ano(df_filtrado, 'MDF_DATA_EMISSAO', 2020)
#st.write("Nova Análise Anual:")
#st.write(filtrado_Anual)

# Nova Análise por Período
filtrado_Periodo = filtrar_por_periodo(df_filtrado, 'MDF_DATA_EMISSAO', '2020-01-01', '2020-04-01')
#st.write("Nova Análise por Período:")
#st.write(filtrado_Periodo)

# Adicionar colunas de Ano, Semestre e Mês
df_com_colunas = criar_colunas_ano_semestre_mes(df_filtrado, 'MDF_DATA_EMISSAO')
#st.write("Adicionando colunas de Ano, Semestre e Mês:")
#st.write(df_com_colunas.head())
