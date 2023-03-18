import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv
from website import app
import requests
import json
import matplotlib.pyplot as plt
from typing import Union

load_dotenv()
api_key = key=os.getenv("API_KEY")

ts = TimeSeries(key=api_key, output_format="pandas")


def get_stock_price_by_ticker(stock_ticker: str) -> Union[str, float]:
    """
    Parameters:
        stock_ticker (str): The ticker symbol for the desired stock.

    Returns:
        Union[str, float]: If the ticker symbol is valid, returns the current price of the stock as a float. If the ticker
        symbol is invalid, returns a string error message.
    """    

    try:
        data, _ = ts.get_daily_adjusted(symbol=stock_ticker, outputsize="compact")
    except ValueError:
        return "Ticker symbol does not exists!"
    
    return data["2. high"][0]



def plot_a_graph(symbol: str) -> str:
    """
        Retrieves stock prices data from AlphaVantage API for the specified stock symbol,
        plots a graph using Matplotlib, and saves it as a PNG file. Returns the filename of the saved graph.

        Parameters:
            symbol (str): The stock ticker symbol.

        Returns:
            filename (str): The filename of the saved graph.
    """

    interval = "60min"
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'

    # Make a request to the API and parse the response as JSON
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract the stock prices data from the JSON response
    time_series = data['Time Series (60min)']
    dates = []
    prices = []

    for date in time_series:
        dates.append(date)
        prices.append(float(time_series[date]['4. close']))

    # Plot the stock prices data using Matplotlib
    plt.plot(dates, prices)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(f'Stock Prices for {symbol}')

    # Save the graph as a PNG file
    filename = f'{symbol}_graph.png'
    filepath = os.path.join(app.root_path, 'static', 'graphs', filename)
    plt.savefig(filepath)

    plt.close()

    return filename