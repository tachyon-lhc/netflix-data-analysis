# src/data_utils.py
"""
Utilities para cargar y limpiar el dataset de Netflix.

Funciones principales:
- load_data(path): carga CSV en un DataFrame.
- check_missing_values(df): devuelve conteo de nulos.
- basic_clean(df): limpieza básica y normalización.
- parse_duration(df): convierte la columna 'duration' en minutos (para películas)
                     y en número de temporadas (para series), creando columnas
                     'duration_min' y 'duration_seasons'.
- save_df(df, path): guarda DataFrame a CSV.
"""

import os
import pandas as pd
import numpy as np


def load_data(path: str) -> pd.DataFrame:
    """Carga el CSV desde `path` y retorna un DataFrame.
    - Usa inferencia básica; no modifica el DataFrame.
    """
    df = pd.read_csv(path)
    return df


def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """Devuelve la cantidad de valores nulos por columna."""
    return df.isnull().sum()


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Aplicar limpieza básica y normalizaciones:
    - Drop de duplicados
    - Normalizar nombres de columnas (strip)
    - Rellenar country/director/rating/duration con valores por defecto
    - Convertir date_added a datetime (coerce errores)
    """
    df = df.drop_duplicates().copy()
    df.columns = df.columns.str.strip()

    df["country"] = df["country"].fillna("Unknown")
    df["director"] = df["director"].fillna("No Director")
    df["rating"] = df["rating"].fillna("Unknown")
    df["duration"] = df["duration"].fillna("Unknown")

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    # release_year ya viene como int en este dataset, pero por seguridad:
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype(
        "Int64"
    )

    # Normalizar strings: quitar espacios extra
    str_cols = df.select_dtypes(include="object").columns
    for c in str_cols:
        df[c] = df[c].str.strip()

    return df


def parse_duration(df: pd.DataFrame) -> pd.DataFrame:
    """Parsea la columna 'duration' y agrega:
    - duration_min: minutos si es película (int), NaN si no
    - duration_seasons: temporadas si es serie (int), NaN si no

    Ejemplos de 'duration' que aparecen en el dataset: '90 min', '2 Seasons', '1 Season', 'Unknown'
    """
    duration_min = []
    duration_seasons = []

    for i, row in df.iterrows():
        val = row.get("duration", None)
        if not isinstance(val, str):
            duration_min.append(np.nan)
            duration_seasons.append(np.nan)
            continue

        val = val.strip()
        if val.endswith("min"):
            # formato "90 min"
            try:
                minutes = int(val.replace("min", "").strip())
            except ValueError:
                minutes = np.nan
            duration_min.append(minutes)
            duration_seasons.append(np.nan)
        elif "Season" in val:
            # "1 Season" o "2 Seasons"
            try:
                seasons = int(val.split()[0])
            except ValueError:
                seasons = np.nan
            duration_min.append(np.nan)
            duration_seasons.append(seasons)
        else:
            duration_min.append(np.nan)
            duration_seasons.append(np.nan)

    df = df.copy()
    df["duration_min"] = pd.Series(duration_min).astype("Float64")
    df["duration_seasons"] = pd.Series(duration_seasons).astype("Int64")
    return df


def save_df(df: pd.DataFrame, path: str):
    """Guarda DataFrame a CSV. Crea carpeta si hace falta."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ DataFrame guardado en {path}")
