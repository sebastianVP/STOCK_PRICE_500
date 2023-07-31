import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf


st.title("WEB S&P 500 APP")

st.markdown("""
Esta aplicacion recupera la lista de los **S&P 500** (desde Wikipedia)
* **Python Libraries:** base64,pandas, streamlit,numpy,matplotlib
* ***Data Source:* [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
            """)

st.sidebar.header("Caracteristicas de Entrada del Usuario")

# Web Scraping of S&P 500 Data
@st.cache_data
def load_data():
    url  = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url,header=0)
    