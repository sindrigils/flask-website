from matplotlib.dates import DateFormatter
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv
from website import app
import matplotlib.pyplot as plt
from datetime import datetime
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


def plot_a_graph(symbol):
    interval = "60min"
    # Retrieve the stock prices data from Alpha Vantage
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval)

    dates = data.index.tolist()
    prices = data['4. close'].tolist()

    # Convert the date strings to datetime objects
    dates = [datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') for date in dates]

    # Plot the stock prices data using Matplotlib
    fig, ax = plt.subplots()
    ax.plot(dates, prices)
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title(f'Stock Prices for {symbol}')

    # Format the timestamps on the x-axis
    date_fmt = DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(date_fmt)
    fig.autofmt_xdate()

    # Save the graph as a PNG file
    filename = f'{symbol}_graph.png'
    filepath = os.path.join(app.root_path, 'static', 'graphs', filename)
    plt.savefig(filepath)

    plt.close()

    return filename

