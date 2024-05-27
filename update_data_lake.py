import pandas as pd
from fastapi import FastAPI, HTTPException
from acessar_banco import DatabaseConnector
from fastapi.encoders import jsonable_encoder
from acessar_banco import multi_db_config, rhuan_db_config
#Microsserviço que Atualiza a Base de Dados

app = FastAPI()

@app.put("/update-list/{table_name}")
def update_list(table_name: str):
    try:
        multi_connector = DatabaseConnector(**multi_db_config)
        rhuan_connector = DatabaseConnector(**rhuan_db_config)
        df = pd.read_sql(f"SELECT * FROM dbo.{table_name}", multi_connector.engine)
        multi_connector.close_connection()
        df.to_sql(table_name, rhuan_connector.engine, if_exists='replace', index=False)
        df_copiado = pd.read_sql(f"SELECT * FROM dbo.{table_name}", rhuan_connector.engine)
        rhuan_connector.close_connection()
        return df_copiado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-table/{table_name}")
def delete_table(table_name: str):
    try:
        rhuan_connector = DatabaseConnector(**rhuan_db_config)
        pd.read_sql(f"DROP TABLE dbo.{table_name}", rhuan_connector.engine)
        rhuan_connector.close_connection()
        return {"message": f"Table {table_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))