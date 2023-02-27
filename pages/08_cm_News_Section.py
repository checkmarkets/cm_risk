import pandas as pd
import pyEX
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title = "cm News", 
	page_icon="💲"
	)

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

	
c = pyEX.Client(secret_key)
	
### LOGO POSITIONING ####

col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:
    st.image('LOGO.jpg')

with col3:
    st.write('')
    
	
with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"]).upper()
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker.upper()
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')



### NEWS ###

st.title(ticker_iex + " NEWS TICKER")

st.subheader("check.markets offers up-to-date and reliable corporate stock-related news. ")
st.write("This is especially beneficial to find out what has moved the stock today or recently. Another great advantage: You don't need to click any links. Just read the summary of the article to be informed.")
news = c.newsDF(ticker_iex)
#news = news[["source","headline","summary"]]
news = news[["source","summary"]]



#with st.expander("COMPANY NEWS"):
st.table(news)
