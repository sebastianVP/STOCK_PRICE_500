import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf


# ESQUEMA
# st.title
# st.markdown

# st.header
# st.write
# st.dataframe

# SIDEBAR
# st.sidebar.header
# st.sidebar.selectbox
# st.sidebar.multiselect
# st.sidebar.multiselect

# HEATMAT
# st.button
# st.header
# st.pyplot

st.title("WEB S&P 500 APP")

st.markdown("""
Esta aplicacion recupera la lista de los **S&P 500** (desde Wikipedia)
* **Python Libraries:** base64,pandas, streamlit,numpy,matplotlib
* **Data Source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
            """)

st.sidebar.header("Caracteristicas de Entrada del Usuario")

# Web Scraping of S&P 500 Data
@st.cache_data
def load_data():
    url  = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url,header=0)
    df = html[0]
    return df

df = load_data()
# SIDEBAR. SECTOR SELECTION
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector      = st.sidebar.multiselect('Sector',sorted_sector_unique,sorted_sector_unique)

# FILTERING DATA
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in Selected Sector')
st.write('Data dimension: '+ str(df_selected_sector.shape[0])+ ' rows and '+str(df_selected_sector.shape[1])+' columns.')
st.dataframe(df_selected_sector)

#Download S&P500 Data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
