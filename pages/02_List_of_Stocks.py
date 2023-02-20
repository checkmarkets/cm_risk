import pandas as pd
import numpy as np
import streamlit as st
from eod import EodHistoricalData
from streamlit_option_menu import option_menu

st.set_page_config(page_title = "cm List of Stocks", 
	page_icon="💲"
	)

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

##########################################################################



reference_index = "RUT.INDX"
ref_index_2 = "GSPC.INDX"


### LOGO POSITIONING ####

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.image('LOGO.jpg')

with col3:
    st.write(' ')

	
st.title("List of Available Stocks")


### DATA RETRIEVAL ###

list_of_stocks = pd.DataFrame(list(pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + reference_index + "?api_token=" + eod_api + "&fmt=json")["Components"].dropna()))
sec_list = pd.DataFrame(list(pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + ref_index_2 + "?api_token=" + eod_api + "&fmt=json")["Components"].dropna()))
list_of_stocks = pd.concat([list_of_stocks, sec_list])
list_of_stocks["Ticker"] = list_of_stocks.Code + "." + list_of_stocks.Exchange
list_of_stocks.sort_values("Ticker", ascending=True, inplace = True)
list_of_stocks.reset_index(inplace=True)
list_of_stocks.set_index("Ticker", inplace = True)
list_of_stocks.drop(columns = ["index", "Code", "Exchange"], inplace= True)
list_of_stocks = list_of_stocks.drop_duplicates()

st.table(list_of_stocks)

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)
