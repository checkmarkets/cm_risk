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
st.subheader("Then better check out this website. With check.markets you learn how much money you REALLY risk when investing in US stocks.")
st.write("**Empowered by exclusive access to market and fundamental data, check.markets will now better be your favorite go-to place for profound risk analysis for US stock investments.**")

risk, visuals, ride = st.columns(3)
risk.write("Whether you're analyzing market trends, predicting potential risks, or simply exploring the data, this app is **the ultimate tool for data-driven decision making**.")
visuals.write("With its interactive and visually appealing interface, you can quickly and easily dive into complex data sets and uncover insights that you can't find anywhere else.") 
ride.write("**So if you're ready to take your risk analysis to the next level, add this website to your bookmarks!**")

st.subheader("**Enter a Stock Ticker on the lefthand side.** Try **AAPL.US** for Apple or **MSFT.US** for Microsoft if you are here for the first time. If you want to know the Ticker of a specific stock, use List of Stocks on the lefthand side.")

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')
