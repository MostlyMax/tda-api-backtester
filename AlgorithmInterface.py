import pandas as pd
import matplotlib.pyplot as plt
import traceback
import math
import numpy as np
from Environment import *
from Portfolio import *
import logging


logger = logging.getLogger('Backtester.py')


class Algorithm:
    def __init__(self):

        self.Portfolio = Portfolio()
        self.Settings = Environment()
        self.Slice = None
        self.now = None

    def OnData(self):
        pass

    def OnFinish(self, market):
        pass

    # Changing Environment Settings
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


