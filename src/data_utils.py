# src/data_utils.py
import pandas as pd


def load_data(path):
    """Carga el dataset desde el archivo CSV."""
    df = pd.read_csv(path)
    return df


def check_missing_values(df):
    """Devuelve el conteo de valores nulos por columna."""
    return df.isnull().sum()


def clean_data(df):
    """Ejemplo básico de limpieza."""
    # Llenar valores nulos en 'country' con 'Unknown'
    df["country"] = df["country"].fillna("Unknown")
    # Llenar valores nulos en 'director' con 'No Director'
    df["director"] = df["director"].fillna("No Director")
    return df
