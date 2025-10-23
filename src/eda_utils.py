import os
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs", "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_plot(fig, filename):
    """Guarda la figura en la carpeta outputs/plots."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"✅ Gráfico guardado en {path}")


def plot_content_types(df):
    counts = df["type"].value_counts()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", color=["#FF5C5C", "#5C8CFF"], ax=ax)
    ax.set_title("Distribución de Tipos de Contenido en Netflix")
    ax.set_xlabel("Tipo")
    ax.set_ylabel("Cantidad")
    save_plot(fig, "content_types.png")


def plot_top_countries(df, n=10):
    top_countries = df["country"].value_counts().head(n)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="crest", ax=ax)
    ax.set_title(f"Top {n} países con más títulos")
    ax.set_xlabel("Cantidad de títulos")
    ax.set_ylabel("País")
    save_plot(fig, "top_countries.png")


def plot_release_years(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df["release_year"], bins=20, kde=True, color="#5C8CFF", ax=ax)
    ax.set_title("Distribución de títulos por año de lanzamiento")
    ax.set_xlabel("Año de lanzamiento")
    ax.set_ylabel("Cantidad de títulos")
    save_plot(fig, "release_years.png")


def plot_genres(df, n=10):
    all_genres = df["listed_in"].str.split(", ").explode()
    top_genres = all_genres.value_counts().head(n)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_genres.values, y=top_genres.index, palette="flare", ax=ax)
    ax.set_title(f"Top {n} géneros más comunes en Netflix")
    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Género")
    save_plot(fig, "top_genres.png")
