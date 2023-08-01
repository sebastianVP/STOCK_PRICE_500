import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
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
* **Python Libraries:** base64,pandas, streamlit,matplotlib, yfinance
* **Data Source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
            """)

st.sidebar.header("Caracteristicas de Entrada del Usuario")

# Web Scraping of S&P 500 Data,save the data once
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

def filedownload(df):
    csv = df.to_csv(index= False)
    b64 = base64.b64encode(csv.encode()).decode()# string<> byte conversion
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector),unsafe_allow_html=True)


# https://pypi.org/project/yfinance/

#estudiar las propiedades del api yf
# tambien se puede usar pd.get_data_yahoo(...)
data = yf.download(
    # LISTA DE TICKETS O CADENAS 
    tickers     = list(df_selected_sector[:10].Symbol),
    #USA PERIODO EN LUGAR DE INICIO/FIN
    # PERIODOS VALIDOS: 1d,5d,10d,1mes,  year to data
    period      = "ytd",
    interval    = "1d",
    group_by    = "ticker",
    auto_adjust = True,
    prepost     = True,
    threads     = True,
    proxy       = None
)

# Plot Closing Price of Query Symbol

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date']= df.index
    plt.fill_between(df.Date,df.Close,color='skyblue',alpha=0.3)
    plt.plot(df.Date,df.Close,color='skyblue',alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol,fontweight='bold')
    plt.xlabel('Date',fontweight= 'bold')
    plt.ylabel('Closing Price',fontweight= 'bold')
    return st.pyplot()

num_company = st.sidebar.slider('Number of Companies',1,5)
st.set_option('deprecation.showPyplotGlobalUse', False)


if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)