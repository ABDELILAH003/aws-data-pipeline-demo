from fastapi import FastAPI
import pandas as pd
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent  # racine du repo
DATA_PATH = BASE_DIR / "data" / "sample_data.csv"

@app.get("/")
def home():
    return {"status": "API running (local) - ready for AWS"}

@app.get("/data")
def get_data():
    df = pd.read_csv(DATA_PATH)
    return df.head(5).to_dict(orient="records")
