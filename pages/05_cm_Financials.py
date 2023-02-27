import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
from eod import EodHistoricalData
from time import time
from datetime import datetime, timedelta
from openpyxl.workbook import Workbook
from streamlit_option_menu import option_menu

eod_api = st.secrets["eod_api"]
secret_key = st.secrets["secret_key"]


st.set_page_config(page_title = "cm Financials", 
	page_icon="💲"
	)

with st.sidebar:
	if "ticker" not in st.session_state:
		st.session_state["ticker"] = ""
	ticker = st.text_input("Enter a Ticker here (Try **AAPL.US** or **MSFT.US**)", st.session_state["ticker"]).upper()
	submit = st.button("Submit")
	
	if submit:
		st.session_state["ticker"] = ticker.upper()
		st.write("You are analyzing: ", ticker)
    	
ticker_iex = ticker.replace('.US', '')



############ F U N D A M E N T A L S ##################

### DATA RETRIEVAL ###

infos = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=General::")
infos = pd.DataFrame(infos[["Name","Description","Sector","Industry", "CurrencyCode"]].iloc[0]).T

annual_bs = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=Financials::Balance_Sheet::yearly").T
annual_inc = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=Financials::Income_Statement::yearly").T
annual_cf = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=Financials::Cash_Flow::yearly").T
annual_summary = pd.concat([annual_bs, annual_inc, annual_cf])

annual_inc.to_excel("inc.xlsx", index_label = True)
annual_bs.to_excel("bs.xlsx")
annual_cf.to_excel("cf.xlsx")

inc = pd.read_excel("inc.xlsx", usecols= ["date","totalRevenue", "grossProfit", "ebitda", "ebit","incomeBeforeTax", "netIncome"])
bs = pd.read_excel("bs.xlsx", usecols = ["date","totalCurrentAssets","goodWill","propertyPlantEquipment","netTangibleAssets","totalAssets", "totalStockholderEquity", "totalCurrentLiabilities","netDebt","commonStockSharesOutstanding","cashAndEquivalents"])
cf = pd.read_excel("cf.xlsx", usecols = ["date","totalCashFromOperatingActivities","freeCashFlow","dividendsPaid","issuanceOfCapitalStock", "salePurchaseOfStock"])



#############################################################################

st.title("FINANCIALS AT A GLANCE")
st.write("Check out the most important financial metrics to understand how sustainable the investment in your stock is.")

### GROWTH ###

growth = pd.DataFrame(index = cf.index, columns = ["rev_gth", "ni_gth", "div_gth", "adjdiv_gth"])

growth.rev_gth = round(inc.totalRevenue.pct_change(-5) * 100, 1)
growth.ni_gth = round(inc.netIncome.pct_change(-5) * 100, 1)
growth.div_gth = round(abs(cf.dividendsPaid).pct_change(-5) * 100, 1)
growth.adjdiv_gth = round((abs(cf.dividendsPaid.fillna(value=0)) - (cf.issuanceOfCapitalStock.fillna(value=0) + cf.salePurchaseOfStock.fillna(value=0))).pct_change(-1)  * 100, 1)

currGrowth = {"Revenue 5y" : str(growth.rev_gth.iloc[0]) + " %",
             "Net Income 5y" : str(growth.ni_gth.iloc[0]) + " %",
             "Dividends 5y" : str(growth.div_gth.iloc[0]) + " %",
             "Adj Dividends 1y" : str(growth.adjdiv_gth.iloc[0]) + " %"
             }



### MARGINS ###

margins = pd.DataFrame(index = cf.index, columns = ["gpm", "ebitdam", "ebitm", "nim", "ocfm", "fcfm", "roe"])

margins.gpm = round(inc.grossProfit/inc.totalRevenue * 100, 1)
margins.ebitdam = round(inc.ebitda/inc.totalRevenue * 100, 1)
margins.ebitm = round(inc.ebit/inc.totalRevenue * 100, 1)
margins.nim = round(inc.netIncome/inc.totalRevenue * 100, 1)
margins.ocfm = round(cf.totalCashFromOperatingActivities/inc.totalRevenue * 100, 1)
margins.fcfm = round(cf.freeCashFlow/inc.totalRevenue * 100, 1)
margins.roe = round(inc.netIncome/bs.totalStockholderEquity * 100, 1)

margins.columns = ["Gross Profit margin in %", "EBITDA margin in %", "EBIT margin in %", "Net Income margin in %", "OCF margin in %", "FCF margin in %", "Return on Equity in %"]
avgMargins = pd.DataFrame(margins.iloc[:10].mean(axis=0))
avgMargins = round(avgMargins, 1)
currMargins = pd.DataFrame(margins.iloc[0].T)
currMargins["10yAvg"] = avgMargins.iloc[:,0]
currMargins.columns=["Latest", "10yAvg"]


