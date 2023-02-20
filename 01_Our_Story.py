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
st.write("**Empowered by exclusive access to market and fundamental data, check.markets will now better be your favorite go-to place for profound risk analysis for US stock investments.** So if you're ready to take your risk analysis to the next level, add this website to your bookmarks!")

st.subheader("**Enter a Stock Ticker on the left-hand side.**")
st.write("If you want to know the Ticker of a specific stock, go to **List of Stocks** on the lefthand side.")


with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')

st.header("What you can learn from this page")
ri, crash, indx = st.columns(3)
ri.write("Nothing is more key to an investor than knowing the risk of his investments. Freely quoting Buffett or Graham, it takes a lot of insight to decide for a good investment.")
crash.write("What definitely needs to be checked is how the stock performed during market crashes to know how much we could have lost in the past.")
indx.write("To optimize performance despite crashes, we create trading algorithms for long-term investors that provide exceptional risk/reward ratios.")

