import pandas as pd

def main ():

	Nasdaq = pd.read_csv('AMEX.csv')
	Nasdaq = pd.DataFrame(Nasdaq)
	Nasdaq.columns = pd.RangeIndex(0, len(Nasdaq.columns))
	listNasdaq = list(Nasdaq[0])
	print(len(listNasdaq))
	
if __name__ == '__main__': main()