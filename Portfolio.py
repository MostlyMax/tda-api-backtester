import pandas as pd


class Portfolio:
    def __init__(self):
        self.Value = 100_000
        self.Cash = 100_000
        self.Holdings = pd.DataFrame(columns=['Quantity', 'AvgPrice', 'Value'])
        self.TrackValue = {}

        self.Slice = None
        self.now = None

    def UpdateValue(self):
        self.Holdings['Value'] = self.Holdings['Quantity'] * self.Holdings['AvgPrice']

        Portfolio_Value = self.Holdings['Value'].sum()
        self.Value = self.Cash + Portfolio_Value

    def AddEquities(self, tickers):
        zeros = [0] * len(tickers)
        temp_Holdings = pd.DataFrame(data=zip(zeros, zeros, zeros), index=tickers, columns=['Quantity', 'AvgPrice'])

        self.Holdings = pd.concat(self.Holdings, temp_Holdings)

    def AddEquity(self, ticker):
        self.Holdings.loc[ticker] = [0, 0, 0]

