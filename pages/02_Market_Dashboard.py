import streamlit as st
import yfinance as yf
import pyEX
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

st.set_page_config(page_title = "cm Markets", 
	page_icon="💲"
	)

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

c = pyEX.Client(secret_key)

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"]).upper()
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker.upper()
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')


### LOGO POSITIONING ####

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image('LOGO.jpg')

with col3:
    st.write(' ')


### MARKET DASHBOARD ###

st.title("MARKET DASHBOARD")

list_of_indexes = ["^GSPC", "^NDX", "^GDAXI", "EURUSD=X", "EURCHF=X", "EURGBP=X", "GC=F", "SI=F", "CL=F", "^IRX", "^FVX", "^TNX", "^TYX"]

data = yf.download(list_of_indexes)["Adj Close"].dropna(axis = 0)

asOfDate = data.index[-1].strftime("%Y-%m-%d")
st.markdown("Market data as of " + str(asOfDate))
st.subheader("Indices")

sp500, ndx, dax = st.columns(3)
sp500.metric(label = "S&P 500", value = round(data["^GSPC"].iloc[-1],2), delta = str(round((data["^GSPC"].iloc[-1]/data["^GSPC"].iloc[-2]-1)*100,2))+"%")
ndx.metric(label = "Nasdaq 100", value = round(data["^NDX"].iloc[-1],2), delta = str(round((data["^NDX"].iloc[-1]/data["^NDX"].iloc[-2]-1)*100,2))+"%")
dax.metric(label = "DAX", value = round(data["^GDAXI"].iloc[-1],2), delta = str(round((data["^GDAXI"].iloc[-1]/data["^GDAXI"].iloc[-2]-1)*100,2))+"%")

st.subheader("Bonds")
m3, y5, y30 = st.columns(3)
m3.metric(label = "3M Treasury Yield", value= round(data["^IRX"].iloc[-1],4), delta = str(round((data["^IRX"].iloc[-1]/data["^IRX"].iloc[-2]-1)*100,2))+"%")
y5.metric(label = "5Y Treasury Yield", value = round(data["^FVX"].iloc[-1],4), delta = str(round((data["^FVX"].iloc[-1]/data["^FVX"].iloc[-2]-1)*100,2))+"%")
y30.metric(label = "30Y Treasury Yield", value = round(data["^TYX"].iloc[-1],4), delta = str(round((data["^TYX"].iloc[-1]/data["^TYX"].iloc[-2]-1)*100,2))+"%")

st.subheader("Commodities")
gold, silver, oil = st.columns(3)
gold.metric(label = "Gold", value = round(data["GC=F"].iloc[-1],2), delta = str(round((data["GC=F"].iloc[-1]/data["GC=F"].iloc[-2]-1)*100,2))+"%")
silver.metric(label = "Silver", value = round(data["SI=F"].iloc[-1],2), delta = str(round((data["SI=F"].iloc[-1]/data["SI=F"].iloc[-2]-1)*100,2))+"%")
oil.metric(label = "Crude Oil", value = round(data["CL=F"].iloc[-1],2), delta = str(round((data["CL=F"].iloc[-1]/data["CL=F"].iloc[-2]-1)*100,2))+"%")

st.subheader("Currency Exchange Rates")
eurusd, eurchf, eurgbp = st.columns(3)
eurusd.metric(label = "EUR/USD", value= round(data["EURUSD=X"].iloc[-1],4), delta = str(round((data["EURUSD=X"].iloc[-1]/data["EURUSD=X"].iloc[-2]-1)*100,2))+"%")
eurchf.metric(label = "EUR/CHF", value = round(data["EURCHF=X"].iloc[-1],4), delta = str(round((data["EURCHF=X"].iloc[-1]/data["EURCHF=X"].iloc[-2]-1)*100,2))+"%")
eurgbp.metric(label = "EUR/GBP", value = round(data["EURGBP=X"].iloc[-1],4), delta = str(round((data["EURGBP=X"].iloc[-1]/data["EURGBP=X"].iloc[-2]-1)*100,2))+"%")
