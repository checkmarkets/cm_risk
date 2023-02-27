import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
from time import time
from datetime import datetime, timedelta
from math import sqrt
from streamlit_option_menu import option_menu

st.set_page_config(page_title = "cm Risk Check", 
	page_icon="💲"
	)

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]

### LOGO POSITIONING ####
col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.image('LOGO.jpg')
with col3:
    st.write('')

st.title("CHECK.MARKETS RISK CHECK")
st.write("Our intuitive interface provides real-time updates and clear visualizations to help you make informed decisions and stay ahead of market trends.")
st.write("Let's start with the most popular Risk KPIs. We compare the actuals to the target ratio of each KPI.")

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"]).upper()
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker.upper()
		st.write("You are analyzing: ", ticker)

ticker_iex = ticker.replace('.US', '')

###########################################################

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

###########################################################

df = yf.download(ticker_iex, start = start_date, interval = "1d")["Adj Close"]
df = pd.DataFrame(df)

crises_list = ["^GSPC", ticker_iex]
crises_df = yf.download(crises_list, interval = "1d")["Adj Close"]

#MAX DRAWDOWN

tab1, tab2, tab3, tab4 = st.tabs(["MAXIMUM DRAWDOWN", "RISK DASHBOARD", "(INVERTED) YIELD CURVE", "PERFORMANCE DURING FINANCIAL CRISES"])

with tab1:
	st.subheader("Maximum Drawdown Chart ("+ticker+" vs. S&P 500)")
	maxDDDataset = crises_df.dropna(axis=0)
	maxDDChart = ((maxDDDataset.div(maxDDDataset.expanding().max())-1)*100)
	maxDD = ((maxDDDataset.div(maxDDDataset.expanding().max())-1)*100).min()
	maxDD_stock = maxDD[0]
	maxDD_index = maxDD[1]

	st.write("The maximum Drawdown of " + ticker_iex + " is at " + str(round(maxDD_stock, 1))+"%" + ", whereas the S&P 500's highest drawdown in this timeframe is at " + str(round(maxDD_index, 1))+"%"  + ". ")
	st.line_chart(maxDDChart)

days_year = len(df)

### RISK MEASURES ###

#SHARPE RATIO
risk_free_yield = yf.download("^TYX", start = start_date)["Adj Close"]
yearAgoPrice = df.iloc[-days_year,0]
currPrice = df.iloc[-1,0]
return1y = currPrice / yearAgoPrice - 1
latest_rfr = risk_free_yield.iloc[-1]/100

sharpeRatio = ((return1y - latest_rfr) / (df.iloc[:,0].rolling(days_year).std().iloc[-1]/100))
sharpeRatio = round(sharpeRatio, 2)

#SORTINO RATIO
firstPrice = df.iloc[0,0]
cagr = (currPrice / firstPrice) ** (1/(days_year)) - 1
ref_idx = yf.download("^GSPC", period="max")["Adj Close"]
expected_return = (ref_idx.iloc[-1]/ref_idx.iloc[0])**(1/(len(ref_idx)/252))-1

dly_chg = df.iloc[-days_year:,0].pct_change(1)
dly_chg = dly_chg[dly_chg < 0]
neg_std = dly_chg.std()
sortinoRatio = round((cagr - expected_return) / neg_std, 2)


#TREYNOR RATIO
ref_idx = yf.download("^GSPC", period="max")["Adj Close"]
idx_currPrice = ref_idx.iloc[-1]
idx_yearAgoPrice = ref_idx.iloc[-days_year]
idx1yrReturn = idx_currPrice / idx_yearAgoPrice - 1

# (B) CORRELATION
#Source: https://corporatefinanceinstitute.com/resources/data-science/correlation/
mean_stock = df.iloc[:,0].describe().T["mean"]
mean_index = ref_idx[df.index[0]:].describe().T["mean"]

a = df.iloc[:,0] - mean_stock
b = ref_idx[df.index[0]:] - mean_index

a_b = a*b
a2 = sum(a**2)
b2 = sum(b**2)

correlation = round(sum(a_b)/(np.sqrt(a2)*np.sqrt(b2)), 3)

stock_std = df.iloc[:,0].pct_change(1).std()
index_std = ref_idx[df.index[0]:].pct_change(1).std()

#Source for formula: https://www.investopedia.com/ask/answers/070615/what-formula-calculating-beta.asp
beta = round(correlation * (stock_std/index_std), 2)

#Source: https://corporatefinanceinstitute.com/resources/capital-markets/treynor-ratio/
treynorRatio = round((return1y - idx1yrReturn)/beta, 2) 

#VOLATILITY
std_dev = df.pct_change(1).describe().T["std"][0]
volatility = round(np.sqrt(252)*std_dev*100, 1)

###########################################################################

