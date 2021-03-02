#-----------------------------------------------------------------------
# screener.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 14/02/2020
# Version: 1.0
#-----------------------------------------------------------------------

#The objective of this code is to check the scores for all stock tickers in the Nasdaq, AMEX and NYSE and update there scores in the five categories to the database

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from typing import List
from dataScraping import *
from pointSystem import *

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

	#find the numbers that the user wants for each approved ticker
	ValueScore = enterScore('Value')
	FutureScore = enterScore('Future')
	HealthScore = enterScore('Health')
	PastScore = enterScore('Past')
	InsiderScore = enterScore('Insider')

	approvedTickers = []
	
			
			#if anyone of the parameters is not met we discard the ticker and dont check the rest of the parameters
			check = True
			print(Value)
			print(pointsEarnedValue, TotalpointsValue)
			if (Value < ValueScore or TotalpointsValue < 10) and check:
				check = False
			if Past < PastScore and check:
				check = False
			if Future < FutureScore and check:
				check = False
			if Health < HealthScore and check:
				check = False
			if Insiders < InsiderScore and check:
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