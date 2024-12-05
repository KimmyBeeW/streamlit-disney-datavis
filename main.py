import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    movies['Release Dates'] = pd.to_datetime(movies['Release Dates'], errors='coerce')
    url1 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/marvel_movies.csv'
    marvel = pd.read_csv(url1)
    marvel['Release Dates'] = pd.to_datetime(marvel['Release Dates'], errors='coerce')
    url2 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/lucasfilm_movies.csv'
    lucas = pd.read_csv(url2)
    lucas['Release Dates'] = pd.to_datetime(lucas['Release Dates'], errors='coerce')
    url3 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/pixar_movies.csv'
    pixar = pd.read_csv(url3)
    pixar['Release Dates'] = pd.to_datetime(pixar['Release Dates'], errors='coerce')
    url4 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disney_animation_movies.csv'
    animation = pd.read_csv(url4)
    animation['Release Dates'] = pd.to_datetime(animation['Release Dates'], errors='coerce')
    url5 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disney_channel_movies.csv'
    channel = pd.read_csv(url5)
    channel['Release Dates'] = pd.to_datetime(channel['Release Dates'], errors='coerce')
    url6 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disneynature_movies.csv'
    nature = pd.read_csv(url6)
    nature['Release Dates'] = pd.to_datetime(nature['Release Dates'], errors='coerce')
    url7 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/disneytoon_movies.csv'
    toon = pd.read_csv(url7)
    toon['Release Dates'] = pd.to_datetime(toon['Release Dates'], errors='coerce')
    url8 = 'https://github.com/KimmyBeeW/Disney-Web-Scraping/raw/main/datasets/blue_sky_movies.csv'
    bluesky = pd.read_csv(url8)
    bluesky['Release Dates'] = pd.to_datetime(bluesky['Release Dates'], errors='coerce')
    return movies, marvel, lucas, pixar, animation, channel, nature, toon, bluesky

stocks = load_stock_data()
movies, marvel, lucas, pixar, animation, channel, nature, toon, bluesky = load_movie_data()
brand_datasets = {
    'Marvel': marvel,
    'Lucasfilm': lucas,
    'Pixar': pixar,
    'Walt Disney Animation': animation,
    'Disney Channel': channel,
    'Disneynature': nature,
    'Disneytoon Studios': toon,
    'Blue Sky Studios': bluesky,
    'All 8 Brands from BoxMojo': movies
}


# The APP implementation (needs at least six interactive elements)
st.title("Disney Stocks and Disney Brands Box Office Numbers")  # app title

with st.sidebar:  # interactive side bar
    brands = st.radio('Brand name', ['Marvel', 'Lucasfilm', 'Pixar', 'Walt Disney Animation', 'Disney Channel', 
                                     'Disneytoon Studios', 'Disneynature', 'Blue Sky Studios', 'All 8 Brands from BoxMojo'])

data = brand_datasets[brands]

tab1, tab2, tab3 = st.tabs(["Disney Stocks", "Gross Income", "Brand Summaries"])
with tab1:
    # slider for range of the graph dates
    startyear_input = st.slider('Start Year', min_value = 1962, max_value=2024, value=2021)
    endyear_input = st.slider('End Year', min_value = 1962, max_value=2024, value=2024)
    filt_stocks = stocks[(stocks['Date'] >= pd.Timestamp(startyear_input, 1, 1)) & 
                         (stocks['Date'] <= pd.Timestamp(endyear_input, 12, 31))].copy()
    # make it possible to see all four lines
    mlt_stocks = filt_stocks.melt(id_vars='Date', value_vars=['Close', 'Open', 'High', 'Low'], 
                                     var_name='Type', value_name='Price ($)')
    # custom colors
    val_colors = {'High': '#29b6f6', 'Low': '#a80930',
                     'Close': '#efb71d', 'Open': '#2bb007'}
    # plot the stocks
    fig = px.line(mlt_stocks, x='Date', y='Price ($)', color='Type',
                  title='Disney Stock Prices Over Time',
                  labels={'Price': 'Stock Price', 'Type': 'Price Type'},
                  color_discrete_map=val_colors)
    st.plotly_chart(fig)
with tab2:
    df = movies.copy()
    df['Gross Income'] = df['Gross Income'].replace('[$,]', '', regex=True).astype(float)
    studio_gross = df.groupby('Brand')['Gross Income'].sum().reset_index()
    
    fig = px.bar( # plotly bar chart
        studio_gross, x='Brand', y='Gross Income',
        title="Total Gross Income per Brand",
        labels={'Gross Income': 'Total Gross Income (B$)', 'Brand': 'Brand'},
        color='Brand'
    )
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)
with tab3:
    st.subheader(f"Summary Statistics: {brands}")
    
    # dataset has the necessary columns
    if 'Release Dates' in data.columns and 'Opening Earnings' in data.columns:
        # convert Release Dates to datetime if not already
        data['Release Dates'] = pd.to_datetime(data['Release Dates'], errors='coerce')

        # create scatter plot
        fig = px.scatter(
            data,
            x='Release Dates',
            y='Opening Earnings',
            hover_data=['Title', 'Gross Income', 'Max Theaters', 'Studio'],  # add movie title etc as hover information
            title=f"Opening Earnings vs. Release Dates for {brands}",
            labels={'Opening Earnings': 'Opening Earnings (M$)', 'Release Dates': 'Release Date'},
            color='Opening Earnings',  # Optional: add color based on the gross
            color_continuous_scale='Viridis'
        )
        fig.update_traces(marker=dict(size=8))  # adjust marker size
        st.plotly_chart(fig)  # show figure
    else:
        st.warning("The selected dataset does not contain the required columns: 'Release Date' and 'Opening Week Gross'.")

