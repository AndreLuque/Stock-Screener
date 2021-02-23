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

def main ():
	#first we get all the ticker to be analyzed
	listTicker = []
	Tickers = str(input('Enter a List of Tickers seperated by a space: '))
	listTicker += Tickers.split(' ')
	print(listTicker)












if __name__ == '__main__': main()