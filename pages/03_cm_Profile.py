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
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"]).upper()
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker.upper()
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

reference_index = "RUT.INDX"
ref_index_2 = "GSPC.INDX"

list_of_stocks = pd.DataFrame(list(pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + reference_index + "?api_token=" + eod_api + "&fmt=json")["Components"].dropna()))
sec_list = pd.DataFrame(list(pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + ref_index_2 + "?api_token=" + eod_api + "&fmt=json")["Components"].dropna()))
list_of_stocks = pd.concat([list_of_stocks, sec_list])
companyName = list_of_stocks.Name.where(list_of_stocks.Code == ticker_iex).dropna().iloc[0]
sector = list_of_stocks.Sector.where(list_of_stocks.Code == ticker_iex).dropna().iloc[0]
industry = list_of_stocks.Industry.where(list_of_stocks.Code == ticker_iex).dropna().iloc[0]

#logo = pd.read_json("https://eodhistoricaldata.com/img/logos/US/"+ticker_iex+".png")
st.image(
            "https://eodhistoricaldata.com/img/logos/US/"+ticker_iex+".png",
            width=200 # Manually Adjust the width of the image as per requirement
        )

rt_price = pd.DataFrame(pd.read_csv("https://eodhistoricaldata.com/api/real-time/"+ticker+"?fmt=csv&api_token="+eod_api+"&filter=close")).iloc[0,0]

highlights = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=Valuation,Highlights").T
marketCap_unformatted = round(highlights.MarketCapitalization[1]/1000000000, 1)
marketCap = "{:,.2f}".format(marketCap_unformatted)

st.metric(label = "Company Name", value = companyName)

price, mcap = st.columns(2)
price.metric(label = "Latest Price (USD)", value = rt_price)
mcap.metric(label = "Market Cap in USDb", value = marketCap)

sec, ind = st.columns(2)
sec.metric(label = "Sector", value = sector)
ind.metric(label = "Industry", value = industry)

desc = pd.read_csv("https://eodhistoricaldata.com/api/fundamentals/"+ticker+"?api_token="+eod_api+"&filter=General::Description").columns[0]
st.write(desc)