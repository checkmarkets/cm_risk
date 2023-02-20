import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
from eod import EodHistoricalData
from datetime import datetime, timedelta
import datetime as dt
from streamlit_option_menu import option_menu

st.set_page_config(page_title = "cm Indices", 
	page_icon="💲"
	)

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]


### LOGO POSITIONING ###

col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    st.image('LOGO.jpg')

with col3:
    st.header("")
    
####################################


st.title('NEW: OUR ULTIMATE SPECIAL')  

st.write("We develop **CHECK.MARKETS STOCK INDICES** on the basis of momentum and risk indicators. We strive for maximum return, no matter which direction markets take.")
st.write("")
st.write("")
st.header("Strategy #1: PHIL-RATIO")
st.subheader("Implemented for all Nasdaq 100 constituents as of today. Updated Daily. Investments are made quarterly.")
st.write("Our first algorithm can be introduced for any stock market index. In this case, we focus on Nasdaq 100 and its constituents.")
st.write("With the Phil-Ratio, we invest in the TOP 10 stocks according to the three momentum indicators Std, Pos Days and Performance. To calculate the Phil Ratio, all three factors are multiplied. Every first day of a new quarter after market close, we buy the 10 best stocks according to the preceding quarter.")

st.latex(r'''Phil Ratio = Std * No Pos Days * Performance''')
st.write("")
with st.expander("STD"):
	st.write("**Std** is the abbreviation for **Standard Deviation Multiple**. To calculate this multiple, we divide the standard deviation of positive returns by the standard deviation of negative returns. In case this multiple shows a value higher than 1, this means that the volatility for stock price increases is higher than the volatility for stock price decreases.")
with st.expander("NO POS DAYS"):
	st.write("**No Pos Days** is the abbreviation for the **Number of Positive Days Multiple**. With this multiple, we compare (and divide) the number of positive days by the number of negative days. If the multiple is higher than 1, this means that the stock has experienced more positive closing days than negative closing days.")
with st.expander("PERFORMANCE"):
	st.write("This multiple is rather easily derivable: To calculate the **Performance Multiple** we divide the latest stock price by the first one. Values above 1 indicate that the stock return was positive in the timeframe analyzed.")

####################################################################################


with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)

ticker_iex = ticker.replace('.US', '')

today = dt.datetime.today()
today = today.strftime('%Y-%m-%d')

#Source: https://www.geeksforgeeks.org/python-pandas-timestamp-quarter/
year = str(pd.Timestamp(today).year)
quarter = str(pd.Timestamp(today).quarter)

if quarter == "1":
    beginn = year+"-01-01"
    ende = year+"-03-31"
if quarter == "2":
    beginn = year+"-04-01"
    ende = year+"-06-30"
if quarter == "3":
    beginn = year+"-07-01"
    ende = year+"-09-30"
if quarter == "4":
    beginn = year+"-10-01"
    ende = year+"-12-31"


################## USER INTERFACE ######################

reference_index = "GSPC.INDX"


################## P H I L   R A T I O ##################

# philRatio (on 1y basis)
list_of_index_components = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/" + reference_index + "?api_token=" + eod_api + "&filter=Components&fmt=json").T
list_of_tickers = list(list_of_index_components.Code)
list_of_tickers.append(ticker_iex)
list_of_tickers = list(set(list_of_tickers))

df = yf.download(list_of_tickers, start = beginn, interval = "1d")["Adj Close"].dropna(thresh = 5, axis = 1)

norm_prices = df.div(df.iloc[0])*100
dly_chg = norm_prices.pct_change(1)
	
#Perf
first_price = norm_prices.iloc[0]
latest_price = norm_prices.iloc[-1]
perf_ratio = latest_price/first_price
	
#Std
std_pos = dly_chg.where(dly_chg > 0).std()
std_neg = dly_chg.where(dly_chg < 0).std()
std_ratio = dly_chg.where(dly_chg > 0).std()/dly_chg.where(dly_chg < 0).std()
std_ratio = std_ratio.where(std_ratio.between(0.05, 10))
	
#No days
no_days_neg = dly_chg.where(dly_chg < 0).count()
no_days_pos = dly_chg.where(dly_chg > 0).count()
no_days_ratio = no_days_pos/no_days_neg

philRatio = std_ratio * no_days_ratio * perf_ratio
top_stocks = philRatio.sort_values(ascending=False).nlargest(10)

##########
				    
st.write("")
st.subheader("Standings as of today (Top 10)")
st.write("")

tbl, chart = st.columns(2)
chart.table(top_stocks)
tbl.bar_chart(top_stocks)

std, nodays, perf = st.columns(3)
std_ratio.columns = ["Std"]
no_days_ratio.columns = ["Pos Days"]
perf_ratio.columns = ["Performance"]
std.subheader("Std")
nodays.subheader("Pos Days")
perf.subheader("Performance")
std.bar_chart(std_ratio.sort_values(ascending=False).nlargest(10))
nodays.bar_chart(no_days_ratio.sort_values(ascending=False).nlargest(10))
perf.bar_chart(perf_ratio.sort_values(ascending=False).nlargest(10))

st.header("How strong does " + ticker_iex + " perform?")
st.subheader("Check out how your selected stock performs. Should you invest?")

c1, c2, c3 = st.columns(3)
with c1:
    st.write("")
with c2:
    st.metric(label = "Phil Ratio", value = round(philRatio[ticker_iex], 2), delta = round(strength_ratio[ticker_iex] - top_stocks.min(), 2))
with c3:
    st.header("")


stdratio, daysratio, perfratio = st.columns(3)
stdratio.metric(label= "Standard Deviation Multiple", value = round(std_ratio[ticker_iex], 2), delta = round(std_ratio[ticker_iex] - 1, 2))
daysratio.metric(label = "Positive Days Multiple", value = round(no_days_ratio[ticker_iex], 2), delta = round(no_days_ratio[ticker_iex] - 1, 2))
perfratio.metric(label = "Performance Multiple", value = round(perf_ratio[ticker_iex], 2), delta = round(perf_ratio[ticker_iex] - 1, 2))
