import argparse
from termcolor import colored
import tdaClientInterpreter as tda
from datetime import datetime, timedelta
import traceback
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import logging
import os
from Environment import *
from AlgorithmInterface import *

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('Backtester.py')
logger.setLevel(level=logging.DEBUG)


class Backtester:
    def __init__(self, settings: Environment, u: bool):
        self.Settings = settings
        self.Tickers = self.Settings.Tickers
        if u: self.ExportData()

        self.Market = pd.read_csv("Resources/Data/SPY_data.csv", index_col=0,
                                  parse_dates=['datetime'])

        # ---------- Start of Spaghetti ---------- #
        # Reads CSV files and converts them into multi-indexed dataframe
        logger.debug("Loading data from CSV files...")
        self.__tickerData = {}
        self.Data = None
        for ticker in tqdm(self.Tickers):
            try:
                self.__tickerData[ticker] = pd.read_csv(f"Resources/Data/{ticker}_data.csv", index_col=0,
                                                        parse_dates=['datetime'])
            except FileNotFoundError:
                logger.warning(colored(f"{ticker} not found in Resources/Data! "
                                       f"Try rerunning with update parameter enabled (-u)", "red"))
                self.Tickers.remove(ticker)

        self.PreProcess()
        # ---------- End of Spaghetti ---------- #

    def PreProcess(self):
        self.Market['pChange'] = self.Market['close'] / self.Market['close'].shift(1)

        for ticker, data in self.__tickerData.items():
            data['pChange_ratio'] = data['close'] / data['close'].shift(1)
            data['pChange'] = 1 - data['pChange_ratio']

            data.dropna(inplace=True)

        self.Data = pd.concat(self.__tickerData.values(), keys=self.__tickerData.keys())

    def RunBacktest(self, algo):
        logger.debug("Running backtest...")

        idxCount = 0
        for idx, row in tqdm(self.Market.iterrows(), total=len(self.Market.index)):
            if idxCount < self.Settings.WarmUpPeriod:
                idxCount += 1
                continue

            algo.Slice = self.Data.loc(axis=0)[:, :idx]
            algo.Portfolio.Slice = algo.Slice

            if algo.Slice.empty:
                idxCount += 1
                continue

            algo.now = idx
            algo.Portfolio.now = idx

            algo.UpdateOrders()
            algo.OnData()
            algo.UpdateOrders()
            algo.Portfolio.UpdateValue()

    def ExportData(self):
        if not os.path.exists('Resources/Data'):
            logger.debug("Resources/Data directory not found, creating...")
            os.mkdir('Resources/Data')

        logger.debug(f"Updating CSV files...")
        for ticker in tqdm(self.Settings.Tickers):
            try:
                if self.Settings.Frequency == Frequency.Minute:
                    price_history = tda.get_price_history_minute(ticker, self.Settings.StartDate,
                                                                 self.Settings.EndDate)
                elif self.Settings.Frequency == Frequency.Five_Minute:
                    price_history = tda.get_price_history_five_minute(ticker, self.Settings.StartDate,
                                                                      self.Settings.EndDate)
                elif self.Settings.Frequency == Frequency.Fifteen_Minute:
                    price_history = tda.get_price_history_fifteen_minute(ticker, self.Settings.StartDate,
                                                                         self.Settings.EndDate)
                elif self.Settings.Frequency == Frequency.Thirty_Minute:
                    price_history = tda.get_price_history_thirty_minute(ticker, self.Settings.StartDate,
                                                                        self.Settings.EndDate)
                elif self.Settings.Frequency == Frequency.Day:
                    price_history = tda.get_price_history_day(ticker, self.Settings.StartDate,
                                                              self.Settings.EndDate)
                else:
                    price_history = tda.get_price_history_week(ticker, self.Settings.StartDate,
                                                               self.Settings.EndDate)

                # Timezone adjustment - needs fixing
                price_history['datetime'] = price_history['datetime'] - (4 * 60 * 60 * 1000)
                price_history['datetime'] = pd.to_datetime(price_history['datetime'], unit='ms')
                price_history.set_index('datetime', inplace=True)

                price_history.to_csv(f"Resources/Data/{ticker}_data.csv")

            except KeyError:
                logger.warning(f"{ticker} KeyError")


def InitializeBacktest(algo: Algorithm, update: bool):
    algo.AddEquity('SPY')
    backtest = Backtester(algo.Settings, update)

    try:
        backtest.RunBacktest(algo)
    except KeyboardInterrupt:
        algo.OnFinish(backtest.Market)
    else:
        algo.OnFinish(backtest.Market)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--Update", action='store_true', help="Update CSV Files")
    args = parser.parse_args()

    algo = Algorithm()
    algo.AddEquity("SPY")
    algo.SetFrequency(Frequency.Week)
    backtest = Backtester(algo.Settings, args.Update)

    try:
        backtest.RunBacktest(algo)
    except KeyboardInterrupt:
        algo.OnFinish(backtest.Market)
    else:
        algo.OnFinish(backtest.Market)
