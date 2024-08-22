from sqlalchemy.engine import URL
from sqlalchemy import create_engine

# Configurações Banco MultiSoftware
multi_db_config = {
    "driver_name": "ODBC Driver 17 for SQL Server",
    "server_name": "sql-multisoftware-hml.database.windows.net",
    "database_name": "sqldb-brisa-hml",
    "username": "usr_brisa_homolog",
    "password": "Multi@2024"
}

#Configurações Data Warehouse
#----------------------------

#Classes para acessar o banco de dados
class DatabaseConnector:
    #Construtor
    def __init__(self, driver_name, server_name, database_name, username, password):
        self.driver_name = driver_name
        self.server_name = server_name
        self.database_name = database_name
        self.username = username
        self.password = password
        self.engine = self.create_connection()

    # Função para criar uma conexão com o banco de dados usando SQLAlchemy (não modifique)
    def create_connection(self):
        connection_string = f"DRIVER={self.driver_name};SERVER={self.server_name};PORT=1433;DATABASE={self.database_name};UID={self.username};PWD={self.password};&autocommit=true"
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url, use_setinputsizes=False, echo=False)
        return engine
    
    def close_connection(self):
        self.engine.dispose()
        print("Conexão com o banco de dados encerrada.")
