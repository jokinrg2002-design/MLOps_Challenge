# MLOps_Challenge
# 🏎️ F1 MLOps: Predicción de Top 10 (Pipeline de Producción)

Este repositorio contiene la resolución del Challenge de Arquitectura MLOps. El objetivo principal es construir un flujo de trabajo de Machine Learning.

## 🎯 Objetivo del Proyecto
Predecir si un piloto de Fórmula 1 terminará en la zona de puntos (Top 10) basándose en su posición de salida (`grid`) y el año de la carrera (`year`).

## 🛠️ Arquitectura y Tecnologías
1. **Preparación de Datos:** Extracción y limpieza de datos históricos de F1 (Pilotos, Carreras, Clasificaciones) usando `Pandas`.
2. **Experimentación (MLflow):** 
   - Implementación de un Grid Search automatizado evaluando múltiples algoritmos (Regresión Logística, Random Forest, Gradient Boosting).
   - Uso de **MLflow Tracking** para el registro de hiperparámetros y métricas (`accuracy`, `precision`).
3. **Puesta en Producción (FastAPI):**
   - Creación de una API RESTful.
   - Uso de **MLflow Model Registry** para que la API cargue dinámicamente el mejor modelo (`model.pkl`) en memoria durante el arranque, aislando el entorno de entrenamiento del de producción.

## 📂 Estructura del Repositorio
* `/notebooks`: Cuaderno de Jupyter (`.ipynb`) con el pipeline completo (ETL, Entrenamiento, MLflow Tracking).
* `/src`: Código fuente de la API (`api.py`) construida con FastAPI.
* `/data`: CSV originales y el CSV tratado final utilizado para la eleboración del modelo.
* `requirements.txt`: Dependencias necesarias para ejecutar el entorno.
