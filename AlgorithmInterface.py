import pandas as pd
import matplotlib.pyplot as plt
import traceback
import math
import numpy as np
from Environment import *
from Portfolio import *
import logging, argparse


logger = logging.getLogger('Backtester.py')


class Algorithm:
    def __init__(self):

        self.Portfolio = Portfolio()
        self.Settings = Environment()
        self.Orders = {}
        self.Slice = None
        self.now = None

    def OnData(self):
        pass

    def OnFinish(self, market):
        pass

    # --- Environment Settings --- #
    def SetFrequency(self, freq: Frequency):
        self.Settings.Frequency = freq

    def AddEquities(self, tickers):
        try:
            self.Settings.Tickers.extend(tickers)
            self.Portfolio.AddEquities(tickers)
        except TypeError as e:
            logger.warning("Used single ticker in AddEquities - use AddEquity instead")
            raise e

    def AddEquity(self, ticker):
        if type(ticker) is list:
            logger.warning("Used list of tickers in AddEquity - use AddEquities instead")
            raise TypeError
        else:
            self.Settings.Tickers.append(ticker)
            self.Portfolio.AddEquity(ticker)

    def SetStartDate(self, date):
        if type(date) is str: date = pd.to_datetime(date, infer_datetime_format=True)
        self.Settings.StartDate = date

    def SetEndDate(self, date):
        if type(date) is str: date = pd.to_datetime(date, infer_datetime_format=True)
        self.Settings.EndDate = date

    def SetStartingCash(self, amount):
        self.Portfolio.Value = amount
        self.Portfolio.Cash = amount
        self.Portfolio.InitialCash = amount

    # --- Order Placement --- #

    def PlaceMarketOrder(self, ticker, quantity):
        price = self.Slice.loc[ticker, 'close'].iloc[-1]
        if price * quantity > self.Portfolio.Cash: return False

        order = Order(ticker, quantity, self.Slice.loc[ticker, 'close'].iloc[-1])
        self.Portfolio.FillOrder(order)

    def PlaceLimitOrder(self, ticker, quantity, price):
        if price * quantity > self.Portfolio.Cash: return False

        order = Order(ticker, quantity, price)

        orderno = len(self.Orders)
        self.Orders[orderno] = order

        return orderno

    def UpdateOrders(self):
        delete_keys = []

        for key, order in self.Orders.items():
            ticker_data = self.Slice.loc[order.Ticker].iloc[-1]

            if order.Quantity > 0 and order.Price > ticker_data.low:
                self.Portfolio.FillOrder(order)
                delete_keys.append(key)

            if order.Quantity < 0 and order.Price < ticker_data.high:
                self.Portfolio.FillOrder(order)
                delete_keys.append(key)

        for key in delete_keys: del self.Orders[key]