### VALUATION ###

highlights = pd.read_json("https://eodhistoricaldata.com/api/fundamentals/"+ ticker +"?api_token=" + eod_api + "&filter=Valuation,Highlights").T

highlights = highlights[["MarketCapitalization","TrailingPE", "PEGRatio", "PriceSalesTTM", "PriceBookMRQ", "EnterpriseValue", "EnterpriseValueRevenue", "EnterpriseValueEbitda"]]

valuation = pd.DataFrame(index = cf.index, columns = ["pS","pGp","pB","pOcf","pFcf","pE","evS","evEbitda", "evOcf"])

valuation.pS = round(highlights.PriceSalesTTM[0], 1)
valuation.pGp = round(highlights.MarketCapitalization[1]/inc.grossProfit[0], 1)
valuation.pB = round(highlights.PriceBookMRQ[0], 1)
valuation.pOcf = round(highlights.MarketCapitalization[1]/cf.totalCashFromOperatingActivities[0], 1)
valuation.pFcf = round(highlights.MarketCapitalization[1]/cf.freeCashFlow[0], 1)
valuation.pE = round(highlights.TrailingPE[0], 1)
valuation.evS = round(highlights.EnterpriseValueRevenue[0], 1)
valuation.evEbitda = round(highlights.EnterpriseValueEbitda[0], 1)
valuation.evOcf = round(highlights.EnterpriseValue[0]/cf.totalCashFromOperatingActivities[0], 1)

valuation = pd.DataFrame(valuation.iloc[0]).T

currValuation = pd.DataFrame(valuation.iloc[0]).T
currValuation_dict = {"Price/Sales": str(currValuation.pS.iloc[0]),
					  "Price/OCF": str(currValuation.pOcf.iloc[0]),
					  "Price/FCF": str(currValuation.pFcf.iloc[0]),
					  "Price/GP": str(currValuation.pGp.iloc[0]),
					  "Price/BV": str(currValuation.pB.iloc[0]),
					  "Price/Earnings": str(currValuation.pE.iloc[0]),
					  "EV/Sales": str(currValuation.evS.iloc[0]),
					  "EV/EBITDA": str(currValuation.evEbitda.iloc[0]),
					  "EV/OCF": str(currValuation.evOcf.iloc[0])}


### QUALITY ###

quality = pd.DataFrame(index = cf.index, columns = ["dE", "dOcf","dFcf", "netDebt","wc","gwRatio"])

totalDebt = (bs.cashAndEquivalents + bs.netDebt)
quality.dE = round(totalDebt/bs.totalStockholderEquity, 1)
quality.dOcf = round(totalDebt/cf.totalCashFromOperatingActivities, 1)
quality.dFcf = round(totalDebt/cf.freeCashFlow, 1)
quality.netDebt = bs.netDebt < 0
quality.wc = round(bs.totalCurrentAssets/bs.totalCurrentLiabilities, 1)
quality.gwRatio = round(bs.goodWill/bs.totalAssets*100, 1)

currQuality = pd.DataFrame(quality.iloc[0]).T
currQuality_dict = {"Debt/Equity": str(currQuality.dE.iloc[0]),
					"Debt/OCF": str(currQuality.dOcf.iloc[0]),
					"Debt/FCF": str(currQuality.dFcf.iloc[0]),
					"Net Debt": currQuality.netDebt[0],
					"Current Ratio/WC Multiple": str(currQuality.wc.iloc[0]),
					"Goodwill Ratio": str(currQuality.gwRatio.iloc[0]) + " %"}

### ROI ###

roi = pd.DataFrame(index = cf.index, columns = ["divYd", "adjdivYd", "fcfYd", "chgShares5y"])

roi.divYd = round(abs(cf.dividendsPaid[0])/highlights.MarketCapitalization[1]*100,1)
roi.adjdivYd = round((-cf.dividendsPaid.fillna(value=0) + cf.issuanceOfCapitalStock.fillna(value=0) - cf.salePurchaseOfStock.fillna(value=0))/highlights.MarketCapitalization[1]*100,1)
roi.fcfYd = round(cf.freeCashFlow/highlights.MarketCapitalization[1]*100,1)
chgShares = round((bs.commonStockSharesOutstanding[0] - bs.commonStockSharesOutstanding)/bs.commonStockSharesOutstanding*100,1)
roi.chgShares5y = round(chgShares[5],1)

currROI = pd.DataFrame(roi.iloc[0]).T


