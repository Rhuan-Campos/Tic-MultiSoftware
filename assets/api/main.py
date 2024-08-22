from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from starlette.responses import JSONResponse
from fastapi import HTTPException
from api.database_access import DatabaseConnector 
from api.database_access import multi_db_config

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"FastApi funcionando"}

class DataFrameData(BaseModel):
    data: list

@app.get("/columns")
def get_columns():
    try:
        # Conectar ao banco de dados
        connector = DatabaseConnector(**multi_db_config)
        
        # Consulta SQL para obter as colunas da tabela
        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'T_MDFE'"
        
        # Executar a consulta e carregar os dados em um DataFrame
        df_columns = pd.read_sql(query, connector.engine)

        # Converter as colunas para uma lista
        columns = df_columns["COLUMN_NAME"].tolist()
        connector.close_connection()
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/unique_counts/{column}/{data_inicio}/{data_fim}")
def get_unique_counts(column: str, data_inicio: str, data_fim: str):
    try:
        # Converter as datas de entrada
        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD' format.")

    try:
        # Conectar ao banco de dados
        connector = DatabaseConnector(**multi_db_config)
        
        # Verifique se a coluna especificada existe na tabela
        table_name = 'T_MDFE'
        check_column_query = f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{column}'
        """
        column_check = pd.read_sql(check_column_query, connector.engine)
        if column_check.empty:
            raise HTTPException(status_code=404, detail=f"Column '{column}' not found in table '{table_name}'")

        # Consulta SQL para contar os valores únicos na coluna especificada dentro do intervalo de datas
        query = f"""
        SELECT {column}, COUNT(*) as count
        FROM dbo.{table_name}
        WHERE MDF_DATA_EMISSAO BETWEEN '{data_inicio}' AND '{data_fim}'
        GROUP BY {column}
        """
        
        # Executar a consulta e carregar os dados em um DataFrame
        df = pd.read_sql(query, connector.engine)
        
        # Verifique se o DataFrame está vazio
        if df.empty:
            connector.close_connection()
            return {"unique_counts": {}}

        # Converter o DataFrame para um dicionário
        unique_counts = df.set_index(column)['count'].to_dict()
        connector.close_connection()
        
        return {"unique_counts": unique_counts}
    except Exception as e:
        connector.close_connection()
        raise HTTPException(status_code=500, detail=str(e))
    

# @app.get("/data/filter")
# def get_filtered_data(column: str, dataInicio: str, dataFim: str):
#     try:
#         dataInicio = pd.to_datetime(dataInicio)
#         dataFim = pd.to_datetime(dataFim)
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Formato de data inválido. Use o formato 'AAAA-MM-DD'.")

#     if column not in df.columns:
#         raise HTTPException(status_code=404, detail="Coluna não encontrada")
    
#     if not pd.api.types.is_datetime64_any_dtype(df[column]):
#         raise HTTPException(status_code=400, detail="Coluna não é do tipo datetime")

#     filtered_data = df[(df[column] >= dataInicio) & (df[column] <= dataFim)]
#     if filtered_data.empty:
#         raise HTTPException(status_code=404, detail="Nenhum dado encontrado no intervalo de datas especificado")
    
#     return {"data": filtered_data.to_dict(orient='records')}


# @app.get("/data/{column}", response_model=DataFrameData)
# def get_data(column: str):
#     if column not in df.columns:
#         raise HTTPException(status_code=404, detail="Column not found")
#     data = df[column].dropna().tolist()
#     return {"data": data}



@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# @app.get("/mean/{column}")
# def get_mean(column: str):
#     if column not in df.columns:
#         raise HTTPException(status_code=404, detail="Column not found")
#     if not pd.api.types.is_numeric_dtype(df[column]):
#         raise HTTPException(status_code=400, detail="Column is not numeric")
#     mean_value = df[column].mean()
#     return {"mean": mean_value}

# @app.get("/median/{column}")
# def get_median(column: str):
#     if column not in df.columns:
#         raise HTTPException(status_code=404, detail="Column not found")
#     if not pd.api.types.is_numeric_dtype(df[column]):
#         raise HTTPException(status_code=400, detail="Column is not numeric")
#     median_value = df[column].median()
#     return {"median": median_value}

# @app.get("/std_dev/{column}")
# def get_std_dev(column: str):
#     if column not in df.columns:
#         raise HTTPException(status_code=404, detail="Column not found")
#     if not pd.api.types.is_numeric_dtype(df[column]):
#         raise HTTPException(status_code=400, detail="Column is not numeric")
#     std_dev_value = df[column].std()
#     return {"std_dev": std_dev_value}

# @app.get("/min_max/{column}")
# def get_min_max(column: str):
#     if column not in df.columns:
#         raise HTTPException(status_code=404, detail="Column not found")
#     if not pd.api.types.is_numeric_dtype(df[column]):
#         raise HTTPException(status_code=400, detail="Column is not numeric")
#     min_value = df[column].min()
#     max_value = df[column].max()
#     return {"min": min_value, "max": max_value}

# @app.get("/summary")
# def get_summary():
#     summary = df.describe(include='all').to_dict()
#     return {"summary": summary}

# @app.get("/correlation/{column1}/{column2}")
# def get_correlation(column1: str, column2: str):
#     if column1 not in df.columns or column2 not in df.columns:
#         raise HTTPException(status_code=404, detail="Column(s) not found")
#     if not pd.api.types.is_numeric_dtype(df[column1]) or not pd.api.types.is_numeric_dtype(df[column2]):
#         raise HTTPException(status_code=400, detail="One or both columns are not numeric")
#     correlation = df[column1].corr(df[column2])
#     return {"correlation": correlation}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
