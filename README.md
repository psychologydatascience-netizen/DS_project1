# Language Routes

**Language Routes** is a Streamlit app that allows users to explore countries based on the language they speak.
By entering a language, users can view details of countries where that language is spoken, including flags, capitals, population and more.
The app also provides a visual comparison of the top 10 countries that speak the language by population or area.

## Features
- Search countries by language.
- View detailed information about each country (flag, capital, region, languages, etc.).
- Interactive comparison of the top 10 countries by population or area.
- Data fetched from the [Rest Countries API](https://restcountries.com).

## Usage

You can use the app directly by visiting the live Streamlit app:  
[Streamlit App](https://dsproject1-gvxvq3zflnhvdn2annxru7.streamlit.app/)

Or by executing the "main.py" file.

## Code Overview

- **`main.py`**: The main file that powers the Streamlit app. 
It defines the data model, fetches country data based on the entered language, and provides an interactive UI for exploring country details and comparisons.

## Dependencies

- Streamlit
- Requests
- Pandas
- Matplotlib