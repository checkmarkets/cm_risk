import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu


headers = {
	"authorization": st.secrets["eod_api"],
	"authorization": st.secrets["secret_key"]}



###############     F O R M A T T I N G    #################


st.set_page_config(page_title = "check.markets Risk Analysis", 
	page_icon="💲"
	#,layout="wide",
	)


### LOGO POSITIONING ####

#st.image('/myfirststream/casino_coverphoto.jpeg')


#### NAVIGATION BAR ###

#selected = option_menu(
#	menu_title="check.markets Risk Dashboard",
#	options=["Home", "Technical", "Financials", "Risk", "News"],
#	icons = ["bank", "pie-chart", "bar-chart-line", "ui-checks", "newspaper"],
#	orientation = "horizontal"
#	)
	
st.title("Are you tired of leaving your investments to chance? With check.markets, this is over now.")
st.subheader("Look no further than our cutting-edge risk analysis tool for US stocks!")



st.write("**This app is powered by nothing more than the cutting-edge technology of Streamlit. With exclusive access to market and fundamental data, this application will now be your favorite go-to place for US stock analysis.**")

risk, visuals, ride = st.columns(3)

risk.write("Whether you're analyzing market trends, predicting potential risks, or simply exploring the data, this app is the ultimate tool for data-driven decision making.")
visuals.write("With its interactive and visually appealing interface, you can quickly and easily dive into complex data sets and uncover insights that were previously hidden.") 
ride.write("**So if you're ready to take your risk analysis to the next level, let's go.**")

st.subheader("Start analyzing stocks by entering a Stock Ticker on the left. Get inspired by clicking **'List of Available Stocks'** to check out all stocks you can analyze with this app.")


with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)
    	


ticker_iex = ticker.replace('.US', '')
