import pandas as pd
from Environment import *


class Portfolio:
    def __init__(self):
        self.Value = 100_000
        self.Cash = 100_000
        self.Holdings = pd.DataFrame(columns=['Quantity', 'AvgPrice', 'Cost', 'RecentPrice'])
        self.TrackValue = {}
        self.InTrade = False

        self.Slice = None
        self.now = None

    # TODO Broken Class!!
    def UpdateValue(self):
        self.Holdings['Cost'] = self.Holdings['Quantity'] * self.Holdings['AvgPrice']

        Portfolio_Cost = self.Holdings['Cost'].sum()
        self.Value = self.Cash + Portfolio_Cost

        self.TrackValue[self.now] = self.Value

        if Portfolio_Cost != 0: self.InTrade = True

    def PlotValue(self, Market=None):
        pass

    def FillOrder(self, order: Order):
        self.Cash += (order.Quantity * order.Price)

        ticker_holding = self.Holdings.loc[order.Ticker]
        new_total_price = ticker_holding['Quantity'] * ticker_holding['AvgPrice'] + order.Quantity * order.Price
        new_total_quantity = ticker_holding['Quantity'] + order.Quantity

        if new_total_quantity == 0: self.Holdings.loc[order.Ticker] = [0, 0, 0]

        else:
            new_average_price = new_total_price / new_total_quantity
            self.Holdings.loc[order.Ticker] = [new_total_quantity, new_average_price, 0]

    def AddEquities(self, tickers):
        zeros = [0] * len(tickers)
        temp_Holdings = pd.DataFrame(data=zip(zeros, zeros, zeros), index=tickers, columns=['Quantity', 'AvgPrice'])

        self.Holdings = pd.concat(self.Holdings, temp_Holdings)

    def AddEquity(self, ticker):
        self.Holdings.loc[ticker] = [0, 0, 0]

