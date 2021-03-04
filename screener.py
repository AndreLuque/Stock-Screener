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
		option = str(input(f'Would you like to enter a minimum {name}? (Yes/No): '))

	#if the user want to we make sure that they enter a volume that is a natural number	
	if option == 'Yes':	
		while value <= 0:
			value = int(input(f'Enter the minimum Volume: '))
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
	NasdaqDF['Value'] = pd.to_numeric(NasdaqDF['Value'], errors = 'coerce')
	NasdaqDF['Past'] = pd.to_numeric(NasdaqDF['Past'], errors = 'coerce')
	NasdaqDF['Future'] = pd.to_numeric(NasdaqDF['Future'], errors = 'coerce')
	NasdaqDF['Health'] = pd.to_numeric(NasdaqDF['Health'], errors = 'coerce')
	NasdaqDF['Insiders'] = pd.to_numeric(NasdaqDF['Insiders'], errors = 'coerce')
		
	#we search for tickers that pass the parameter values set by the user	
	approvedDF = NasdaqDF.loc[(NasdaqDF['Value'] >= ValueScore) & (NasdaqDF['Future'] >= FutureScore) & (NasdaqDF['Past'] >= PastScore) & (NasdaqDF['Health'] >= HealthScore) & (NasdaqDF['Insiders'] >= InsiderScore) & (NasdaqDF['Volume'] >= Volume) & (NasdaqDF['Market Cap'] >= MarketCap) & (NasdaqDF['Last Sale'] >= Price)]	
	
	#we delete columns with irrelevant info to visualize to approved tickers better
	del approvedDF['Net Change'], approvedDF['IPO Year'], approvedDF['Industry'], approvedDF['Sector'], approvedDF['Name']

	#we format the dataframe, so that we are able to visualize all the columns and row
	pd.set_option('display.max_columns', None, 'display.max_rows', None)
	pd.set_option('display.width', None)
	#pd.set_option('display.max_colwidth', -1)

	#shows the dataframe of the approved tickers
	print(approvedDF)
	
	#shows a final list of the approved tickers
	print()
	print()
	approvedTickers = list(approvedDF['Symbol'])
	print(f'List of Approved Tickers: {approvedTickers}')



if __name__ == '__main__': main() 