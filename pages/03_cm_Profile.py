import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
from time import time
from datetime import datetime, timedelta
from math import sqrt
from streamlit_option_menu import option_menu

st.set_page_config(page_title = "cm Profile", 
	page_icon="💲"
	)

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)

ticker_iex = ticker.replace('.US', '')

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

list_of_stocks = pd.DataFrame(list(pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + reference_index + "?api_token=" + eod_api + "&fmt=json")["Components"].dropna()))
sec_list = pd.DataFrame(list(pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + ref_index_2 + "?api_token=" + eod_api + "&fmt=json")["Components"].dropna()))
list_of_stocks = pd.concat([list_of_stocks, sec_list])
companyName = list_of_stocks.loc[ticker].Name 

logo = pd.read_json("https://eodhistoricaldata.com/img/logos/US/"+ticker+".png")
st.image(logo)

rt_price = pd.read_json("https://eodhistoricaldata.com/api/real-time/AAPL.US?api_token="+eod_api+"&fmt=json&filter=close")

highlights = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=Valuation,Highlights").T
marketCap = highlights.MarketCapitalization[1]

name, price, mcap = st.columns(3)
name.metric(label = "Company Name", value = companyName)
price.metric(label = "Latest Price (USD)", value = rt_price)
mcap.metric(label = "Market Cap in USDm", value = marketCap)
