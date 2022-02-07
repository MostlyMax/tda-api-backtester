from datetime import datetime, timedelta


class Frequency:
    Minute = 'MIN'
    Five_Minute = '5MIN'
    Fifteen_Minute = '15MIN'
    Thirty_Minute = '30MIN'
    Day = 'DAY'
    Week = 'WEEK'


class Order:
    def __init__(self, ticker, quantity, price):
        self.Ticker = ticker
        self.Quantity = quantity
        self.Price = price

    def EditOrder(self, quantity=None, price=None):
        if quantity is None: quantity = self.Quantity
        if price is None: price = self.Price

        self.Quantity = quantity
        self.Price = price


class Environment:
    def __init__(self):
        self.StartDate = datetime(month=3, day=2, year=2002)
        self.EndDate = datetime.now()

        self.Tickers = []
        self.Frequency = Frequency.Day

        self.WarmUpPeriod = 0
