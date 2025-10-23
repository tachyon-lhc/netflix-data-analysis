# src/analysis.py
"""
Script principal que ejecuta la EDA y guarda outputs en outputs/{plots,reports}
Ejecución:
    python src/analysis.py
"""

import os
from data_utils import load_data, basic_clean, parse_duration, save_df
from eda_utils import (
    plot_content_types,
    plot_top_countries,
    plot_release_trend,
    average_duration_by_type,
    top_directors,
    genre_counts,
    save_basic_report,
)

DATA_PATH = os.path.join("..", "data", "netflix_titles.csv")


def main():
    df = load_data(DATA_PATH)
    print(f"Cargado dataset: {df.shape} filas, columnas: {df.shape[1]}\n")

    df = basic_clean(df)
    df = parse_duration(df)

    # Guardar versión limpia (opcional)
    cleaned_path = os.path.join("..", "outputs", "reports", "netflix_cleaned.csv")
    save_df(df, cleaned_path)

    # Generar gráficos y reportes
    plot_content_types(df)
    plot_top_countries(df, n=20)
    plot_release_trend(df)
    avg = average_duration_by_type(df)
    top_dirs = top_directors(df, n=15)
    genres = genre_counts(df, n=20)
    save_basic_report(df)

    print(df.head(), "\n")
    print(avg, "\n")
    print(top_dirs, "\n")
    print(genres, "\n")


if __name__ == "__main__":
    main()
