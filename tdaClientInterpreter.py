import traceback
import httpx
import pytz
from tda.auth import easy_client
from tda.auth import client_from_login_flow
from tda.client import Client
from tda.streaming import StreamClient
from termcolor import colored
from Resources.config import client_id, redirect_url, my_account_id
from selenium import webdriver
from datetime import datetime
import pandas as pd
import asyncio
import json

tz_NY = pytz.timezone('America/New_York')
now = datetime.now(tz_NY)
minutes_passed = 0

try:  # Tries to initialize tda client
    client = easy_client(
        api_key=client_id,
        redirect_uri=redirect_url,
        token_path='Resources/token.txt',
        webdriver_func=webdriver.Chrome)

except Exception as exc:  # Gets new token if previous token is expired
    client = client_from_login_flow(webdriver.Chrome(), api_key=client_id,
                                    redirect_url=redirect_url,
                                    token_path='Resources/token.txt',
                                    redirect_wait_time_seconds=0.1,
                                    max_waits=3000,
                                    asyncio=False,
                                    token_write_func=None)
    traceback.print_exc(exc)

stream_client = StreamClient(client, account_id=int(my_account_id))


# Cancels an order given an order number
def cancel_order(order):
    r = client.cancel_order(order_id=order, account_id=int(my_account_id))
    assert r.status_code == httpx.codes.OK, r.raise_for_status()


def get_option_chain(symbol):
    r = client.get_option_chain(symbol=symbol)
    assert r.status_code == httpx.codes.OK, r.raise_for_status()

    return pd.DataFrame(r.json())


# Should get a list of orders but this is unused right now!
def get_orders():
    allOrders = client.get_account(account_id=my_account_id, fields=client.Account.Fields.ORDERS)
    # orders = pd.DataFrame(orders)
    return allOrders


def get_order(orderno):
    order = client.get_order(orderno, my_account_id)
    assert order.status_code == httpx.codes.OK, order.raise_for_status()
    return order.json()


def get_hours_for_market(market, date):
    market = client.Markets(market)
    data = client.get_hours_for_single_market(market, date)
    if data.status_code == 404: return None
    return data.json()


def place_order(order):
    r = client.place_order(account_id=int(my_account_id), order_spec=order)
    orderno = r.headers['Location'].split("/")[-1]

    if r.status_code == 200 or r.status_code == 201:
        return orderno
    else:
        r.raise_for_status()


def get_account(account_id, fields=None):
    return pd.DataFrame(client.get_account(account_id, fields=fields).json())


def get_accounts(fields=None):
    return pd.DataFrame(client.get_accounts(fields=fields).json())


# Just returns get quotes given a list of symbols
async def get_quote_data(quoteList):
    return pd.DataFrame(client.get_quotes(quoteList).json())


def get_quotes(quoteList):
    return pd.DataFrame(client.get_quotes(quoteList).json())


def get_quote(symbol):
    return pd.DataFrame(client.get_quote(symbol).json())


def get_price_history_minute(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_minute(symbol,
                                                              start_datetime=start_datetime,
                                                              end_datetime=end_datetime).json()['candles'])


def get_price_history_five_minute(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_five_minutes(symbol,
                                                                    start_datetime=start_datetime,
                                                                    end_datetime=end_datetime).json()['candles'])


def get_price_history_thirty_minute(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_thirty_minutes(symbol,
                                                                      start_datetime=start_datetime,
                                                                      end_datetime=end_datetime).json()['candles'])


def get_price_history_fifteen_minute(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_fifteen_minutes(symbol,
                                                                       start_datetime=start_datetime,
                                                                       end_datetime=end_datetime).json()['candles'])


def get_price_history_day(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_day(symbol,
                                                           start_datetime=start_datetime,
                                                           end_datetime=end_datetime).json()['candles'])


def get_price_history_week(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_week(symbol,
                                                            start_datetime=start_datetime,
                                                            end_datetime=end_datetime).json()['candles'])


async def async_get_price_history_day(symbol, start_datetime=None, end_datetime=None):
    return pd.DataFrame(client.get_price_history_every_day(symbol,
                                                           start_datetime=start_datetime,
                                                           end_datetime=end_datetime).json()['candles'])
