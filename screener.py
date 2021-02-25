#-----------------------------------------------------------------------
# screener.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 14/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of this code is to let the user set different parametrs for 5 different categories and show all stocks from a list that fit that desrcription

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
from dataScraping import *
from pointSystem import *

def accessWeb(Ticker:str):

	url1 = 'http://finviz.com/quote.ashx?t=' + Ticker
	req1 = Request(url1, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded1 = urlopen(req1, timeout = 1).read() #We open the page and read all the raw info
   	#webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup1 = BeautifulSoup(webpage_coded1, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url2 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials'
	req2 = Request(url2, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded2 = urlopen(req2, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded2 = webpage_coded2.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup2 = BeautifulSoup(webpage_coded2, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url3 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/balance-sheet'
	req3 = Request(url3, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded3 = urlopen(req3, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup3 = BeautifulSoup(webpage_coded3, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ##################################################################################################################################################

	url4 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/financials/cash-flow'
	req4 = Request(url4, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded4 = urlopen(req4, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup4 = BeautifulSoup(webpage_coded4, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

    ###################################################################################################################################################

	url5 = 'https://www.marketwatch.com/investing/stock/' + Ticker + '/analystestimates?mod=mw_quote_tab'
	req5 = Request(url5, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded5 = urlopen(req5, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup5 = BeautifulSoup(webpage_coded5, 'html.parser') #Parsing(breaking the code down into relevant info) the html code
	
	#####################################################################################################################################################

	url6 = 'https://finance.yahoo.com/quote/' + Ticker + '/analysis?p=' + Ticker
	req6 = Request(url6, headers = {'User-Agent': 'Mozilla/5'}) #The website restricts urllib request so we must use request switching the user agent to mozilla 
	webpage_coded6 = urlopen(req6, timeout = 1).read() #We open the page and read all the raw info
    #webpage_decoded = webpage_coded.decode('utf-8') #Since it is coded in utf-8 we decode it to be able to process it

	soup6 = BeautifulSoup(webpage_coded6, 'html.parser') #Parsing(breaking the code down into relevant info) the html code

	return soup1, soup2, soup3, soup4, soup5, soup6

def enterScore(category:str, correct = False, score = -1) -> float:	
	#function to see if the values introduced are correct, so no errors are produced
	#we must also make sure that the numbers stay between the established parameters
	while correct == False or score > 10 or score < 0:
		correct = True
		try:
			score = float(input(f'Enter a Minimum {category} Score(0.0 - 10.0): '))
			if score > 10 or score < 0:
				print('Incorrect Value Entered... Try Again...')
		except:
			print('Incorrect Value Entered... Try Again...')
			correct = False
	return score			

def main ():
	#first we get all the ticker to be analyzed
	listTickers = []
	Tickers = str(input('Enter a List of Tickers seperated by a space: '))
	listTickers += Tickers.split(' ')

	#find the numbers that the user wants for each approved ticker
	ValueScore = enterScore('Value')
	FutureScore = enterScore('Future')
	HealthScore = enterScore('Health')
	PastScore = enterScore('Past')
	InsiderScore = enterScore('Insider')

	approvedTickers = []
	for Ticker in listTickers:
		print()
		print()
		#try to access the webpage of each ticker, if one doesnt exist we tell the user that it is not available
		wrong = False
		try:
			print(f'Webscraping info for {Ticker.upper()}...')
			soup1, soup2, soup3, soup4, soup5, soup6 = accessWeb(Ticker)
		except:
			wrong = True

		#############################################################################################################################
		
		if wrong:
			print(f'{Ticker.upper()} not available')
		else:	
			#if it is available, we webscrape and evaluate each individual stock
			print(f'Analyzing and Assesing Data...')
			PE, PEG, PS, PB, MarketCap, DebtEquity, Recom, InsiderTrans, InstitutionTrans, ROA, ROE, AvgVolume, Price, LastChange, PerfWeek, PerfMonth, PerfYear, YearHighPercent, EPSNextY, EPSNext5Y = fundamentalInfoFVZ(soup1)

			RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5, InterestExpense, NetIncomePast5 = IncomeStatementMW(soup2)
			TotalEquity, GrowthLA, GrowthDA, TotalLiabilities, TotalCurrentLiabilities, LongTermLiabilities, TotalAssets, TotalCurrentAssets, LongTermAssets, ShortTermDebt, LongTermDebt = BalanceSheet(soup3)
			FreeCashFlow, TotalDebtReduction, NetOperatingCashFlow = CashFlow(soup4)

			estimateRevision1, estimateRevision2 = EPSRevisions(soup5)
			HighTarget, LowTarget, AverageTarget, NumberOfRatings = PriceTargets(soup5)

			EPSestimates = EPSEstimates(soup5)
			RevenueGrowthNextY = RevenuesEstimates(soup6)

			columnNames, xValues, Buy, Overweight, Hold, Underweight, Sell = Recomendations(soup5)

			###############################################################################################################################

			pointsEarnedHealth, TotalpointsHealth = health(DebtEquity, LongTermLiabilities, NetOperatingCashFlow, EBIT, InterestExpense, TotalCurrentAssets, TotalCurrentLiabilities, TotalLiabilities, GrowthLA, TotalEquity, ShortTermDebt, LongTermDebt, TotalDebtReduction, GrowthDA, TotalAssets)
			pointsEarnedFuture, TotalpointsFuture = future(EPSNextY, EPSNext5Y, estimateRevision1, estimateRevision2, AverageTarget, LowTarget, Buy, Overweight, Hold, Underweight, Sell, RevenueGrowthNextY, Price)
			pointsEarnedPast, TotalpointsPast = past(ROA, ROE, RevenuePast5, RevenueGrowthPast5, EPSpast5, EPSgrowthPast5, NetIncomePast5)
			pointsEarnedInsiders, TotalpointsInsiders = insiders(InsiderTrans, InstitutionTrans)
			pointsEarnedValue, TotalpointsValue = value(PE, PEG, PS, PB, YearHighPercent, EBITDA, LongTermDebt, ShortTermDebt, FreeCashFlow, MarketCap)

			################################################################################################################################

			#if anyone of the parameters is not met we discard the ticker and dont check the rest of the parameters
			check = True
			if (pointsEarnedValue / TotalpointsValue) * 10 < ValueScore and check:
				check = False
			if (pointsEarnedPast / TotalpointsPast) * 10 < PastScore and check:
				check = False
			if (pointsEarnedFuture / TotalpointsFuture) * 10 < FutureScore and check:
				check = False
			if (pointsEarnedHealth / TotalpointsHealth)  * 10 < HealthScore and check:
				check = False
			if (pointsEarnedInsiders / TotalpointsInsiders) * 10 < InsiderScore and check:
				check = False		

			#if it is approved we add it to the last and tell the user that it has been approved 	
			if check:
				print(f'{Ticker.upper()} APPROVED')
				approvedTickers += [Ticker]
			else:
				print(f'{Ticker.upper()} FAILED')		

	print()
	#finally we show the list of approved tickers or if there arent any			
	if len(approvedTickers) != 0:
		print('APPROVED TICKERS: ')
		for Ticker in approvedTickers:
			print(Ticker.upper()) 
	else:
		print('NO APPROVED TICKERS')						

			













if __name__ == '__main__': main()