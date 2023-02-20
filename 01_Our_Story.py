import pandas as pd
import streamlit as st


### FORMATTING ###
st.set_page_config(page_title = "check.markets Risk Analysis", 
	page_icon="💲"
	#,layout="wide",
	)

st.image('casino_coverphoto.jpeg')


### CONTENT ###
st.title("Do you want to know the REAL risks of your US stock investments?")
st.subheader("Look no further than our cutting-edge risk analysis for US stocks!")
st.write("**This app is powered by nothing more than the innovative power of Streamlit. With exclusive access to market and fundamental data, check.markets will now be your favorite go-to place for US stock analysis.**")

risk, visuals, ride = st.columns(3)
risk.write("Whether you're analyzing market trends, predicting potential risks, or simply exploring the data, this app is the ultimate tool for data-driven decision making.")
visuals.write("With its interactive and visually appealing interface, you can quickly and easily dive into complex data sets and uncover insights that were previously hidden.") 
ride.write("**So if you're ready to take your risk analysis to the next level, let's go.**")

st.write("**Enter a Stock Ticker on the lefthand side.** If you want to know the Ticker of a specific stock (like "**AAPL.US**" for Apple or "**MSFT.US**" for Microsoft), use "List of Stocks" on the left hand side.")

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')
