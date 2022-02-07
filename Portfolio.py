import pandas as pd
from Environment import *


class Portfolio:
    def __init__(self):
        self.Value = 100_000
        self.Cash = 100_000
        self.Holdings = pd.DataFrame(columns=['Quantity', 'AvgPrice', 'RecentPrice'])
        self.TrackValue = {}
        self.InTrade = False

        self.Slice = None
        self.now = None

    def UpdateValue(self):
        HoldingTickers = self.Holdings[self.Holdings['Quantity'] != 0]

        for ticker in HoldingTickers.index:
            last_close = self.Slice.loc[ticker, 'close'].iloc[-1]
            self.Holdings.loc[ticker, 'RecentPrice'] = last_close

        values_series = self.Holdings['Quantity'] * (self.Holdings['RecentPrice'] - self.Holdings['AvgPrice'])
        total_values = values_series.sum()
        self.Value = self.Cash + total_values

        self.TrackValue[self.now] = self.Value

        if total_values != 0: self.InTrade = True

    def PlotValue(self, Market=None):
        pass

    def FillOrder(self, order: Order):
        self.Cash -= (order.Quantity * order.Price)

        ticker_holding = self.Holdings.loc[order.Ticker]
        new_total_price = ticker_holding['Quantity'] * ticker_holding['AvgPrice'] + order.Quantity * order.Price
        new_total_quantity = ticker_holding['Quantity'] + order.Quantity

        if new_total_quantity == 0: self.Holdings.loc[order.Ticker] = [0, 0, 0]

        else:
            new_average_price = new_total_price / new_total_quantity
            self.Holdings.loc[order.Ticker] = [new_total_quantity, new_average_price, 0]

    def AddEquities(self, tickers):
        zeros = [0] * len(tickers)
        temp_Holdings = pd.DataFrame(data=zip(zeros, zeros, zeros), index=tickers,
                                     columns=['Quantity', 'AvgPrice', 'RecentPrice'])

        self.Holdings = pd.concat(self.Holdings, temp_Holdings)

    def AddEquity(self, ticker):
        self.Holdings.loc[ticker] = [0, 0, 0]

