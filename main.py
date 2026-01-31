import streamlit as st
import requests
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Config ------------------

BASE_URL = "https://restcountries.com/v3.1"
st.set_page_config(page_title="Language Routes")


# ------------------ Data Model ------------------

@dataclass
class Country:
    name: str
    flag: str
    capital: str
    region: str
    languages: str
    languages_low: dict[str, str]
    currency: str
    startOfWeek: str
    borders: str
    area: int
    population: int
    map_url: str


# ------------------ Data layer ------------------

@st.cache_data(show_spinner="Fetching countries...")
def fetch_countries_by_language(language: str) -> list[dict]:
    url = f"{BASE_URL}/lang/{language}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return []

    return response.json()


def to_country(raw: dict) -> Country:
    lang = raw.get("languages", {})
    currencies = raw.get("currencies", {})
    if currencies:
        currency = list(currencies.values())[0].get("name", "")
    else:
        currency = ""

    return Country(
        name=raw.get("name", {}).get("common", "Unknown"),
        flag=raw.get("flags", {}).get("svg", ""),
        capital=", ".join(raw.get("capital", [])),
        region=raw.get("region", ""),
        languages=", ".join(list(lang.values())),
        languages_low={key.lower(): value.lower() for key, value in lang.items()},
        currency=currency,
        startOfWeek=raw.get("startOfWeek", ""),
        borders=", ".join(raw.get("borders", [])),
        area=raw.get("area", 0),
        population=raw.get("population", 0),
        map_url=raw.get("maps", {}).get("googleMaps", ""),
    )


def countries_to_dataframe(countries: list[Country]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": c.name,
            "flag": c.flag,
            "capital": c.capital,
            "region": c.region,
            "languages": c.languages,
            "languages_low": c.languages_low,
            "currency": c.currency,
            "startOfWeek": c.startOfWeek,
            "borders": c.borders,
            "area": c.area,
            "population": c.population,
            "map": c.map_url,
        }
        for c in countries
    ).sort_values("name")


# ------------------ UI helpers ------------------

def country_selector(df: pd.DataFrame):
    left, mid, right = st.columns([2, 3, 4])

    with left:
        choice = st.selectbox("**Select a country**", df["name"].tolist())

    with right:
        comparison_type = st.radio("Select comparison type", ["population", "area"])
        st.subheader(f"Comparison of the Top 10 Countries by {comparison_type.capitalize()}")
        plot_comparison(df, comparison_type)

    selected = df.loc[df["name"] == choice].iloc[0]
    return selected, mid


def country_details(country, container):
    cols = container.columns([2, 3])

    with cols[0]:
        if country["flag"]:
            st.image(country.flag, width=60)

    with cols[1]:
        st.subheader(country["name"])

    st.write(f"**Capital:** {country["capital"]}")
    st.write(f"**Region:** {country["region"]}")
    st.write(f"**Languages:** {country["languages"]}")
    st.write(f"**Currency:** {country["currency"]}")
    st.write(f"**Start of the week:** {country["startOfWeek"] or 'Unknown'}")
    st.write(f"**Borders:** {country["borders"] or 'None'}")
    st.write(f"**Area:** {country["area"]:,} km²")
    st.write(f"**Population:** {country["population"]:,}")

    if country["map"]:
        st.markdown(f"[🌍 View on Google Maps]({country["map"]})")


def plot_comparison(df, comparison_type="population"):
    top_10 = df.nlargest(10, comparison_type)

    fig, ax = plt.subplots(figsize=(10, 6))

    if comparison_type == "population":
        ax.barh(top_10["name"], top_10["population"], color='skyblue')
        ax.set_xlabel("Population")
        ax.set_ylabel("Country")
        ax.set_title("Top 10 Countries by Population")
    elif comparison_type == "area":
        ax.barh(top_10["name"], top_10["area"], color='salmon')
        ax.set_xlabel("Area (km²)")
        ax.set_ylabel("Country")
        ax.set_title("Top 10 Countries by Area")

    st.pyplot(fig)


# ------------------ App ------------------

def main():
    st.title("Language Routes")

    language = (
        st.text_input("What language do you speak?")
        .strip()
        .lower()
    )

    if not language:
        st.info("Enter a language to explore countries 🌍")
        return

    raw_countries = fetch_countries_by_language(language)

    if not raw_countries:
        st.error("No countries found for that language.")
        return

    countries = [to_country(c) for c in raw_countries]
    df = countries_to_dataframe(countries)

    selected, details_col = country_selector(df)
    with details_col:
        country_details(selected, details_col)


if __name__ == "__main__":
    main()
