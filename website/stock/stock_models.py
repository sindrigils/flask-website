import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv

load_dotenv()
ts = TimeSeries(key=os.getenv("API_KEY"), output_format="pandas")



#models
def get_stock_price_by_ticker(stock_ticker: str):
    """ Gets a ticker symbol as a parameter and returns its stock price """

    try:
        data, _ = ts.get_daily_adjusted(symbol=stock_ticker, outputsize="compact")
    except ValueError:
        return "Ticker symbol does not exists!"
    
    return data["2. high"][0]


