import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st


headers = {
	"authorization": st.secrets["eod_api"],
	"content-type": "application/json",
	"authorization": st.secrets["secret_key"]}

	
c = pyEX.Client(secret_key)

today = datetime.today()
today = today.strftime('%Y-%m-%d')

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
	ticker = st.text_input("Enter a Ticker here", st.session_state["ticker"])
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker
		st.write("You are analyzing: ", ticker)

ticker_iex = ticker.replace('.US', '')


#CORRELATION ANALYSIS

analyzed_instruments = ["EURUSD=X", "EURCHF=X", "EURGBP=X", "GC=F", "SI=F", "CL=F", "^TNX", "^TYX", "^GSPC"]
bonds_const = ["^TNX", "^TYX", "^GSPC"]
curr_const = ["EURUSD=X", "EURCHF=X", "EURGBP=X", "^GSPC"]
comm_const = ["GC=F","SI=F", "CL=F", "^GSPC"]

c01 = ["2000-03-24", "2002-10-09"]
c02 = ["2007-10-09", "2013-03-28"]
c03 = ["2020-02-19", "2020-08-18"]
c04 = ["2022-01-03", today]


df = yf.download(analyzed_instruments, period="max")["Adj Close"]

st.header("HOW DO OTHER ASSET CLASSES PERFORM DURING CRASHS?")
st.write("Many investors have a clear opinion of what to invest in in case of crises. This dataset is **updated daily**. We introduced an **automatic crises analyzer algorithm** which finds out when crises started and how they developed. Do these instruments really suffice? We analyze the correlation between:") 
st.write("- Equity (= S&P 500),")
st.write("- Bonds (10Y Treasury Yd, 30Y Treasury Yd),") 
st.write("- Commodities (Gold, Silver, Oil) and ")
st.write("- Currencies (EUR/USD, EUR/CHF, EUR/GBP).")
st.write("")
st.write("")

st.subheader("#1: BONDS")
st.write("")

s1, s2 = st.columns(2)
s1.write("DOTCOM BUBBLE BURST")
norm_c01 = df[c01[0]:c01[1]][bonds_const]
norm_c01 = norm_c01.div(norm_c01.iloc[0])*100-100
norm_c01.columns = ["10Y Treasury Yield", "30Y Treasury Yield", "S&P 500"]
s1.line_chart(norm_c01)

s2.write("SUBPRIME CRISES")
norm_c02 = df[c02[0]:c02[1]][bonds_const]
norm_c02 = norm_c02.div(norm_c02.iloc[0])*100-100
norm_c02.columns = ["10Y", "30Y Treasury Yield", "S&P 500"]
s2.line_chart(norm_c02)

s3, s4 = st.columns(2)
s3.write("CORONA CRISES")
norm_c03 = df[c03[0]:c03[1]][bonds_const]
norm_c03 = norm_c03.div(norm_c03.iloc[0])*100-100
norm_c03.columns = ["10Y Treasury Yield", "30Y Treasury Yield", "S&P 500"]
s3.line_chart(norm_c03)

s4.write("INFLATION")
norm_c04 = df[c04[0]:c04[1]][bonds_const]
norm_c04 = norm_c04.div(norm_c04.iloc[0])*100-100
norm_c04.columns = ["10Y Treasury Yield", "30Y Treasury Yield", "S&P 500"]
s4.line_chart(norm_c04)


st.subheader("#2: COMMODITIES")
st.write("")

s1, s2 = st.columns(2)
s1.write("DOTCOM BUBBLE BURST")
norm_c01 = df[c01[0]:c01[1]][comm_const]
norm_c01 = norm_c01.div(norm_c01.iloc[0])*100-100
norm_c01.columns = ["Gold", "Silver", "Crude Oil", "S&P 500"]
s1.line_chart(norm_c01)

s2.write("SUBPRIME CRISES")
norm_c02 = df[c02[0]:c02[1]][comm_const]
norm_c02 = norm_c02.div(norm_c02.iloc[0])*100-100
norm_c02.columns = ["Gold", "Silver", "Crude Oil", "S&P 500"]
s2.line_chart(norm_c02)

s3, s4 = st.columns(2)
s3.write("CORONA CRISES")
norm_c03 = df[c03[0]:c03[1]][comm_const]
norm_c03 = norm_c03.div(norm_c03.iloc[0])*100-100
norm_c03.columns = ["Gold", "Silver", "Crude Oil", "S&P 500"]
s3.line_chart(norm_c03)

s4.write("INFLATION")
norm_c04 = df[c04[0]:c04[1]][comm_const]
norm_c04 = norm_c04.div(norm_c04.iloc[0])*100-100
norm_c04.columns = ["Gold", "Silver", "Crude Oil", "S&P 500"]
s4.line_chart(norm_c04)

st.subheader("#3: CURRENCY EXCHANGE RATES")
st.write("")

s1, s2 = st.columns(2)
s1.write("DOTCOM BUBBLE BURST")
norm_c01 = df[c01[0]:c01[1]][comm_const]
norm_c01 = norm_c01.div(norm_c01.iloc[0])*100-100
norm_c01.columns = ["Gold", "Silver", "Crude Oil", "S&P 500"]
norm_c01.columns = ["EUR/USD", "EUR/CHF", "EUR/GBP", "S&P 500"]
s1.line_chart(norm_c01)

s2.write("SUBPRIME CRISES")
norm_c02 = df[c02[0]:c02[1]][comm_const]
norm_c02 = norm_c02.div(norm_c02.iloc[0])*100-100
norm_c02.columns = ["EUR/USD", "EUR/CHF", "EUR/GBP", "S&P 500"]
s2.line_chart(norm_c02)

s3, s4 = st.columns(2)
s3.write("CORONA CRISES")
norm_c03 = df[c03[0]:c03[1]][comm_const]
norm_c03 = norm_c03.div(norm_c03.iloc[0])*100-100
norm_c03.columns = ["EUR/USD", "EUR/CHF", "EUR/GBP", "S&P 500"]
s3.line_chart(norm_c03)

s4.write("INFLATION")
norm_c04 = df[c04[0]:c04[1]][comm_const]
norm_c04 = norm_c04.div(norm_c04.iloc[0])*100-100
norm_c04.columns = ["EUR/USD", "EUR/CHF", "EUR/GBP", "S&P 500"]
s4.line_chart(norm_c04)
