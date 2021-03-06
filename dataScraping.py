# -----------------------------------------------------------------------
# dataScraping.py
# Description:
# Author: André Luiz Queiroz Costa
# Date: 03/02/2020
# Version: 1.0
# -----------------------------------------------------------------------

# The objective of this code is to retrieve all the necessary information that we need by scraping different
# webpages, so that we can later commence a full stock analysis with this info.

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from typing import List
from urllib.request import urlopen, Request
import math


# import re
# import lxml

def fundamentalInfoFVZ(soup, PE = -1, PEG = -1, PS = -1, PB = -1, MarketCap = -1, DebtEquity = -1, Recom = -1, InsiderTrans = -1, InstitutionTrans = -1, ROA = -1, ROE = -1, AvgVolume = -1, Price = -1, LastChange = -1, PerfWeek = -1, PerfMonth = -1, PerfYear = -1, YearHighPercent = -1, EPSNextY = -1, EPSNext5Y = -1) -> float:
    # We inspect the webpage to finde the html tags of the pbjects that we want
    # Transforms the html to a pandas dataframe
    check = True
    try:
        fundamentals = pd.read_html(str(soup),
                                    attrs={'class': 'snapshot-table2'})  # Can only do this if class type is a table
    except:
        check = False

    if check:    
        PE = fundamentals[0][3][0]  # Price to earnings ratio
        if PE == '-':
            PE = -1
        PEG = fundamentals[0][3][2]  # Price to earnings growth ratio
        if PEG == '-':
            PEG = -1
        PS = fundamentals[0][3][3]  # Price to sales ratio
        if PS == '-':
            PS = -1
        PB = fundamentals[0][3][4]  # Price to book value ratio
        if PB == '-':
            PB = -1
        DebtEquity = fundamentals[0][3][9]  # Debt to equity ratio
        if DebtEquity == '-':
            DebtEquity = -1
        Recom = fundamentals[0][1][11]  # Analysts recomendations
        if Recom == '-':
            Recom = -1
        MarketCap = fundamentals[0][1][1]  # Number of shares times the the current price of each share
        if MarketCap == '-':
            MarketCap = -1
        else:
            MarketCap = float(MarketCap[0:-1])  # When scraped comes with a B or M at the end we tranform it into number
            MarketCap = MarketCap * 1000000000  # The value is given to use in billions so we transform it
        InsiderTrans = fundamentals[0][7][1]  # The percentage of recent movements by insiders in the company
        if InsiderTrans == '-':
            InsiderTrans = -1
        else:
            InsiderTrans = InsiderTrans[0:-1]
        InstitutionTrans = fundamentals[0][7][3]  # The percentage of recent mvoements made my hedgefunds and institutions
        if InstitutionTrans == '-':
            InstitutionTrans = -1
        else:
            InstitutionTrans = InstitutionTrans[0:-1]
        ROA = fundamentals[0][7][4]  # Return on assets
        if ROA == '-':
            ROA = -1
        else:
            ROA = ROA[0:-1]
        ROE = fundamentals[0][7][5]  # Return on equity
        if ROE == '-':
            ROE = -1
        else:
            ROE = ROE[0:-1]
        AvgVolume = fundamentals[0][9][10]  # The amount of shares bought and sold in a single trading period
        if AvgVolume == '-':
            AvgVolume = -1
        else:
            if AvgVolume[-1] == 'B':
                AvgVolume = float(AvgVolume[0:-1]) * 1000000000
            elif AvgVolume[-1] == 'M':
                AvgVolume = float(AvgVolume[0:-1]) * 1000000
            elif AvgVolume[-1] == 'K':
                AvgVolume = float(AvgVolume[0:-1]) * 1000
            else:
                AvgVolume = float(AvgVolume)    
        Price = fundamentals[0][11][10]  # price per share
        if Price == '-':
            Price = -1
        LastChange = fundamentals[0][11][11]  # The price percentage change in the last trading day
        if LastChange == '-':
            LastChange = -1
        else:
            LastChange = LastChange[0:-1]
        PerfWeek = fundamentals[0][11][0]  # The price percentage change in the last week
        if PerfWeek == '-':
            PerfWeek = -1
        else:
            PerfWeek = PerfWeek[0:-1]
        PerfMonth = fundamentals[0][11][1]  # The price percentage change in the last month
        if PerfMonth == '-':
            PerfMonth = -1
        else:
            PerfMonth = PerfMonth[0:-1]
        PerfYear = fundamentals[0][11][4]  # The price percentage change in the last year
        if PerfYear == '-':
            PerfYear = -1
        else:
            PerfYear = PerfYear[0:-1]
        YearHighPercent = fundamentals[0][9][6]  # The percent difference from its 52 week high
        if YearHighPercent == '-':
            YearHighPercent = -1
        else:
            YearHighPercent = YearHighPercent[0:-1]
        EPSNextY = fundamentals[0][5][4]  # Earnings per share growth for next year
        if EPSNextY == '-':
            EPSNextY = -1
        else:
            EPSNextY = EPSNextY[0:-1]
        EPSNext5Y = fundamentals[0][5][5]  # Earnings per share growth for next 5 years
        if EPSNext5Y == '-':
            EPSNext5Y = -1
        else:
            EPSNext5Y = EPSNext5Y[0:-1]

    return PE, PEG, PS, PB, MarketCap, DebtEquity, Recom, InsiderTrans, InstitutionTrans, ROA, ROE, AvgVolume, Price, LastChange, PerfWeek, PerfMonth, PerfYear, YearHighPercent, EPSNextY, EPSNext5Y


