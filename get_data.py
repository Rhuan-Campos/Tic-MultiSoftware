import pandas as pd
from fastapi import FastAPI, HTTPException
from acessar_banco import DatabaseConnector
from fastapi.encoders import jsonable_encoder
from acessar_banco import multi_db_config, rhuan_db_config

app = FastAPI()

@app.get("/get-list/{table_name}")
def get_list(table_name: str):
    try:
        rhuan_connector = DatabaseConnector(**rhuan_db_config)
        df = pd.read_sql(f"SELECT * FROM dbo.{table_name}", rhuan_connector.engine)
        rhuan_connector.close_connection()
        
        # Substituir valores "NaN" por uma string vazia
        df = df.fillna("")
        
        # Converter DataFrame para uma lista de dicionários
        data = df.to_dict(orient='records')
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/get-list/{table_name}/{column_name}")
def get_list(table_name: str, column_name: str):
    try:
        rhuan_connector = DatabaseConnector(**rhuan_db_config)
        df = pd.read_sql(f"SELECT {column_name} FROM dbo.{table_name} WHERE {column_name} IS NOT NULL", rhuan_connector.engine)
        rhuan_connector.close_connection()
        
        # Substituir valores "NaN" por uma string vazia
        df = df.fillna("")
        
        # Converter DataFrame para uma lista de dicionários
        data = df.to_dict(orient='records')
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-list/{table_name}/{column_name}/{value}")
def get_list(table_name: str, column_name: str, value: int):
    try:
        rhuan_connector = DatabaseConnector(**rhuan_db_config)
        # Verificar o tipo de dado da coluna
        df = pd.read_sql(f"SELECT * FROM dbo.{table_name} WHERE {column_name} = '{value}'", rhuan_connector.engine)
        rhuan_connector.close_connection()
        
        # Substituir valores "NaN" por uma string vazia
        df = df.fillna("")
        
        # Converter DataFrame para uma lista de dicionários
        data = df.to_dict(orient='records')
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))