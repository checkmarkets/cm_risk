import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import datetime as dt
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu


#####################    P A R A M E T E R S  ###########################

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

st.set_page_config(page_title = "check.markets Risk Analysis", 
	page_icon="💲"
	)


today = datetime.today()
today = today.strftime('%Y-%m-%d')

day = pd.Timestamp(today).day
day = str(day)

month = pd.Timestamp(today).month
if month < 10:
    month = str("0" + str(month))

year = int(pd.Timestamp(today).year)
year_new = str(year - 1)

start_date = str(year_new+"-"+month+"-"+day)
start_date = datetime.strptime(start_date,'%Y-%m-%d')


with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)


ticker_iex = ticker.replace('.US', '')


df = yf.download(ticker_iex, start = start_date, interval = "1d")["Adj Close"]
df = pd.DataFrame(df)

days_year = len(df)
days_3y = len(df)*3

currPrice = round(df.iloc[-1,0], 2)
ytdHigh = round(df.rolling(days_year).max().iloc[-1,0], 2)
high_dist = (-ytdHigh + currPrice)/currPrice * 100
high_dist = round(high_dist, 1)
high_dist = str(high_dist)+"%"

ytdLow = round(df.rolling(days_year).min().iloc[-1,0], 2)
low_dist = (currPrice - ytdLow)/ytdLow * 100
low_dist = round(low_dist, 1)
low_dist = str(low_dist)+"%"

ma50 = df.rolling(50).mean()
last_ma50 = round(ma50.iloc[-1,0],2)
ma50_dist = (currPrice - last_ma50)/currPrice * 100
ma50_dist = round(ma50_dist, 1)
ma50_dist = str(ma50_dist) + " %"

ma100 = df.rolling(100).mean()
last_ma100 = round(ma100.iloc[-1,0],2)
ma100_dist = (currPrice - last_ma100)/currPrice * 100
ma100_dist = round(ma100_dist, 1)
ma100_dist = str(ma100_dist) + " %"

ma200 = df.rolling(200).mean()
last_ma200 = round(ma200.iloc[-1,0],2)
ma200_dist = (currPrice - last_ma200)/currPrice * 100
ma200_dist = round(ma200_dist, 1)
ma200_dist = str(ma200_dist) + " %"


st.header("TECHNICAL ANALYSIS")
st.write("Technical analysis help you to identify trends in a stock's price, which provides valuable insights into the stock's performance and potential future movements. Our focus especially deals with technical risk analysis.")

st.subheader("Trend Analysis")

return1y = str(round((df.iloc[-1, 0]/df.iloc[0, 0]-1) * 100, 1)) + " %"

# Technical Dashboard
row1col1, row1col2, row1col3 = st.columns(3)
row1col1.metric(label="Current Price (1y Return)", value= currPrice, delta= return1y)
row1col2.metric(label="52wk High (% needed for new 52wk High)", value = ytdHigh, delta = high_dist)
row1col3.metric(label="52wk Low (return since 52wk Low)", value = ytdLow, delta = low_dist)

row2col1, row2col2, row2col3 = st.columns(3)
row2col1.metric(label="50 Days Moving Avg", value = last_ma50, delta= ma50_dist)
row2col2.metric(label="100 Days Moving Avg", value = last_ma100, delta = ma100_dist)
row2col3.metric(label="200 Days Moving Avg", value = last_ma200, delta = ma200_dist)

with st.expander("EXPLANATION"):
	st.markdown("**Negative values**: The stock needs to reach this return in order to break this level.")
	st.markdown("**Positive values**: The stock has reached this return since having topped this level.")


#### CHARTING ####

st.subheader('BENCHMARK ANALYSIS (VS NASDAQ 100)')

ref_index = "^NDX"

new_ticker = ticker.replace(".US", "")
new_ticker_list = [new_ticker, ref_index]

new_df = yf.download(new_ticker_list)["Adj Close"].dropna()
new_df.columns = [new_ticker, "Nasdaq 100"]

new_norm_df = new_df.div(new_df.iloc[0]) * 100
new_norm_1y = new_df.div(new_df.iloc[-days_year]) * 100
new_norm_3y = new_df.div(new_df.iloc[-days_3y]) * 100

chart_timeframe = st.selectbox("Which chart would you like to see?", ("1y", "3y", "All-Time"))    
if ticker:
	if chart_timeframe == "1y":
		st.line_chart(new_norm_1y.loc[start_date:])
	if chart_timeframe == "3y":
		st.line_chart(new_norm_3y.iloc[-days_year*3:])
	if chart_timeframe == "All-Time":
		st.line_chart(new_norm_df)


