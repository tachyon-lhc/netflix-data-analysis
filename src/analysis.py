from data_utils import load_data, check_missing_values, clean_data
from eda_utils import (
    plot_content_types,
    plot_top_countries,
    plot_release_years,
    plot_genres,
)

df = load_data("../data/netflix_titles.csv")
print(df.head())

print(check_missing_values(df))

df = clean_data(df)
print(df)

plot_content_types(df)
plot_top_countries(df)
plot_release_years(df)
plot_genres(df)
