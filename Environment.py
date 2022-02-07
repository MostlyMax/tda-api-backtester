from datetime import datetime, timedelta


class Frequency:
    Minute = 'MIN'
    Five_Minute = '5MIN'
    Fifteen_Minute = '15MIN'
    Thirty_Minute = '30MIN'
    Day = 'DAY'
    Week = 'WEEK'


class Environment:
    def __init__(self):
        self.StartDate = datetime(month=3, day=2, year=2002)
        self.EndDate = datetime.now()

        self.Tickers = ['SPY']
        self.Frequency = Frequency.Day

        self.WarmUpPeriod = 0
