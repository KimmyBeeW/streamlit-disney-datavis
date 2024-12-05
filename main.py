import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import *
import streamlit as st

@st.cache_data
def load_stock_data():
    url = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/all_disney_stocks.csv'
    stocks = pd.read_csv(url, index_col = 0)
    stocks = stocks[~stocks.apply(lambda row: row.astype(str).str.contains('Dividend', na=False)).any(axis=1)]
    stocks['Date'] = pd.to_datetime(stocks['Date'])
    stocks.set_index('Date', inplace=True)
    stocks['Open'] = pd.to_numeric(stocks['Open'], errors='coerce')
    return stocks

@st.cache_data
def load_movie_data():
    url = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disney_owned_movies.csv'
    movies = pd.read_csv(url)
    url1 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/marvel_movies.csv'
    marvel = pd.read_csv(url1)
    url2 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/lucasfilm_movies.csv'
    lucas = pd.read_csv(url2)
    url3 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/pixar_movies.csv'
    pixar = pd.read_csv(url3)
    url4 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disney_animation_movies.csv'
    animation = pd.read_csv(url4)
    url5 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disney_channel_movies.csv'
    channel = pd.read_csv(url5)
    url6 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disneynature_movies.csv'
    nature = pd.read_csv(url6)
    url7 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disneytoon_movies.csv'
    toon = pd.read_csv(url7)
    url8 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/blue_sky_movies.csv'
    bluesky = pd.read_csv(url8)
    return movies, marvel, lucas, pixar, animation, channel, nature, toon, bluesky

stocks = load_stock_data()
movies, marvel, lucas, pixar, animation, channel, nature, toon, bluesky = load_movie_data()



# The APP implementation (needs at least six interactive elements)
st.title("Disney Stocks and Disney Brands Box Office Numbers")  # app title

with st.sidebar:  # interactive side bar
    brands = st.radio('Brand name', ['Marvel', 'Lucasfilm', 'Pixar', 'Walt Disney Animation', 'Disney Channel', 'Disneytoon Studios', 'Disneynature', 'Blue Sky Studios'])

tab1, tab2, tab3, tab4 = st.tabs(["Disney Stocks", "2", "3", "4"])
with tab1:
    startyear_input = st.slider('Start Year', min_value = 1962, max_value=2024, value=2019)
    endyear_input = st.slider('End Year', min_value = 1962, max_value=2024, value=2024)
    allstocks = stocks.copy
    fig=px.line(allstocks, x='Date', y='Close')
    st.plotly_chart(fig)


