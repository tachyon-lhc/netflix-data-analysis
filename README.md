# Netflix Data Analysis (Pro)

## Objetivo

Análisis exploratorio del dataset "Netflix Movies and TV Shows" (Kaggle).
Se limpia, se parsean columnas complejas y se generan métricas y visualizaciones.

## Estructura

- `data/` : dataset original.
- `src/` : código fuente (data_utils.py, eda_utils.py, analysis.py).
- `outputs/plots/` : imágenes generadas.
- `outputs/reports/` : CSVs y reportes en markdown.

## Cómo ejecutar

1. Clonar repo y colocar `netflix_titles.csv` en `data/`.
2. Crear entorno e instalar dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
