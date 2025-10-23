# src/eda_utils.py
"""
Funciones para análisis exploratorio y generación de gráficos/estadísticas.
Guarda plots en outputs/plots y resúmenes en outputs/reports.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
PLOTS_DIR = os.path.join(BASE_DIR, "outputs", "plots")
REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


def save_fig(fig, filename: str):
    """Guarda figura matplotlib en la carpeta de plots"""
    path = os.path.join(PLOTS_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"✅ Guardado: {path}")


def plot_content_types(df: pd.DataFrame):
    """Guarda gráfico barras: Películas vs Series."""
    counts = df["type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Distribución de Tipos (Movie vs TV Show)")
    ax.set_ylabel("Cantidad")
    save_fig(fig, "content_types.png")


def plot_top_countries(df: pd.DataFrame, n=15):
    """Top N países con más títulos (guarda gráfico)."""
    top = df["country"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(8, max(4, n * 0.25)))
    sns.barplot(x=top.values, y=top.index, ax=ax)
    ax.set_title(f"Top {n} países por cantidad de títulos")
    save_fig(fig, "top_countries.png")


def plot_release_trend(df: pd.DataFrame):
    """Guarda gráfico de títulos por año (serie temporal)."""
    counts = df["release_year"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    counts.plot(ax=ax)
    ax.set_title("Títulos por Año de Lanzamiento")
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad de títulos")
    save_fig(fig, "titles_per_year.png")


def average_duration_by_type(df: pd.DataFrame):
    """Calcula la duración promedio (en minutos) de películas, y guarda CSV resumen."""
    # Asegurarse de tener duration_min parseado
    if "duration_min" not in df.columns:
        raise ValueError(
            "duration_min no está en el DataFrame. Ejecutá parse_duration primero."
        )
    # Solo películas con duration_min válidos
    movies = df[df["type"] == "Movie"]
    avg_min = movies["duration_min"].mean()
    median_min = movies["duration_min"].median()
    summary = pd.DataFrame(
        {
            "type": ["Movie"],
            "avg_duration_min": [avg_min],
            "median_duration_min": [median_min],
            "count": [len(movies)],
        }
    )
    out_path = os.path.join(REPORTS_DIR, "duration_summary.csv")
    summary.to_csv(out_path, index=False)
    print(f"✅ Resumen guardado en {out_path}")
    return summary


def top_directors(df: pd.DataFrame, n=10):
    """Guarda CSV con los top N directores por número de títulos. Maneja 'No Director'."""
    top = df["director"].fillna("No Director").value_counts().head(n).reset_index()
    top.columns = ["director", "num_titles"]
    out_path = os.path.join(REPORTS_DIR, "top_directors.csv")
    top.to_csv(out_path, index=False)
    print(f"✅ Top directores guardado en {out_path}")
    return top


def genre_counts(df: pd.DataFrame, n=15):
    """Explota la columna 'listed_in' y guarda top N géneros a CSV y gráfico."""
    genres = df["listed_in"].str.split(", ").explode()
    counts = genres.value_counts().head(n)
    # CSV
    out_csv = os.path.join(REPORTS_DIR, "top_genres.csv")
    counts.reset_index().rename(columns={"index": "genre", 0: "count"}).to_csv(
        out_csv, index=False
    )
    print(f"✅ Top géneros guardado en {out_csv}")
    # Gráfico
    fig, ax = plt.subplots(figsize=(8, max(4, n * 0.25)))
    sns.barplot(x=counts.values, y=counts.index, ax=ax)
    ax.set_title("Top géneros")
    save_fig(fig, "top_genres.png")
    return counts


def save_basic_report(df: pd.DataFrame):
    """Genera un archivo markdown con estadísticas básicas del dataset."""
    n_rows, n_cols = df.shape
    missing = df.isnull().sum()
    types = df.dtypes

    lines = [
        "# Reporte básico del dataset",
        "",
        f"- Filas: {n_rows}",
        f"- Columnas: {n_cols}",
        "",
        "## Conteo de valores nulos por columna",
        "",
        missing.to_frame(name="missing").to_markdown(),
        "",
        "## Tipos de columnas",
        "",
        types.to_frame(name="dtype").to_markdown(),
    ]
    out_md = os.path.join(REPORTS_DIR, "basic_report.md")
    with open(out_md, "w", encoding="utf8") as f:
        f.write("\n".join(lines))
    print(f"✅ Reporte básico guardado en {out_md}")