tab_titles = [
	"GROWTH",
	"PROFITABILITY",
	"VALUATION",
	"QUALITY",
	"ROI FOR INVESTORS"]
	
	
tabs = st.tabs(tab_titles)

with tabs[0]:
	st.header("GROWTH")
	rev5y, ni5y, div5y = st.columns(3)
	rev5y.metric(label="Revenue in USDm (5y Chg in %)", value= "{:,.0f}".format(round(inc.totalRevenue.iloc[0]/1000000,0)), delta= str(growth.rev_gth.iloc[0])+"%")
	ni5y.metric(label= "Net Income in USDm (5y Chg in %)", value = "{:,.0f}".format(round(inc.netIncome.iloc[0]/1000000,0)), delta = str(growth.ni_gth.iloc[0])+"%")
	div5y.metric(label= "Dividends in USDm (5y Chg in %)", value = "{:,.0f}".format(round(abs(cf.dividendsPaid.iloc[0]/1000000),0)), delta = str(growth.div_gth.iloc[0])+"%")
	#st.line_chart(inc[["totalRevenue","netIncome"]].pct_change(-1))

	with st.expander("WHY GROWTH MAKES A DIFFERENCE"):
		st.write("Companies need to grow in order to remain competitive and maintain their market position. As companies grow, they can achieve **economies of scale**, **reduce costs**, and **increase profitability**. Additionally, growth can lead to **new opportunities for investment**, **innovation**, and **expansion into new markets** - and these aspects are most important for us as investors to find the **next BIG growth story**.")


with tabs[1]:
	st.header("PROFITABILITY")
	
	currgpm, currebitm, currnim = st.columns(3)
	currgpm.metric(label="Gross Profit margin (vs 10y Avg)", value= str(currMargins.iloc[0,0])+"%", delta= str(round(currMargins.iloc[0,0] - currMargins.iloc[0,1], 1))+"%p")
	currebitm.metric(label= "EBIT margin (vs 10y Avg)", value = str(currMargins.iloc[2,0])+"%", delta = str(round(currMargins.iloc[2,0] - currMargins.iloc[2,1], 1))+"%p")
	currnim.metric(label= "Net Income margin (vs 10y Avg)", value = str(currMargins.iloc[3,0])+"%", delta = str(round(currMargins.iloc[3,0] - currMargins.iloc[3,1], 1))+"%p")	
	
	currocfm, currfcfm, currroe = st.columns(3)
	currocfm.metric(label="OCF margin (vs 10y Avg)", value= str(currMargins.iloc[4,0])+"%", delta= str(round(currMargins.iloc[4,0] - currMargins.iloc[4,1], 1))+"%p")
	currfcfm.metric(label= "FCF margin (vs 10y Avg)", value = str(currMargins.iloc[5,0])+"%", delta = str(round(currMargins.iloc[5,0] - currMargins.iloc[5,1], 1))+"%p")
	currroe.metric(label= "ROE (vs 10y Avg)", value = str(currMargins.iloc[6,0])+"%", delta = str(round(currMargins.iloc[6,0] - currMargins.iloc[6,1], 1))+"%p")
	#st.line_chart(margins[["Gross Profit margin in %", "OCF margin in %","Net Income margin in %","FCF margin in %"]].pct_change(-1)*100)

	with st.expander("WHY HIGH PROFITS MEAN HIGH STOCK RETURNS"):
		st.write("Profitable companies provide higher returns to shareholder. With piles of cash, financial debt is easily repaid and dividends and stock buybacks can follow a sustainable growth plan. With the help of these cash resources, companies can invest in research and highly attractive companies. Economic downturn and downswings can be mastered easily. New investors are attracted and the value of the company increases. ")

		
