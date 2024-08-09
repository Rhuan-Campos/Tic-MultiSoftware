from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import uvicorn
import os

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

csv_path = r"C:\\Users\\Softex\\Desktop\\banco de daods\\CTE - Copia.csv"

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    raise FileNotFoundError(f"O arquivo {csv_path} não foi encontrado.")

@app.get("/")
def read_root():
    return {"FastApi funcionando"}

class DataFrameData(BaseModel):
    data: list

@app.get("/columns")
def get_columns():
    return {"columns": df.columns.tolist()}

@app.get("/data/{column}", response_model=DataFrameData)
def get_data(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    data = df[column].dropna().tolist()
    return {"data": data}

@app.get("/unique_counts/{column}")
def get_unique_counts(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    unique_counts = df[column].value_counts().to_dict()
    return {"unique_counts": unique_counts}

@app.get("/mean/{column}")
def get_mean(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    mean_value = df[column].mean()
    return {"mean": mean_value}

@app.get("/median/{column}")
def get_median(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    median_value = df[column].median()
    return {"median": median_value}

@app.get("/std_dev/{column}")
def get_std_dev(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    std_dev_value = df[column].std()
    return {"std_dev": std_dev_value}

@app.get("/min_max/{column}")
def get_min_max(column: str):
    if column not in df.columns:
        raise HTTPException(status_code=404, detail="Column not found")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise HTTPException(status_code=400, detail="Column is not numeric")
    min_value = df[column].min()
    max_value = df[column].max()
    return {"min": min_value, "max": max_value}

@app.get("/summary")
def get_summary():
    summary = df.describe(include='all').to_dict()
    return {"summary": summary}

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
