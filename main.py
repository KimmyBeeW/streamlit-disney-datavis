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
    stocks['Date'] = pd.to_datetime(stocks['Date'], errors='coerce')
    stocks['Open'] = pd.to_numeric(stocks['Open'], errors='coerce')
    stocks['Close'] = pd.to_numeric(stocks['Close'], errors='coerce')
    stocks.set_index('Date', inplace=False)
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
    startyear_input = st.slider('Start Year', min_value = 1962, max_value=2024, value=2021)
    endyear_input = st.slider('End Year', min_value = 1962, max_value=2024, value=2024)
    
    filt_stocks = stocks[(stocks['Date'] >= pd.Timestamp(startyear_input, 1, 1)) & 
                         (stocks['Date'] <= pd.Timestamp(endyear_input, 12, 31))].copy()
    
    mlt_stocks = filt_stocks.melt(id_vars='Date', value_vars=['Close', 'Open', 'High', 'Low'], 
                                     var_name='Type', value_name='Price ($)')
    
    val_colors = {'High': 'green', 'Low': 'red',
                     'Close': 'blue', 'Open': 'orange'}
    
    # Create a line chart with Plotly Express
    fig = px.line(mlt_stocks, x='Date', y='Price ($)', color='Type',
                  title='Disney Stock Prices Over Time',
                  labels={'Price': 'Stock Price', 'Type': 'Price Type'},
                  color_discrete_map=val_colors)
    st.plotly_chart(fig)


