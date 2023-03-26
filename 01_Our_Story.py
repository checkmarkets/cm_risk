import pandas as pd
import streamlit as st


### FORMATTING ###
st.set_page_config(page_title = "check.markets Risk Analysis", 
	page_icon="💲"
	#,layout="wide",
	)

st.image('casino_coverphoto.jpeg')


### CONTENT ###
st.title("You love to minimize risk better than anybody else?")
stock_query = '[Search Your Stock HERE!](https://checkmarkets.streamlit.app/cm_List_of_Stocks)'
st.subheader(stock_query)
st.subheader("Then better check out this website. With check.markets you learn how much money you REALLY risk when investing in US stocks.")
st.write("**Empowered by exclusive access to market and fundamental data, check.markets will now better be your favorite go-to place for profound risk analysis for US stock investments.** So if you're ready to take your risk analysis to the next level, add this website to your bookmarks!")

tutorial = '[Learn how to get the max out of this app!](https://www.youtube.com/watch?v=nmCxvaOxEoU)'
st.subheader(tutorial)
st.write("If you want to know the Ticker of a specific stock, go to **List of Stocks** on the lefthand side.")

st.write("If the entry of your ticker symbol (MSFT.US/AAPL.US) does not work, this is caused by me currently working on a professional high-class web-app for which I need to download ALL historic financials of US companies requiring the maximum amount of my allowed API calls. My data provider cuts the retrieval of data after the maximum amount of 100,000 calls was used within one day. Please try again one day later or contact me - I will make it work for you :-)")

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')