def IncomeStatementMW(soup, RevenuePast5 = [], RevenueGrowthPast5 = -1, EBITDA = -1, EBIT = -1, DepreciationAmortization = -1, EPSpast5 = [], EPSgrowthPast5 = -1, InterestExpense = -1, NetIncomePast5 = []) -> float:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    check = True
    try:
        IncomeStatement = pd.read_html(str(soup), attrs={
            'class': 'table table--overflow align--right'})  # Can only do this if class type is a table
    except:
        check = False
    if check:    
        IncomeStatement = IncomeStatement[0]  # Only getting the table since there are more objects with the same class
        IncomeStatement.columns = pd.RangeIndex(0, len(
            IncomeStatement.columns))  # Indexing the columns as numbers so that the differences in the name of columns wont matter
        # There is no defined number of columns so we set it to len

        # We add all the columns except the first which is the title and the last which is Nan
        RevenuePast5t = []
        RevenuePast5 = []
        for i in range(1, len(IncomeStatement.columns) - 1):
            RevenuePast5t += [IncomeStatement[i][0]]
            # We must change the values from billions and millions to full numbers
        
        for i in range(len(RevenuePast5t)):
            if RevenuePast5t[i] != '-':
                if RevenuePast5t[i][0] == '(':
                    RevenuePast5t[i] = '-' + RevenuePast5t[i][1:-1]  
                if RevenuePast5t[i][-1] == 'T':
                    RevenuePast5 += [float(RevenuePast5t[i][0:-1]) * 1000000000000]    
                elif RevenuePast5t[i][-1] == 'B':
                    RevenuePast5 += [float(RevenuePast5t[i][0:-1]) * 1000000000]
                elif RevenuePast5t[i][-1] == 'M':
                    RevenuePast5 += [float(RevenuePast5t[i][0:-1]) * 1000000]
                elif RevenuePast5t[i][-1] == 'K':
                    RevenuePast5 += [float(RevenuePast5t[i][0:-1]) * 1000]
                else:
                    RevenuePast5 += [float(RevenuePast5t[i])]    

        # We take the growth year to year and average it. We must take off the percentage symbol from each one to be able to do the calculations
        RevenueGrowthPast5 = 0
        for i in range(2, len(IncomeStatement.columns) - 1):
            if IncomeStatement[i][1] != '-':     
                RevenueGrowthPast5 += float((IncomeStatement[i][1].replace(',', ''))[0:-1])
        if RevenueGrowthPast5 != 0 and len(IncomeStatement.columns) - 3 != 0:
            RevenueGrowthPast5 = RevenueGrowthPast5 / (len(IncomeStatement.columns) - 3)

        # We check if the Depreciation and Amortization exists in the income statement, and then we isolate it and convert the number from millions
        NetIncomePast5 = []
        if len(IncomeStatement.loc[IncomeStatement[0] == 'Net Income Net Income']) == 1:
            for i in range(1, len(IncomeStatement.columns) - 1):
                NetIncome = IncomeStatement.loc[IncomeStatement[0] == 'Net Income Net Income'][i]
                NetIncome = NetIncome[int(
                    NetIncome.index.values)]  # We dont know what position it is in so we find out and take only that specific value
                if NetIncome[0] == '(':
                    NetIncome = '-' + NetIncome[1:-1]
                if NetIncome[-1] == 'T':
                    NetIncome = float(NetIncome[0:-1]) * 1000000000000
                elif NetIncome[-1] == 'B':
                    NetIncome = float(NetIncome[0:-1]) * 1000000000
                elif NetIncome[-1] == 'M':
                    NetIncome = float(NetIncome[0:-1]) * 1000000
                elif NetIncome[-1] == 'K':
                    NetIncome = float(NetIncome[0:-1]) * 1000
                elif NetIncome == '-':
                    NetIncome = -1
                else:
                    NetIncome = float(NetIncome)    
                NetIncomePast5 += [NetIncome]
        else:
            NetIncomePast5 = -1    

            # We check if the EBITDA exists in the income statement, and then we isolate it and convert the number from millions
        EBITDA = 0
        if len(IncomeStatement.loc[IncomeStatement[0] == 'EBITDA EBITDA']) == 1:
            EBITDA = IncomeStatement.loc[IncomeStatement[0] == 'EBITDA EBITDA'][len(IncomeStatement.columns) - 2]
            EBITDA = EBITDA[int(
                EBITDA.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if EBITDA[0] == '(':
                EBITDA = '-' + EBITDA[1:-1]
            if EBITDA[-1] == 'T':
                EBITDA = float(EBITDA[0:-1]) * 1000000000000
            elif EBITDA[-1] == 'B':
                EBITDA = float(EBITDA[0:-1]) * 1000000000
            elif EBITDA[-1] == 'M':
                EBITDA = float(EBITDA[0:-1]) * 1000000
            elif EBITDA[-1] == 'K':
                EBITDA = float(EBITDA[0:-1]) * 1000
            elif EBITDA == '-':
                EBITDA = -1
            else:
                EBITDA = float(EBITDA)    
        else:
            EBITDA = -1

        # We check if the Depreciation and Amortization exists in the income statement, and then we isolate it and convert the number from millions
        DepreciationAmortization = 0
        if len(IncomeStatement.loc[
                   IncomeStatement[0] == 'Depreciation & Amortization Expense Depreciation & Amortization Expense']) == 1:
            DepreciationAmortization = IncomeStatement.loc[
                IncomeStatement[0] == 'Depreciation & Amortization Expense Depreciation & Amortization Expense'][
                len(IncomeStatement.columns) - 2]
            DepreciationAmortization = DepreciationAmortization[int(
                DepreciationAmortization.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if DepreciationAmortization[0] == '(':
                DepreciationAmortization = '-' + DepreciationAmortization[1:-1]
            if DepreciationAmortization[-1] == 'T':
                DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000000000000
            elif DepreciationAmortization[-1] == 'B':
                DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000000000
            elif DepreciationAmortization[-1] == 'M':
                DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000000
            elif DepreciationAmortization[-1] == 'K':
                DepreciationAmortization = float(DepreciationAmortization[0:-1]) * 1000
            elif DepreciationAmortization == '-':
                DepreciationAmortization = -1
            else:
                DepreciationAmortization = float(DepreciationAmortization)    
        else:
            DepreciationAmortization = -1

            # We check if the EPS of the past 5 years exists in the income statement, and then we isolate it and convert the number from millions
        EPSpast5 = []
        if len(IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) EPS (Basic)']) == 1:
            # We want the last 5 years EPS so we isolate each case and add it to the list
            for i in range(1, len(IncomeStatement.columns) - 1):
                EPS = IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) EPS (Basic)'][i]
                if EPS[int(EPS.index.values)] != '-':
                    # The negative values for this in the website appear with a parentesis before it, so we must correct that
                    if EPS[int(EPS.index.values)][0] == '(':
                        if EPS[int(EPS.index.values)][-2] == 'K':
                            EPSpast5 += [-1000 * (float(EPS[int(EPS.index.values)][1:-2]))]
                        elif EPS[int(EPS.index.values)][-2] == 'M':
                            EPSpast5 += [-1000000 * (float(EPS[int(EPS.index.values)][1:-2]))]     
                        elif EPS[int(EPS.index.values)][-2] == 'B':
                            EPSpast5 += [-1000000000 * (float(EPS[int(EPS.index.values)][1:-2]))]          
                        else:    
                            EPSpast5 += [-1 * (float(EPS[int(EPS.index.values)][1:-1]))]
                    else:
                        if EPS[int(EPS.index.values)][-1] == 'K':
                            EPSpast5 += [1000 * float(EPS[int(EPS.index.values)][0:-1])]
                        elif EPS[int(EPS.index.values)][-1] == 'M':
                            EPSpast5 += [1000000 * float(EPS[int(EPS.index.values)][0:-1])]   
                        elif EPS[int(EPS.index.values)][-1] == 'B':
                            EPSpast5 += [1000000000 * (float(EPS[int(EPS.index.values)][0:-1]))]        
                        else:    
                            EPSpast5 += [float(EPS[int(EPS.index.values)])]

        EPSgrowthPast5 = 0
        count = 0
        if len(IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) Growth EPS (Basic) Growth']) == 1:
            for i in range(2, len(IncomeStatement.columns) - 1):
                EPS = IncomeStatement.loc[IncomeStatement[0] == 'EPS (Basic) Growth EPS (Basic) Growth'][i]
                if EPS[int(EPS.index.values)] != '-':
                    # We search to see if there are any commas and we remove them so that it can be converted to float
                    EPSgrowthPast5 += float((EPS[int(EPS.index.values)].replace(',', ''))[0:-1])
                    count += 1
            if count != 0:
                EPSgrowthPast5 = EPSgrowthPast5 / count

        # Since the statement doesnt give us EBIT, we calculate it by using other metrics, first making sure we have these
        EBIT = 0
        if EBITDA != -1:
            EBIT = float(EBITDA) - float(DepreciationAmortization)
        # sometimes EBITDA doesnt exist(Insurance companies) and EBIT is equal to Operating income before interest expense and taxes
        else:
            if len(IncomeStatement.loc[IncomeStatement[
                                           0] == 'Operating Income Before Interest Expense Operating Income Before Interest Expense']) == 1:
                EBIT = IncomeStatement.loc[IncomeStatement[
                                               0] == 'Operating Income Before Interest Expense Operating Income Before Interest Expense'][
                    len(IncomeStatement.columns) - 2]
                EBIT = EBIT[int(
                    EBIT.index.values)]  # We dont know what position it is in so we find out and take only that specific value
                if EBIT[0] == '(':
                    EBIT = '-' + EBIT[1:-1]
                if EBIT[-1] == 'T':
                    EBIT = float(EBIT[0:-1]) * 1000000000000    
                elif EBIT[-1] == 'B':
                    EBIT = float(EBIT[0:-1]) * 1000000000
                elif EBIT[-1] == 'M':
                    EBIT = float(EBIT[0:-1]) * 1000000
                elif EBIT[-1] == 'K':
                    EBIT = float(EBIT[0:-1]) * 1000
                elif EBIT == '-':
                    EBIT = -1
                else:
                    EBIT = float(EBIT)    
            else:
                EBIT = -1

                # We check if the InterestExpense exists in the income statement, and then we isolate it and convert the number from millions
        InterestExpense = 0
        if len(IncomeStatement.loc[IncomeStatement[0] == 'Interest Expense Interest Expense']) == 1:
            InterestExpense = IncomeStatement.loc[IncomeStatement[0] == 'Interest Expense Interest Expense'][
                len(IncomeStatement.columns) - 2]
            InterestExpense = InterestExpense[int(
                InterestExpense.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if InterestExpense[-1] == 'T':
                InterestExpense = float(InterestExpense[0:-1]) * 1000000000000
            elif InterestExpense[-1] == 'B':
                InterestExpense = float(InterestExpense[0:-1]) * 1000000000
            elif InterestExpense[-1] == 'M':
                InterestExpense = float(InterestExpense[0:-1]) * 1000000
            elif InterestExpense[-1] == 'K':
                InterestExpense = float(InterestExpense[0:-1]) * 1000
            elif InterestExpense == '-':
                InterestExpense = -1
            else:
                InterestExpense = float(InterestExpense)    
                # We make sure that interest expense is not named in another name(happens with insurance companies)
        else:
            if len(IncomeStatement.loc[IncomeStatement[
                                           0] == 'Interest Expense (excl. Interest Capitalized) Interest Expense (excl. Interest Capitalized)']) == 1:
                InterestExpense = IncomeStatement.loc[IncomeStatement[
                                                          0] == 'Interest Expense (excl. Interest Capitalized) Interest Expense (excl. Interest Capitalized)'][
                    len(IncomeStatement.columns) - 2]
                InterestExpense = InterestExpense[int(
                    InterestExpense.index.values)]  # We dont know what position it is in so we find out and take only that specific value
                if InterestExpense[-1] == 'T':
                    InterestExpense = float(InterestExpense[0:-1]) * 1000000000000
                elif InterestExpense[-1] == 'B':
                    InterestExpense = float(InterestExpense[0:-1]) * 1000000000
                elif InterestExpense[-1] == 'M':
                    InterestExpense = float(InterestExpense[0:-1]) * 1000000
                elif InterestExpense[-1] == 'K':
                    InterestExpense = float(InterestExpense[0:-1]) * 1000
                elif InterestExpense == '-':
                    InterestExpense = -1
                else: 
                    InterestExpense = float(InterestExpense)    
            else:
                InterestExpense = -1

    return RevenuePast5, RevenueGrowthPast5, EBITDA, EBIT, DepreciationAmortization, EPSpast5, EPSgrowthPast5, InterestExpense, NetIncomePast5


def BalanceSheet(soup, TotalEquity = -1, GrowthLA = -1, GrowthDA = -1, TotalLiabilities = -1, TotalCurrentLiabilities = -1, LongTermLiabilities = -1, TotalAssets = -1, TotalCurrentAssets = -1, LongTermAssets = -1, ShortTermDebt = -1, LongTermDebt = -1) -> float:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    # Balance sheet is broken up into these two categories
    check = True
    try:
        BalanceSheet = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'})
        Assets = BalanceSheet[0]
        Liabilities = BalanceSheet[1]
    except:
        check = False
    
    if check:    
        Assets.columns = pd.RangeIndex(0, len(
            Assets.columns))  # Indexing the columns as numbers so that the differences in the name of columns wont matter

        # We check if the Total Assets exists in the income statement, and then we isolate it and convert the number from millions or billions
        TotalAssets = 0
        if len(Assets.loc[Assets[0] == 'Total Assets Total Assets']) == 1:
            TotalAssets = Assets.loc[Assets[0] == 'Total Assets Total Assets'][len(Assets.columns) - 2]
            TotalAssets = TotalAssets[int(
                TotalAssets.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            # Some companies have assets in the trillions so we must convert it
            if TotalAssets[-1] == 'T':
                TotalAssets = float(TotalAssets[0:-1]) * 1000000000000
            elif TotalAssets[-1] == 'B':
                TotalAssets = float(TotalAssets[0:-1]) * 1000000000
            elif TotalAssets[-1] == 'M':
                TotalAssets = float(TotalAssets[0:-1]) * 1000000
            elif TotalAssets[-1] == 'K':
                TotalAssets = float(TotalAssets[0:-1]) * 1000
            elif TotalAssets == '-':
                TotalAssets = -1
            else:
                TotalAssets = float(TotalAssets)    
        else:
            TotalAssets = -1

            # We check if the Total Current Assets exists in the income statement, and then we isolate it and convert the number from millions or billions
        TotalCurrentAssets = 0
        if len(Assets.loc[Assets[0] == 'Total Current Assets Total Current Assets']) == 1:
            TotalCurrentAssets = Assets.loc[Assets[0] == 'Total Current Assets Total Current Assets'][
                len(Assets.columns) - 2]
            TotalCurrentAssets = TotalCurrentAssets[int(
                TotalCurrentAssets.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if TotalCurrentAssets[0] == '(':
                TotalCurrentAssets = '-' + TotalCurrentAssets[1:-1]
            if TotalCurrentAssets[-1] == 'T':
                TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000000000000
            elif TotalCurrentAssets[-1] == 'B':
                TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000000000
            elif TotalCurrentAssets[-1] == 'M':
                TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000000
            elif TotalCurrentAssets[-1] == 'K':
                TotalCurrentAssets = float(TotalCurrentAssets[0:-1]) * 1000
            elif TotalCurrentAssets == '-':
                TotalCurrentAssets = -1
            else:
                TotalCurrentAssets = float(TotalCurrentAssets)    
        else:
            TotalCurrentAssets = -1

        ###################################################################################################################################

        Liabilities.columns = pd.RangeIndex(0, len(
            Liabilities.columns))  # Indexing the columns as numbers so that the differences in the name of columns wont matter

        # We check if the Total Current Liabilities exists in the income statement, and then we isolate it and convert the number from millions or billions
        TotalCurrentLiabilities = 0
        if len(Liabilities.loc[Liabilities[0] == 'Total Current Liabilities Total Current Liabilities']) == 1:
            TotalCurrentLiabilities = \
                Liabilities.loc[Liabilities[0] == 'Total Current Liabilities Total Current Liabilities'][
                    len(Liabilities.columns) - 2]
            TotalCurrentLiabilities = TotalCurrentLiabilities[int(
                TotalCurrentLiabilities.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if TotalCurrentLiabilities[0] == '(':
                TotalCurrentLiabilities = '-' + TotalCurrentLiabilities[1:-1]
            if TotalCurrentLiabilities[-1] == 'T':
                TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000000000000
            elif TotalCurrentLiabilities[-1] == 'B':
                TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000000000
            elif TotalCurrentLiabilities[-1] == 'M':
                TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000000
            elif TotalCurrentLiabilities[-1] == 'K':
                TotalCurrentLiabilities = float(TotalCurrentLiabilities[0:-1]) * 1000
            elif TotalCurrentLiabilities == '-':
                TotalCurrentLiabilities = -1
            else:
                TotalCurrentLiabilities = float(TotalCurrentLiabilities)    
        else:
            TotalCurrentLiabilities = -1

        # We check if the Total Liabilities exists in the income statement, and then we isolate it and convert the number from millions or billions
        TotalLiabilities = 0
        if len(Liabilities.loc[Liabilities[0] == 'Total Liabilities Total Liabilities']) == 1:
            TotalLiabilities = Liabilities.loc[Liabilities[0] == 'Total Liabilities Total Liabilities'][
                len(Liabilities.columns) - 2]
            TotalLiabilities = TotalLiabilities[int(
                TotalLiabilities.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            # Some companies have liabilities in the trillions so we must convert it
            if TotalLiabilities[0] == '(':
                TotalLiabilities = '-' + TotalLiabilities[1:-1]
            if TotalLiabilities[-1] == 'T':
                TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000000000000
            elif TotalLiabilities[-1] == 'B':
                TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000000000
            elif TotalLiabilities[-1] == 'M':
                TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000000
            elif TotalLiabilities[-1] == 'K':
                TotalLiabilities = float(TotalLiabilities[0:-1]) * 1000
            elif TotalLiabilities == '-':
                TotalLiabilities = -1
            else:
                TotalLiabilities = float(TotalLiabilities)    
        else:
            TotalLiabilities = -1

        # First we retrieve the liabilities to assets ratio of the past 5 years
        RatioLA = []
        if len(Liabilities.loc[Liabilities[0] == 'Total Liabilities / Total Assets Total Liabilities / Total Assets']) == 1:
            for i in range(1, len(Liabilities.columns) - 1):
                LA = Liabilities.loc[Liabilities[0] == 'Total Liabilities / Total Assets Total Liabilities / Total Assets'][
                    i]
                if LA[int(LA.index.values)] != '-':        
                    RatioLA += [float((LA[int(LA.index.values)].replace(',', ''))[0:-1])]                        
        # Now we calculate the growth of this ratio year over year
        GrowthLA = 0
        if len(RatioLA) != 0:
            GrowthLA += (RatioLA[-1] * 100 / RatioLA[0]) - 100
            GrowthLA = GrowthLA ** (1 / len(RatioLA))
            if str(GrowthLA)[0] == '(':
                GrowthLA = float(str(GrowthLA)[1:5])
            else:
                GrowthLA = float(str(GrowthLA)[:4])
        else:
            GrowthLA = -1

            # First we retrieve the Debt to assets ratio of the past 5 years
        RatioDA = []
        if len(Liabilities.loc[Liabilities[0] == 'Total Debt / Total Assets Total Debt / Total Assets']) == 1:
            for i in range(1, len(Liabilities.columns) - 1):
                DA = Liabilities.loc[Liabilities[0] == 'Total Debt / Total Assets Total Debt / Total Assets'][i]
                if DA[int(DA.index.values)] != '-'  and DA[int(DA.index.values)][0] != '0':
                    RatioDA += [float((DA[int(DA.index.values)].replace(',', ''))[0:-1])]
        # Now we calculate the growth of this ratio year over year
        GrowthDA = 0
        if len(RatioDA) != 0:
            GrowthDA += (RatioDA[-1] * 100 / RatioDA[0]) - 100
            GrowthDA = GrowthDA ** (1 / len(RatioDA))
            if str(GrowthDA)[0] == '(':
                GrowthDA = float(str(GrowthDA)[1:5])
            else:
                GrowthDA = float(str(GrowthDA)[:4])
        else:
            GrowthDA = -1

            # We check if the Total Equity exists in the income statement, and then we isolate it and convert the number from millions or billions
        TotalEquity = 0
        if len(Liabilities.loc[Liabilities[0] == 'Total Equity Total Equity']) == 1:
            TotalEquity = Liabilities.loc[Liabilities[0] == 'Total Equity Total Equity'][len(Liabilities.columns) - 2]
            TotalEquity = TotalEquity[int(
                TotalEquity.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if TotalEquity[0] == '(':
                TotalEquity = '-' + TotalEquity[1:-1]
            if TotalEquity[-1] == 'T':
                TotalEquity = float(TotalEquity[0:-1]) * 1000000000000
            elif TotalEquity[-1] == 'B':
                TotalEquity = float(TotalEquity[0:-1]) * 1000000000
            elif TotalEquity[-1] == 'M':
                TotalEquity = float(TotalEquity[0:-1]) * 1000000
            elif TotalEquity[-1] == 'K':
                TotalEquity = float(TotalEquity[0:-1]) * 1000
            elif TotalEquity == '-':
                TotalEquity = -1
            else:
                TotalEquity = float(TotalEquity)    
        else:
            TotalEquity = -1

        # We check if Short Term Debt exists in the income statement, and then we isolate it and convert the number from millions or billions
        ShortTermDebt = 0
        if len(Liabilities.loc[Liabilities[0] == 'Short Term Debt Short Term Debt']) == 1:
            ShortTermDebt = Liabilities.loc[Liabilities[0] == 'Short Term Debt Short Term Debt'][
                len(Liabilities.columns) - 2]
            ShortTermDebt = ShortTermDebt[int(
                ShortTermDebt.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if ShortTermDebt[0] == '(':
                ShortTermDebt = '-' +  ShortTermDebt[1:-1]
            if ShortTermDebt[-1] == 'T':
                ShortTermDebt = float(ShortTermDebt[0:-1]) * 1000000000000     
            elif ShortTermDebt[-1] == 'B':
                ShortTermDebt = float(ShortTermDebt[0:-1]) * 1000000000
            elif ShortTermDebt[-1] == 'M':
                ShortTermDebt = float(ShortTermDebt[0:-1]) * 1000000
            elif ShortTermDebt[-1] == 'K':
                ShortTermDebt = float(ShortTermDebt[0:-1]) * 1000
            elif ShortTermDebt == '-':
                ShortTermDebt = -1
            else:
                ShortTermDebt = float(ShortTermDebt)    
        else:
            ShortTermDebt = -1

            # We check if the Long Term Debt exists in the income statement, and then we isolate it and convert the number from millions or billions
        LongTermDebt = 0
        if len(Liabilities.loc[Liabilities[0] == 'Long-Term Debt Long-Term Debt']) == 1:
            LongTermDebt = Liabilities.loc[Liabilities[0] == 'Long-Term Debt Long-Term Debt'][len(Liabilities.columns) - 2]
            LongTermDebt = LongTermDebt[int(
                LongTermDebt.index.values)]  # We dont know what position it is in so we find out and take only that specific value
            if LongTermDebt[0] == '(':
                LongTermDebt = '-' +  LongTermDebt[1:-1]
            if LongTermDebt[-1] == 'T':
                LongTermDebt = float(LongTermDebt[0:-1]) * 1000000000000         
            elif LongTermDebt[-1] == 'B':
                LongTermDebt = float(LongTermDebt[0:-1]) * 1000000000
            elif LongTermDebt[-1] == 'M':
                LongTermDebt = float(LongTermDebt[0:-1]) * 1000000
            elif LongTermDebt[-1] == 'K':
                LongTermDebt = float(LongTermDebt[0:-1]) * 1000
            elif LongTermDebt == '-':
                LongTermDebt = -1
            else:
                LongTermDebt = float(LongTermDebt)
        else:
            LongTermDebt = -1

            # We calculate the long term assets and liabilities with the difference of other two metrics but first we must make sure that these exist
        LongTermAssets = 0
        if TotalAssets != 0:
            LongTermAssets = TotalAssets - TotalCurrentAssets

        LongTermLiabilities = 0
        if TotalLiabilities != 0:
            LongTermLiabilities = TotalLiabilities - TotalCurrentLiabilities

    return TotalEquity, GrowthLA, GrowthDA, TotalLiabilities, TotalCurrentLiabilities, LongTermLiabilities, TotalAssets, TotalCurrentAssets, LongTermAssets, ShortTermDebt, LongTermDebt


def CashFlow(soup, FreeCashFlow = -1, TotalDebtReduction = -1, NetOperatingCashFlow = -1) -> float:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    # Cash flow is broken up into these three categories
    check = True
    try:
        CashFlow = pd.read_html(str(soup), attrs={'class': 'table table--overflow align--right'})
        OperatingActivities = CashFlow[0]
        InvestingActivities = CashFlow[1]
        FinancingActivities = CashFlow[2]
    except:
        check = False

    if check:    
        OperatingActivities.columns = pd.RangeIndex(0, len(
            OperatingActivities.columns))  # Indexing the columns as numbers so that the differences in the name of columns wont matter

        # We check if the Net Operating Cash Flow exists in the income statement, and then we isolate it and convert the number from millions or billions
        NetOperatingCashFlow = 0
        if len(OperatingActivities.loc[OperatingActivities[0] == 'Net Operating Cash Flow Net Operating Cash Flow']) == 1:
            NetOperatingCashFlow = \
                OperatingActivities.loc[OperatingActivities[0] == 'Net Operating Cash Flow Net Operating Cash Flow'][
                    len(OperatingActivities.columns) - 2]
            NetOperatingCashFlow = NetOperatingCashFlow[int(NetOperatingCashFlow.index.values)]
            # Since negative values come with parentesis , we check for those and then remove them
            if NetOperatingCashFlow[0] == '(':
                NetOperatingCashFlow = '-' + NetOperatingCashFlow[1:-1]  # We dont know what position it is in so we find out and take only that specific value
            if NetOperatingCashFlow[-1] == 'T':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000000000000 
            elif NetOperatingCashFlow[-1] == 'B':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000000000
            elif NetOperatingCashFlow[-1] == 'M':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000000
            elif NetOperatingCashFlow[-1] == 'K':
                NetOperatingCashFlow = float(NetOperatingCashFlow[0:-1]) * 1000
            elif NetOperatingCashFlow == '-':
                NetOperatingCashFlow = -1
            else:
                NetOperatingCashFlow = float(NetOperatingCashFlow)    
        else:
            NetOperatingCashFlow = -1

        InvestingActivities.columns = pd.RangeIndex(0, len(
            InvestingActivities.columns))  # Indexing the columns as numbers so that the differences in the name of columns wont matter

        FinancingActivities.columns = pd.RangeIndex(0, len(
            FinancingActivities.columns))  # Indexing the columns as numbers so that the differences in the name of columns wont matter

        # We check if the Debt reduction exists in the income statement, and then we isolate it and convert the number from millions or billions
        DebtReduction = 0
        TotalDebtReduction = 0
        if len(FinancingActivities.loc[
                   FinancingActivities[0] == 'Issuance/Reduction of Debt, Net Issuance/Reduction of Debt, Net']) == 1:
            # We want to see how much debt was reduced total in the past five years so we add each one
            for i in range(1, len(FinancingActivities.columns) - 1):
                DebtReduction = FinancingActivities.loc[
                    FinancingActivities[0] == 'Issuance/Reduction of Debt, Net Issuance/Reduction of Debt, Net'][i]
                DebtReduction = DebtReduction[int(DebtReduction.index.values)]
                # Since negative values come with parentesis , we check for those and then remove them
                if DebtReduction[0] == '(':
                    DebtReduction = '-' + DebtReduction[1:-1]  # We dont know what position it is in so we find out and take only that specific value
                if DebtReduction[-1] == 'T':
                    DebtReduction = float(DebtReduction[0:-1]) * 1000000000000 
                elif DebtReduction[-1] == 'B':
                    DebtReduction = float(DebtReduction[0:-1]) * 1000000000
                elif DebtReduction[-1] == 'M':
                    DebtReduction = float(DebtReduction[0:-1]) * 1000000
                elif DebtReduction[-1] == 'K':
                    DebtReduction = float(DebtReduction[0:-1]) * 1000
                elif DebtReduction == '-':
                    DebtReduction = 0
                else: 
                    DebtReduction = float(DebtReduction)    
                TotalDebtReduction += DebtReduction
        else:
            TotalDebtReduction = -1

        # We check if the Free Cash Flow exists in the income statement, and then we isolate it and convert the number from millions or billions
        FreeCashFlow = 0
        if len(FinancingActivities.loc[FinancingActivities[0] == 'Free Cash Flow Free Cash Flow']) == 1:
            FreeCashFlow = FinancingActivities.loc[FinancingActivities[0] == 'Free Cash Flow Free Cash Flow'][
                len(FinancingActivities.columns) - 2]
            FreeCashFlow = FreeCashFlow[int(FreeCashFlow.index.values)]
            # Since negative values come with parentesis , we check for those and then remove them
            if FreeCashFlow[0] == '(':
                FreeCashFlow = '-' + FreeCashFlow[1:-1]  # We dont know what position it is in so we find out and take only that specific value
            if FreeCashFlow[-1] == 'T':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000000000000 
            elif FreeCashFlow[-1] == 'B':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000000000
            elif FreeCashFlow[-1] == 'M':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000000
            elif FreeCashFlow[-1] == 'K':
                FreeCashFlow = float(FreeCashFlow[0:-1]) * 1000
            elif FreeCashFlow == '-':
                FreeCashFlow = -1
            else:
                FreeCashFlow = float(FreeCashFlow)    
        else:
            FreeCashFlow = -1

    return FreeCashFlow, TotalDebtReduction, NetOperatingCashFlow


def EPSRevisions(soup, estimateRevision1 = -1, estimateRevision2 = -1) -> float:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    # estimates is broken down in four different parts and we want the last two
    check = True
    try:
        # EPS estimate for next year revisions from 3 months ago 1 month ago and current
        firstYear = pd.read_html(str(soup), attrs={'class': 'table value-pairs no-heading font--lato'})[2]  
        # EPS estimate for the year after next year revisions from 3 months ago 1 month ago and current
        secondYear = pd.read_html(str(soup), attrs={'class': 'table value-pairs no-heading font--lato'})[3]  
    except:
        check = False

    if check:        
        estimateRevision1 = 0
        for i in range(2, 0, -1):
            # We calculate the percentage change from one year to another and then average them out
            # but first we must check for Nan as we can not work with this
            try:
                len(firstYear[1][i])
                len(firstYear[1][i - 1])
                # Some values have a $ sign in the second position so we must supress it
                if firstYear[1][i][0] == '-' and firstYear[1][i - 1][0] == '-':
                    estimateRevision1 += (float(firstYear[1][i - 1][0] + firstYear[1][i - 1][2:]) * 100) / float(
                        firstYear[1][i][0] + firstYear[1][i][2:]) - 100
                elif firstYear[1][i][0] == '-' and firstYear[1][i - 1][0] != '-':
                    estimateRevision1 += (float(firstYear[1][i - 1][1:]) * 100) / float(
                        firstYear[1][i][0] + firstYear[1][i][2:]) - 100
                elif firstYear[1][i][0] != '-' and firstYear[1][i - 1][0] == '-':
                    estimateRevision1 += (float(firstYear[1][i - 1][0] + firstYear[1][i - 1][2:]) * 100) / float(
                        firstYear[1][i][1:]) - 100
                elif firstYear[1][i][0] != '-' and firstYear[1][i - 1][0] != '-':
                    estimateRevision1 += (float(firstYear[1][i - 1][1:]) * 100) / float(firstYear[1][i][1:]) - 100
            except:
                None

        estimateRevision2 = 0
        for i in range(2, 0, -1):
            # We calculate the percentage change from one year to another and then average them out
            # but first we must check for Nan as we can not work with this
            try:
                len(secondYear[1][i])
                len(secondYear[1][i - 1])
                # Some values have a $ sign in the second position so we must supress it
                if secondYear[1][i][0] == '-' and secondYear[1][i - 1][0] == '-':
                    estimateRevision2 += (float(secondYear[1][i - 1][0] + secondYear[1][i - 1][2:]) * 100) / float(
                        secondYear[1][i][0] + secondYear[1][i][2:]) - 100
                elif secondYear[1][i][0] == '-' and secondYear[1][i - 1][0] != '-':
                    estimateRevision2 += (float(secondYear[1][i - 1][1:]) * 100) / float(
                        secondYear[1][i][0] + secondYear[1][i][2:]) - 100
                elif secondYear[1][i][0] != '-' and secondYear[1][i - 1][0] == '-':
                    estimateRevision2 += (float(secondYear[1][i - 1][0] + secondYear[1][i - 1][2:]) * 100) / float(
                        secondYear[1][i][1:]) - 100
                elif secondYear[1][i][0] != '-' and secondYear[1][i - 1][0] != '-':
                    estimateRevision2 += (float(secondYear[1][i - 1][1:]) * 100) / float(secondYear[1][i][1:]) - 100
            except:
                None

    return estimateRevision1, estimateRevision2


def PriceTargets(soup, HighTarget = -1, LowTarget = -1, AverageTarget = -1, NumberOfRatings = -1) -> float:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    # estimates is broken down in four different parts and we want the second one
    check = True
    try:
        estimates = pd.read_html(str(soup), attrs={'class': 'table value-pairs no-heading font--lato'})
    except:
        check = False

    if check:       
        priceTargets = estimates[1]
        # Must make sure that they are not NaN
        if type(priceTargets[1][0]) == str:
            # We must check if it contains a , so that we can remove it
            HighTarget = float(priceTargets[1][0][1:].replace(',', ''))
        if type(priceTargets[1][2]) == str:
            # We must check if it contains a , so that we can remove it
            LowTarget = float(priceTargets[1][2][1:].replace(',', ''))
        if type(priceTargets[1][3]) == str:
            # We must check if it contains a , so that we can remove it
            AverageTarget = float(priceTargets[1][3][1:].replace(',', ''))

        Summary = estimates[0]
        NumberOfRatings = -1
        if type(Summary[1][2]) == str:
            NumberOfRatings = int(Summary[1][2])

    return HighTarget, LowTarget, AverageTarget, NumberOfRatings


def EPSEstimates(soup) -> None:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    check = True
    try:
        EPSestimates = pd.read_html(str(soup), attrs={'class': 'table table--primary'})[0]
    except:
        check = False
    # We save the chart to be able to graph the estimates later
    if check:
        return EPSestimates
    else:
        return -1    

def RevenuesEstimates(soup, RevenueGrowthNextY = -1) -> float:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    check = True
    try:
        RevenueEstimates = pd.read_html(str(soup), attrs={'class': 'W(100%) M(0) BdB Bdc($seperatorColor) Mb(25px)'})[1]
    except:
        check = False
    
    if check:    
        RevenueEstimates.columns = pd.RangeIndex(0, len(RevenueEstimates.columns))
        if type(RevenueEstimates[4][5]) == str:
            RevenueGrowthNextY = float((RevenueEstimates[4][5].replace(',', ''))[0:-1])
        else:
            RevenueGrowthNextY = -1

    return RevenueGrowthNextY


def Recomendations(soup, columnNames = '', xValues = '', Buy = [], Overweight = [], Hold = [], Underweight = [], Sell = []) -> int and bool:
    # We inspect the webpage to finde the html tags of the objects that we want
    # Transform the html to a pandas dataframe
    check = True
    try:
        recom = pd.read_html(str(soup), attrs={'class': 'table table-primary align--left border--dotted'})[0]
        recom = recom.dropna(axis=1, how='any')  # We take away any columns that have at least one Nan
    except:
        check = False

    if check:    
        # We retrieve the name of the columns to later use them in the bar chart
        columnNames = list(recom.columns[1:])
        # Change the column index to numbers som that we can acces it
        recom.columns = pd.RangeIndex(0, len(recom.columns))

        # retrieve the values for the rows
        xValues = []
        for i in range(len(recom) - 1):
            xValues += [recom[0][i]]

            # We retrieve the values for each recomendation by accesing each row
        # We dont know how many columns we will have because of the DropNa
        Buy = []
        for i in range(1, len(recom.loc[recom[0] == 'Buy'].columns)):
            Buy += [int(recom.loc[recom[0] == 'Buy'][i][recom.loc[recom[0] == 'Buy'].index.values])]
        Overweight = []
        for i in range(1, len(recom.loc[recom[0] == 'Overweight'].columns)):
            Overweight += [int(recom.loc[recom[0] == 'Overweight'][i][recom.loc[recom[0] == 'Overweight'].index.values])]
        Hold = []
        for i in range(1, len(recom.loc[recom[0] == 'Hold'].columns)):
            Hold += [int(recom.loc[recom[0] == 'Hold'][i][recom.loc[recom[0] == 'Hold'].index.values])]
        Underweight = []
        for i in range(1, len(recom.loc[recom[0] == 'Underweight'].columns)):
            Underweight += [int(recom.loc[recom[0] == 'Underweight'][i][recom.loc[recom[0] == 'Underweight'].index.values])]
        Sell = []
        for i in range(1, len(recom.loc[recom[0] == 'Sell'].columns)):
            Sell += [int(recom.loc[recom[0] == 'Sell'][i][recom.loc[recom[0] == 'Sell'].index.values])]

    return columnNames, xValues, Buy, Overweight, Hold, Underweight, Sell

