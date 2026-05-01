from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import pandas as pd

class PilotoInput(BaseModel):
    grid: int
    year: int

app = FastAPI(title="API Predictiva F1 - MLOps")
modelo_f1 = None

@app.on_event("startup")
def cargar_modelo():
    global modelo_f1
    try:
        ruta_directa = "file:///content/drive/MyDrive/f1_mlops/mlruns/505708190338931035/models/m-d99fa34fd5684fe294dca9e97467a395/artifacts"
        modelo_f1 = mlflow.sklearn.load_model(ruta_directa)
        print("Modelo cargado desde el disco duro")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")

@app.post("/predecir")
def hacer_prediccion(datos: PilotoInput):
    if modelo_f1 is None:
        return {"error": "El modelo no está cargado"}

    df_entrada = pd.DataFrame([{"grid": datos.grid, "year": datos.year}])
    prediccion = modelo_f1.predict(df_entrada)[0]
    resultado_texto = "Sí (Top 10)" if prediccion == 1 else "No (Fuera de los puntos)"

    return {
        "posicion_salida": datos.grid,
        "año_carrera": datos.year,
        "prediccion_modelo": resultado_texto
    }