with tabs[2]:
	st.header("VALUATION")
	
	prices, priceocf, pricefcf = st.columns(3)
	prices.metric(label = "Price/Sales", value = round(currValuation.pS.iloc[0],1), delta = round(currValuation.pS.iloc[0]-3, 1), delta_color = "inverse")
	priceocf.metric(label = "Price/OCF", value = round(currValuation.pOcf.iloc[0],1), delta = round(currValuation.pOcf.iloc[0]-10, 1), delta_color = "inverse")
	pricefcf.metric(label = "Price/FCF", value = round(currValuation.pFcf.iloc[0],1), delta = round(currValuation.pFcf.iloc[0]-10, 1), delta_color = "inverse")
	
	pgp, pbv, pe = st.columns(3)
	pgp.metric(label = "Price/Gross Profit", value = round(currValuation.pGp.iloc[0],1), delta = round(currValuation.pGp.iloc[0]-8, 1), delta_color = "inverse")
	pbv.metric(label = "Price/Book Value", value = round(currValuation.pB.iloc[0],1), delta = round(currValuation.pB.iloc[0]-3, 1), delta_color = "inverse")
	pe.metric(label = "Price/Earnings", value = round(currValuation.pE.iloc[0],1), delta = round(currValuation.pE.iloc[0]-15, 1), delta_color = "inverse")
	
	evs, evebitda, evocf = st.columns(3)
	evs.metric(label = "EV/Sales", value = round(currValuation.evS.iloc[0],1), delta = round(currValuation.evS.iloc[0]-3, 1), delta_color = "inverse")
	evebitda.metric(label = "EV/EBITDA", value = round(currValuation.evEbitda.iloc[0],1), delta = round(currValuation.evEbitda.iloc[0]-8, 1), delta_color = "inverse")	
	evocf.metric(label = "EV/OCF", value = round(currValuation.evOcf.iloc[0], 1), delta = round(currValuation.evOcf.iloc[0]-10, 1), delta_color = "inverse")

	with st.expander("WHY VALUATION IS KEY TO AVOID RISK"):
		st.write("With the help of suitable valuation KPIs, investors identify stocks that are undervalued by the market, and therefore have potential for long-term growth. Value investing can also help to reduce the risk of investing in overpriced stocks, which may be more susceptible to market downturns. ")


with tabs[3]:
	st.header("QUALITY")
	
	de, docf, dfcf = st.columns(3)
	de.metric(label = "Debt/Equity Multiple", value = round(currQuality.dE.iloc[0], 1), delta = round(currQuality.dE.iloc[0]-1,1), delta_color = "inverse")
	docf.metric(label = "Debt/OCF Multiple", value = round(currQuality.dOcf.iloc[0], 1), delta = round(currQuality.dOcf.iloc[0]-1,1), delta_color = "inverse")
	dfcf.metric(label = "Debt/FCF Multiple", value = round(currQuality.dFcf.iloc[0], 1), delta = round(currQuality.dFcf.iloc[0]-2,1), delta_color = "inverse")

	nd, wcmult, gwratio = st.columns(3)
	nd.metric(label = "Net Cash", value = currQuality.netDebt[0])
	wcmult.metric(label = "Current Ratio (WC Multiple)", value = round(currQuality.wc.iloc[0], 1), delta = round(currQuality.wc.iloc[0] - 2, 1))
	gwratio.metric(label = "Goodwill Ratio", value = str(round(currQuality.gwRatio.iloc[0], 1))+"%", delta = str(round(currQuality.gwRatio.iloc[0]-10, 1))+"%", delta_color="inverse")	

	with st.expander("WHY QUALITY METRICS MAKE YOUR INVESTMENTS SUSTAINABLE"):
		st.write("Companies that are profitable and have a strong financial position may have greater potential for growth and expansion. : Companies with low debt levels are generally considered to be less risky investments because they are less vulnerable to market downturns and economic fluctuations. Quality stocks can be especially attractive in times of market volatility.")


with tabs[4]:
	st.header("ROI FOR INVESTORS")
	
	divyd, adjdivyd = st.columns(2)
	divyd.metric(label = "Dividend Yield (last FY)", value = str(round(currROI.divYd.iloc[0], 1))+"%", delta = str(round(currROI.divYd.iloc[0]-0, 1))+"%")
	adjdivyd.metric(label = "Curr Adj Div Yield (last FY)", value = str(round(currROI.adjdivYd.iloc[0], 1))+"%", delta = str(round(currROI.adjdivYd.iloc[0] - 5, 1))+str("%"))
	
	fcfyd, chgshares = st.columns(2)
	fcfyd.metric(label = "FCF Yield (last FY)", value = str(round(currROI.fcfYd.iloc[0], 1))+"%", delta = str(round(currROI.fcfYd.iloc[0]-10, 1))+"%")
	chgshares.metric(label = "Change in No of Shares (in 5y)", value = str(round(currROI.chgShares5y.iloc[0], 1))+"%", delta = str(round(currROI.chgShares5y.iloc[0]+10, 1))+"%", delta_color="inverse")

	with st.expander("WHY RETURN ON INVESTMENT SHOULD INTEREST YOU MOST"):
		st.write("Dividend-paying stocks can provide a steady stream of income for investors, which can be especially attractive in low-interest-rate environments. This income can be reinvested in the company's stock or used for other investment opportunities. Companies that buy back their own stock may boost the stock price, potentially increasing investors' capital gains. Additionally, companies that pay dividends may attract more investors and increase demand for their shares, which can drive up the stock price. They may be seen as shareholder-friendly, which can improve the company's reputation and attract more investors.")
