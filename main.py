from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import uvicorn

app = FastAPI()

# Permitir CORS para todos os domínios (para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carregar o CSV em um DataFrame do pandas
csv_path = r"C:\Users\Softex\Desktop\Nova pasta\CTE - Copia.csv"
df = pd.read_csv(csv_path)

# Classe para o modelo de dados
class DataFrameData(BaseModel):
    data: list

# Endpoint para obter os nomes das colunas
@app.get("/columns")
def get_columns():
    return {"columns": df.columns.tolist()}

# Endpoint para obter os dados do dataframe baseado na coluna escolhida
@app.get("/data/{column}", response_model=DataFrameData)
def get_data(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    data = df[column].dropna().tolist()
    return {"data": data}

# Endpoint para obter a quantidade de elementos únicos por coluna
@app.get("/unique_counts/{column}")
def get_unique_counts(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    unique_counts = df[column].value_counts().to_dict()
    return {"unique_counts": unique_counts}

# Endpoint para obter dados estruturados para o gráfico geográfico
@app.get("/map_data/{column}")
def get_map_data(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    data = df[column].dropna().value_counts().to_dict()
    map_data = [{"state": state, "value": value} for state, value in data.items()]
    return {"data": map_data}

# Endpoint para obter a média dos valores de uma coluna
@app.get("/mean/{column}")
def get_mean(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    mean_value = df[column].mean()
    return {"mean": mean_value}

# Endpoint para obter a mediana dos valores de uma coluna
@app.get("/median/{column}")
def get_median(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    median_value = df[column].median()
    return {"median": median_value}

# Endpoint para obter o desvio padrão dos valores de uma coluna
@app.get("/std_dev/{column}")
def get_std_dev(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    std_dev_value = df[column].std()
    return {"std_dev": std_dev_value}

# Endpoint para obter os valores mínimos e máximos de uma coluna
@app.get("/min_max/{column}")
def get_min_max(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    min_value = df[column].min()
    max_value = df[column].max()
    return {"min": min_value, "max": max_value}

# Endpoint para obter o resumo estatístico das colunas numéricas
@app.get("/summary")
def get_summary():
    summary = df.describe(include='all').to_dict()
    return {"summary": summary}

# Endpoint para obter a correlação entre duas colunas numéricas
@app.get("/correlation/{column1}/{column2}")
def get_correlation(column1: str, column2: str):
    if column1 not in df.columns or column2 not in df.columns:
        raise HTTPException(status_code=404, detail="Column(s) not found")
    if not pd.api.types.is_numeric_dtype(df[column1]) or not pd.api.types.is_numeric_dtype(df[column2]):
        raise HTTPException(status_code=400, detail="One or both columns are not numeric")
    correlation = df[column1].corr(df[column2])
    return {"correlation": correlation}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
