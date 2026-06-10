# F1 MLOps: Predicción de Top 10 (Pipeline de Producción End-to-End)

Este repositorio contiene la arquitectura y solución avanzada para el Challenge de MLOps. A diferencia de un proyecto tradicional de Ciencia de Datos enfocado únicamente en la precisión del modelo, este desarrollo implementa un **pipeline de producción robusto, reproducible y desacoplado**, gobernando todo el ciclo de vida del modelo de Machine Learning (desde la gestión de datos hasta el despliegue en producción).

---

## 🎯 Objetivo del Proyecto y Enfoque de Datos

El objetivo de negocio es **predecir si un piloto de Fórmula 1 terminará en la zona de puntos (Top 10)** en base a dos variables de entrada: su posición en la parrilla de salida (`grid`) y el año del Gran Premio (`year`). 

### Gestión del Data Leakage
Para garantizar una evaluación realista en condiciones de producción, el dataset histórico se ha dividido de forma cronológica y no aleatoria:
* **Conjunto de Entrenamiento:** Datos anteriores al año 2022.
* **Conjunto de Test/Validación:** Datos del año 2022.
Este enfoque previene la fuga de información temporal y simula el comportamiento real del modelo al enfrentarse a temporadas futuras.

---

## 🛠️ Arquitectura MLOps y Desglose Tecnológico

El proyecto está estructurado en las siguientes fases:

### Fase 0: Control de Versiones de Datos (DVC)
* **Tecnología:** `DVC (Data Version Control)`
* **Explicación:** En este proyecto, DVC calcula un hash único (MD5) del archivo `f1_dataset_clean.csv` y genera un archivo de metadatos ligero (`.dvc`). Git solo trackea este puntero, mientras que los datos reales se almacenan de forma segura en un almacenamiento remoto persistente. Esto asegura la reproducibilidad absoluta haciendo que cualquier ingeniero puede recuperar la versión exacta de los datos ejecutando `dvc checkout`.

### Fase 1: ETL y Preprocesamiento Automatizado
* **Tecnología:** `Pandas`
* **Explicación:** Se limpia el ruido del dataset original eliminando registros inconsistentes. Se realiza una ingeniería de características (Feature Engineering) básica para transformar la posición final en una variable binaria (`is_points`: `1` si quedó $\le$ 10, `0` en caso contrario), adaptando el problema a un entorno de clasificación supervisada.

### Fase 2: Experimentación y Tracking Avanzado
* **Tecnología:** `MLflow Tracking` & `Scikit-Learn`
* **Explicación:** Para evitar el desarrollo a ciegas, se implementa una fase de entrenamiento competitivo utilizando un filtrado exhaustivo de hiperparámetros mediante `GridSearchCV`. Se evalúan en paralelo tres arquitecturas con diferentes niveles de complejidad:
  1. **Regresión Logística:** 
  2. **Random Forest:** 
  3. **Gradient Boosting:**
  
  Cada entrenamiento registra automáticamente en el backend de MLflow sus hiperparámetros, métricas de rendimiento (`accuracy` y `precision`) y tiempos de ejecución, garantizando la trazabilidad del proceso.

### Fase 3: Gestión y Empaquetado de Artefactos (Model Registry)
* **Tecnología:** `MLflow Models`
* **Explicación:** Una vez finalizada la competición, el pipeline identifica automáticamente el modelo con el mejor desempeño y almacena su información física en el registro de artefactos.
  
### Fase 4: Despliegue en Producción y Servido de Modelos
* **Tecnología:** `FastAPI` & `Uvicorn`
* **Explicación:** Se expone el modelo ganador mediante una API RESTful de alta velocidad. Si el modelo se reentrena y mejora la API cargará la nueva versión en su próximo reinicio sin necesidad de modificar una sola línea de código del servidor web. 

---

## 📂 Estructura Detallada del Repositorio

Para facilitar la auditoría del proyecto, el código se ha organizado siguiendo los estándares de la industria:

* **`/data/processed/`**: Contiene el dataset tratado y limpio sobre el que trabaja el modelo.
* **`f1_dataset_clean.csv.dvc`**: Archivo de metadatos generado por DVC para el control de versiones del dataset.
* **`/mlruns/`**: Servidor de almacenamiento local de MLflow donde se registran los experimentos, métricas y los archivos físicos de los modelos entrenados.
* **`/src/`**: Código de ingeniería de producción. Contiene `api.py`, el script que levanta el servidor FastAPI y define los endpoints de predicción.
* **`main.py`**: Orquestador central del pipeline. Al ejecutar este script se dispara el flujo completo: validación de DVC, entrenamiento de modelos, registro en MLflow y test de integración de la API.
* **`requirements.txt`**: Archivo de congelación de dependencias que especifica las librerías exactas y sus versiones para garantizar la portabilidad del entorno.

---
