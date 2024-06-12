import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import functions as func  # Importar as funções personalizadas do arquivo functions.py
#
# Função para obter os dados da API usando a função definida em functions.py
print("Carregando dados da API...")
df = func.get_data_by_column('MDF', 'MDF_DATA_EMISSAO,MDF_DATA_AUTORIZACAO')

# Converter as colunas de data e hora para o tipo datetime
df['MDF_DATA_EMISSAO'] = pd.to_datetime(df['MDF_DATA_EMISSAO'])
df['MDF_DATA_AUTORIZACAO'] = pd.to_datetime(df['MDF_DATA_AUTORIZACAO'])
df.info()#ver se ta convertendo certo

# Calcular o tempo de autorização em minutos
df['Tempo_Autorizacao_Minutos'] = (df['MDF_DATA_AUTORIZACAO'] - df['MDF_DATA_EMISSAO']).dt.total_seconds() / 60

# Estatísticas Descritivas
estatisticas_descritivas = df['Tempo_Autorizacao_Minutos'].describe()
print(estatisticas_descritivas)

# Histograma para visualização
plt.hist(df['Tempo_Autorizacao_Minutos'], bins=50, edgecolor='black')
plt.title('Distribuição do Tempo de Autorização')
plt.xlabel('Tempo de Autorização (minutos)')
plt.ylabel('Frequência')
plt.show()




# Funções de manipulação de dados
def validar_e_formatar_data(data_str):
    try:
        data_obj = pd.to_datetime(data_str)
        return data_obj.strftime('%d/%m/%Y %H:%M:%S')
    except ValueError:
        return None
    
    
    

def calcular_diferenca_tempo(df, col_start, col_end, nova_coluna):
    """
    Calcula a diferença de tempo entre duas colunas datetime64 em um DataFrame
    e adiciona uma nova coluna com essa diferença.

    :param df: DataFrame do Pandas
    :param col_start: Nome da coluna de início
    :param col_end: Nome da coluna de fim
    :param nova_coluna: Nome da nova coluna que armazenará a diferença de tempo
    """
    df[nova_coluna] = (pd.to_datetime(df[col_end]) - pd.to_datetime(df[col_start]))
    
    
    

def filtrar_por_ano(df, coluna_data, ano):
    """
    Filtra um DataFrame por um mês e ano específicos.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser filtrado.
    ano (int): O ano para filtrar.
    mes (int): O mês para filtrar.
    coluna_data (str): O nome da coluna de data.

    Retorna:
    pd.DataFrame: O DataFrame filtrado.
    """
    # Converta a coluna para datetime se ainda não estiver nesse formato
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    
    # Filtre os dados para o mês e ano especificados
    df_filtrado = df[df[coluna_data].dt.year == ano]
    return df_filtrado



def filtrar_por_semestre(df, coluna_data, ano, semestre, nova_coluna):
    """
    Filtra um DataFrame por um semestre e ano específicos e adiciona uma nova coluna indicando as entradas filtradas.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser filtrado.
    coluna_data (str): O nome da coluna de data.
    ano (int): O ano para filtrar.
    semestre (int): O semestre para filtrar (1 para primeiro semestre, 2 para segundo semestre).
    nova_coluna (str): O nome da nova coluna a ser adicionada.

    Retorna:
    pd.DataFrame: O DataFrame filtrado com a nova coluna.
    """
    df[coluna_data] = pd.to_datetime(df[coluna_data])



    # Define os meses que pertencem a cada semestre
    meses_primeiro_semestre = [1, 2, 3, 4, 5, 6]
    meses_segundo_semestre = [7, 8, 9, 10, 11, 12]

    # Filtra os dados para o semestre e ano especificados
    if semestre == 1:
        meses_semestre = meses_primeiro_semestre
    elif semestre == 2:
        meses_semestre = meses_segundo_semestre
    else:
        raise ValueError("Semestre deve ser 1 ou 2")

    # Marca as entradas que correspondem ao semestre e ano especificados
    filtro = (df[coluna_data].dt.year == ano) & (df[coluna_data].dt.month.isin(meses_semestre))
    df_filtrado = df[filtro].copy()
    df_filtrado[nova_coluna] = True

    return df_filtrado

def filtrar_por_trimestre(df, coluna_data, ano, semestre):
    """
    Filtra um DataFrame por um semestre e ano específicos.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser filtrado.
    coluna_data (str): O nome da coluna de data.
    ano (int): O ano para filtrar.
    semestre (int): O semestre para filtrar (1 para primeiro semestre, 2 para segundo semestre).

    Retorna:
    pd.DataFrame: O DataFrame filtrado.
    """
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    
    

    # Define os meses que pertencem a cada trimestre
    meses_primeiro_trimestre = [1, 2, 3]
    meses_segundo_trimestre = [ 4, 5, 6]
    meses_terceiro_trimestre = [7, 8, 9]
    meses_quarto_trimestre = [ 10, 11, 12]
    
    

    # Filtra os dados para o trimestre e ano especificados
    if semestre == 1:
        meses_trimestre = meses_primeiro_trimestre
    elif semestre == 2:
        meses_trimestre = meses_segundo_trimestre
    elif semestre == 3:
        meses_trimestre = meses_terceiro_trimestre
    elif semestre == 4:
        meses_trimestre = meses_quarto_trimestre
    else:
        raise ValueError("trimestre deve ser 1, 2, 3 ou 4 .")

    df_filtrado = df[df[coluna_data].dt.year == ano]
    meses_semestre = [1, 2, 3, 4, 5, 6]  # Define os meses que pertencem a cada semestre
    df_filtrado = df_filtrado[df_filtrado[coluna_data].dt.month.isin(meses_semestre)]

    return df_filtrado



