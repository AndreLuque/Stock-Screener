#-----------------------------------------------------------------------
# screener.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 14/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of this code is to check the scores for all stock tickers in the Nasdaq, AMEX and NYSE and update there scores in the five categories to the database

from typing import List
import pandas as pd

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

def minValue(name:str, value = 0, correct = False, option = '') -> float:
	#ask the user if he they want to set a minimum volume quantity
	while option != 'Yes' and option != 'No':
		try:
			option = str(input(f'Would you like to enter a minimum {name}? (Yes/No): '))
		except:
			None

	#if the user want to we make sure that they enter a volume that is a natural number	
	if option == 'Yes':	
		while value <= 0:
			try:
				value = int(input(f'Enter the minimum {name}: '))
			except:
				None	
	else:
		value = 0

	return value	

def dollarSign(x:str) -> float:
	return float(x[1:])


def main ():

	#get the dataframes for all tickers of nasdaq amex and nyse
	NasdaqDF = pd.read_excel('Nasdaq.xlsx')
	AmexDF = pd.read_excel('AMEX.xlsx')
	NyseDF = pd.read_excel('NYSE.xlsx')

	#changing the prices to floats without the dollar sign
	NasdaqDF['Last Sale'] = NasdaqDF['Last Sale'].apply(dollarSign)
	AmexDF['Last Sale'] = AmexDF['Last Sale'].apply(dollarSign)
	NyseDF['Last Sale'] = NyseDF['Last Sale'].apply(dollarSign)

	#we unite the different dataframes and then we reindex the whole dataframe rows
	dfs = [NasdaqDF, AmexDF, NyseDF]
	TickersDF = pd.concat(dfs)
	TickersDF.reset_index(drop = True, inplace = True)

	#find the numbers that the user wants for each approved ticker
	ValueScore = enterScore('Value')
	FutureScore = enterScore('Future')
	HealthScore = enterScore('Health')
	PastScore = enterScore('Past')
	InsiderScore = enterScore('Insider')

	print()
	Volume = minValue('Volume')

	print()
	MarketCap = minValue('Market Cap')

	print()
	Price = minValue('Price')

	print()
	print()

	#Turn the values in the columns to numeric so that we can compare them
	TickersDF['Value'] = pd.to_numeric(TickersDF['Value'], errors = 'coerce')
	TickersDF['Past'] = pd.to_numeric(TickersDF['Past'], errors = 'coerce')
	TickersDF['Future'] = pd.to_numeric(TickersDF['Future'], errors = 'coerce')
	TickersDF['Health'] = pd.to_numeric(TickersDF['Health'], errors = 'coerce')
	TickersDF['Insiders'] = pd.to_numeric(TickersDF['Insiders'], errors = 'coerce')
		
	#we search for tickers that pass the parameter values set by the user	
	approvedDF = TickersDF.loc[(TickersDF['Value'] >= ValueScore) & (TickersDF['Future'] >= FutureScore) & (TickersDF['Past'] >= PastScore) & (TickersDF['Health'] >= HealthScore) & (TickersDF['Insiders'] >= InsiderScore) & (TickersDF['Volume'] >= Volume) & (TickersDF['Market Cap'] >= MarketCap) & (TickersDF['Last Sale'] >= Price)]	

	#we format the dataframe, so that we are able to visualize all the columns and row
	pd.set_option('display.max_columns', None, 'display.max_rows', None)
	pd.set_option('display.width', None)
	#pd.set_option('display.max_colwidth', -1)
	
	#shows a final list of the approved tickers
	approvedTickers = list(approvedDF['Name'])

	#we delete columns with irrelevant info to visualize to approved tickers better
	del approvedDF['Net Change'], approvedDF['IPO Year'], approvedDF['Industry'], approvedDF['Sector'], approvedDF['% Change'], approvedDF['Name']

	#shows the dataframe of the approved tickers
	print(approvedDF)

	print()
	print()
	print(f'List of Approved Tickers: {approvedTickers}')



if __name__ == '__main__': main() 