with tab2:
	st.subheader("cm RISK DASHBOARD")
	st.write("")

	sharpe, sortino, treynor = st.columns(3)
	sharpe.metric(label = "Sharpe Ratio (1Y)", value = sharpeRatio, delta = round(sharpeRatio - 1, 1))
	sortino.metric(label = "Sortino Ratio (1Y)", value = sortinoRatio, delta = round(sortinoRatio - 2,1))
	treynor.metric(label = "Treynor Ratio (1Y)", value = treynorRatio, delta = round(treynorRatio - 1,2))

	beta1y, corr, vola = st.columns(3)
	beta1y.metric(label = "Beta (1Y)", value = round(beta,2), delta = round(beta - 1,2), delta_color = "inverse")
	corr.metric(label = "Correlation (1Y)", value = str(round(correlation*100,1))+"%", delta = str(round((correlation - 0.5)*100,1))+"%", delta_color = "inverse")
	vola.metric(label = "Volatility (1Y)", value = str(volatility)+"%", delta = str(round(volatility-20, 1))+"%", delta_color = "inverse")

	st.write("")

	with st.expander("SHARPE RATIO"):
		st.write("The **Sharpe Ratio** is a measure of risk-adjusted return that compares an investment's excess return to its volatility (= risk). The higher it is, the better. Typically, a Sharpe Ratio of 1 or higher is considered good, and a ratio of 2 or higher is considered excellent.")

	with st.expander("SORTINO RATIO"):
		st.write("The **Sortino Ratio** concentrates on the downside risk of a portfolio and is therefore widely appreciated. We compare the actual return of the stock to the real CAGR of the reference index since its inception. Sortino Ratio of 1 or higher is considered adequate, while a ratio of 2 or higher is considered strong.")

	with st.expander("TREYNOR RATIO"):
		st.write("The **Treynor Ratio** (commonly known as reward-to-volatility ratio) is a measure of risk-adjusted return that compares an investment's excess return to the systematic risk of the portfolio, as measured by its beta. Treynor Ratio of 1 or higher is considered satisfactory, while a ratio of 2 or higher is considered remarkable.")

	with st.expander("BETA"):
		st.write("**Beta** indicates how much the stock's price tends to move in response to changes in the market. A beta of 1 means the stock's price moves in line with the market, while a beta greater than 1 indicates the stock is more volatile than the market, and a beta less than 1 indicates the stock is less volatile than the market.")
	with st.expander("CORRELATION"):
		st.write("If an investor is looking for high-growth stocks or for stocks that move independently from market swings (especially interesting in case of market downturns), they may be willing to accept a higher level of volatility and less **correlation** with the market. In case of upward trends, correlation with the general market is a good sign for stocks.")
	with st.expander("VOLATILITY"):
		st.write("**Volatility** is a statistical measure of the degree of fluctuation in a stock's price, reflecting the level of risk associated with the investment. For a retail investor with a moderate risk tolerance, a reasonable level of volatility for a stock within a year might be in the range of 10-20%. This would mean that the stock's price could fluctuate by up to 10-20% in either direction over the course of a year.")


#INVERTED YIELD CURVE
with tab3:
	st.subheader("(INVERTED) YIELD CURVE")
	st.write("")
	with st.expander("EXPLANATION"):
		st.write("An **Inverted (or Negative) Yield Curve** occurs when short-term treasury yields are higher than long-term treasury yield of the same credit risk profile. Usually, the US treasury bonds are analyzed. While investors mostly take the 2YR and the 10Y Treasury Yield as indicators, academic studies of the relationship between an inverted yield curve and recessions have tended to look at the spread between the yields on the 10YR U.S. Treasury bond and the 3M Treasury bill.")
	list_of_bonds = ["^IRX", "^TNX"]
	bonds = yf.download(list_of_bonds, interval="1d")["Adj Close"].dropna(axis=0)
	short_bond = round(bonds.iloc[-1][0], 2)
	long_bond = round(bonds.iloc[-1][1], 2)

	st.write("")
	st.write("")
	m3, y10, spread = st.columns(3)
	m3.metric(label = "3M Treasury Yield", value = short_bond)
	y10.metric(label = "10Y Treasury Yield", value = long_bond)
	spread.metric(label = "Yield Spread", value = round(long_bond - short_bond,2))
	st.write("")
	yield_diff = (bonds["^TNX"] - bonds["^IRX"]).dropna(axis=0)
	bonds.columns = ["3M Treasury Yd", "10Y Treasury Yd"]
	st.line_chart(bonds)

	st.subheader("Yield Spread between 3M and 10Y Treasury Yield")
	st.write("")
	st.bar_chart(yield_diff)


	
#CRISES ANALYSIS
with tab4:
	c01 = ["2000-03-24", "2002-10-09"]
	c02 = ["2007-10-09", "2013-03-28"]
	c03 = ["2020-02-19", "2020-08-18"]
	c04 = ["2022-01-03", today]

	st.write("")
	st.write("")

	st.header("HOW DOES " + ticker_iex + " PERFORM DURING CRASHS?")
	st.write("By analyzing how individual stocks or the market as a whole have performed during past crashes, you can gain a better understanding of their potential risk and return characteristics.")

	st.subheader("DOTCOM BUBBLE BURST (" + c01[0] + " to " + c01[1] + ")")
	norm_c01 = crises_df[c01[0]:c01[1]]
	norm_c01 = norm_c01.div(norm_c01.iloc[0])*100-100
	st.line_chart(norm_c01)

	st.subheader("SUBPRIME CRISES (" + c02[0] + " to " + c02[1] + ")")
	norm_c02 = crises_df[c02[0]:c02[1]]
	norm_c02 = norm_c02.div(norm_c02.iloc[0])*100-100
	st.line_chart(norm_c02)

	st.subheader("CORONA CRISES (" + c03[0] + " to " + c03[1] + ")")
	norm_c03 = crises_df[c03[0]:c03[1]]
	norm_c03 = norm_c03.div(norm_c03.iloc[0])*100-100
	st.line_chart(norm_c03)

	st.subheader("INFLATION AND INTEREST RATE HIKES (" + c04[0] + " to " + c04[1] + ")")
	norm_c04 = crises_df[c04[0]:c04[1]]
	norm_c04 = norm_c04.div(norm_c04.iloc[0])*100-100
	st.line_chart(norm_c04)
