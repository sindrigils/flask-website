import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv
from typing import List, Union, Tuple
import requests

load_dotenv()
api_key = key=os.getenv("API_KEY")

ts = TimeSeries(key=api_key, output_format="pandas")


def convert_timestamps_to_datetime(time_list: List):
    """ helper function for converting timestamps into datetime """
    
    formatted_datetimes = [timestamp.to_pydatetime().strftime('%a, %d %b %Y %H:%M') for timestamp in time_list]

    return formatted_datetimes


def get_stock_prices_and_dates_by_ticker(stock_ticker: str) -> Union[str, Tuple[List[float], List[str]]]:
    """
    Parameters:
        stock_ticker (str): The ticker symbol for the desired stock.

    Returns:
        Union[str, float]: If the ticker symbol is valid, returns the current price of the stock as a float. If the ticker
        symbol is invalid, returns a string error message.
    """    

    try:
        data, _ = ts.get_intraday(symbol=stock_ticker.upper(), interval="60min")
        return data["4. close"].tolist(), convert_timestamps_to_datetime(data.index.tolist()[::-1])
    except Exception:
        return "None", "None"
    

def get_latest_stock_price(stock_ticker):
    try:
        data, _ = ts.get_daily_adjusted(symbol=stock_ticker)
        return data["4. close"][0]
    except Exception:
        return None
    

def get_company_name(stock_ticker):
    ticker_data = ts.get_symbol_search(keywords=stock_ticker)

    try:
        return ticker_data[0]["2. name"][0]
    except Exception:
        return None


def get_balance_sheet(stock_ticker):
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={stock_ticker}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        balance_sheet = response.json()
        return balance_sheet
    return "Balance sheet failed"

# print(get_balance_sheet("tsla")["annualReports"][0]["currentDebt"])

# currentDebt
# totalAssets

def get_cashflow(stock_ticker):
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock_ticker}&apikey={api_key}"