def filtrar_por_mes(df, coluna_data, ano, mes):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    df_filtrado = df[(df[coluna_data].dt.month == mes) & (df[coluna_data].dt.year == ano)]
    return df_filtrado



def filtrar_por_hora(df, coluna_data, ano, mes, dia, hora):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    df_filtrado = df[(df[coluna_data].dt.year == ano) &
                    (df[coluna_data].dt.month == mes) &
                    (df[coluna_data].dt.day == dia) &
                    (df[coluna_data].dt.hour == hora)]
    return df_filtrado




def filtrar_por_periodo(df, coluna_data, data_inicio, data_fim):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    df_filtrado = df[(df[coluna_data] >= data_inicio) & (df[coluna_data] <= data_fim)]
    return df_filtrado




def criar_colunas_ano_semestre_mes(df, coluna_data):
    df[coluna_data] = pd.to_datetime(df[coluna_data])
    df['Ano'] = df[coluna_data].dt.year
    df['Semestre'] = df[coluna_data].dt.quarter
    df['Mes'] = df[coluna_data].dt.month
    return df 






# Aplicar validação e formatação de data
print("Validando e formatando datas...")
df['MDF_DATA_EMISSAO'] = df['MDF_DATA_EMISSAO'].apply(validar_e_formatar_data)
df['MDF_DATA_AUTORIZACAO'] = df['MDF_DATA_AUTORIZACAO'].apply(validar_e_formatar_data)

# Calcular o tempo
print("Calculando tempo de autorização...")
calcular_diferenca_tempo(df, 'MDF_DATA_EMISSAO', 'MDF_DATA_AUTORIZACAO', 'Tempo_Autorizacao')

# Converter a diferença de tempo para minutos para o histograma
print("Convertendo para minutos...")
df['Tempo_Autorizacao_Minutos'] = df['Tempo_Autorizacao'].dt.total_seconds() / 60

# Histograma para visualização
print("Gerando histograma...")
plt.hist(df['Tempo_Autorizacao_Minutos'], bins=50, edgecolor='black')
plt.title('Distribuição do Tempo de Autorização')
plt.xlabel('Tempo de Autorização (minutos)')
plt.ylabel('Frequência')
plt.show()

# Filtrar valores negativos e outliers (limitar ao intervalo razoável de 0 a 100 minutos)
print("Filtrando valores negativos e outliers...")
df_filtrado = df[(df['Tempo_Autorizacao_Minutos'] >= 0) & (df['Tempo_Autorizacao_Minutos'] <= 100)]

# Recalcular as estatísticas descritivas
print("Recalculando estatísticas descritivas...")
estatisticas_descritivas_filtradas = df_filtrado['Tempo_Autorizacao_Minutos'].describe()

# Novo histograma para visualização
print("Gerando histograma filtrado...")
plt.hist(df_filtrado['Tempo_Autorizacao_Minutos'], bins=50, edgecolor='black')
plt.title('Distribuição do Tempo de Autorização (Filtrada)')
plt.xlabel('Tempo de Autorização (minutos)')
plt.ylabel('Frequência')
plt.show()

# Imprimir estatísticas descritivas filtradas
print("Estatísticas descritivas filtradas:")
print(estatisticas_descritivas_filtradas)

# Nova Análise Mensal
print("Nova Análise Mensal:")
filtrado_Mes = filtrar_por_mes(df_filtrado, 'MDF_DATA_EMISSAO', 2020, 3)
print(filtrado_Mes)

# Nova Análise Trimestral
print("Nova Análise Trimestral:")
filtrado_Tri = filtrar_por_trimestre(df_filtrado, 'MDF_DATA_EMISSAO', 2020, 1)
print(filtrado_Tri)

# Nova Análise Semestral
print("Nova Análise Semestral:")
filtrado_Semestral = filtrar_por_semestre(df_filtrado, 'MDF_DATA_EMISSAO', 2020, 1, 'Semestre')
print(filtrado_Semestral)

# Nova Análise Anual
print("Nova Análise Anual:")
filtrado_Anual = filtrar_por_ano(df_filtrado, 'MDF_DATA_EMISSAO', 2020)
print(filtrado_Anual)

# Nova Análise por Período
print("Nova Análise por Período:")
filtrado_Periodo = filtrar_por_periodo(df_filtrado, 'MDF_DATA_EMISSAO', '2020-01-01', '2020-04-01')
print(filtrado_Periodo)

# Adicionar colunas de Ano, Semestre e Mês
print("Adicionando colunas de Ano, Semestre e Mês:")
df_com_colunas = criar_colunas_ano_semestre_mes(df_filtrado, 'MDF_DATA_EMISSAO')
print(df_com_colunas.head())



#Desvio padrão
def encontrar_e_mostrar_outliers(df, coluna):
    """
    Esta função identifica e exibe outliers de uma coluna específica de um DataFrame.

    Parâmetros:
    df (pandas.DataFrame): O DataFrame contendo os dados.
    coluna (str): O nome da coluna para identificar os outliers.

    Retorna:
    pandas.DataFrame: Um DataFrame contendo os outliers.
    """
    # Calcular os quartis e os limites para identificar os outliers
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1

    lim_inferior = Q1 - 1.5 * IQR
    lim_superior = Q3 + 1.5 * IQR

    # Identificar os outliers
    outliers = df[(df[coluna] < lim_inferior) | (df[coluna] > lim_superior)]
    print(f"Outliers encontrados na coluna {coluna}:")
    print(outliers)

    # Visualizar os outliers com um boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df[coluna])
    plt.title(f'Boxplot da Coluna {coluna}')
    plt.show()

    return outliers