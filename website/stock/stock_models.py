import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import os
from dotenv import load_dotenv
from website import app
import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

load_dotenv()
api_key = key=os.getenv("API_KEY")

ts = TimeSeries(key=api_key, output_format="pandas")


def get_stock_price_by_ticker(stock_ticker: str):
    """ Gets a ticker symbol as a parameter and returns its stock price """

    try:
        data, _ = ts.get_daily_adjusted(symbol=stock_ticker, outputsize="compact")
    except ValueError:
        return "Ticker symbol does not exists!"
    
    return data["2. high"][0]



# def plot_a_graph(symbol):
#     interval = "60min"
#     url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'

#     # Make a request to the API and parse the response as JSON
#     response = requests.get(url)
#     data = json.loads(response.text)

#     # Extract the stock prices data from the JSON response
#     time_series = data['Time Series (60min)']
#     dates = []
#     prices = []

#     for date in time_series:
#         dates.append(date)
#         prices.append(float(time_series[date]['4. close']))

#     # Plot the stock prices data using Matplotlib
#     plt.plot(dates, prices)
#     plt.xlabel('Time')
#     plt.ylabel('Price')
#     plt.title(f'Stock Prices for {symbol}')

#     # Save the graph as a PNG file
#     filename = f'{symbol}_graph.png'
#     filepath = os.path.join(app.root_path, 'static', 'graphs', filename)
#     plt.savefig(filepath)

#     plt.close()

#     return filename

def plot_a_graph(symbol):
    
    data, meta_data = ts.get_intraday(symbol=symbol, interval="60min")

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
    date_fmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(date_fmt)
    fig.autofmt_xdate()

    # Save the graph as a PNG file
    filename = f'{symbol}_graph.png'
    filepath = os.path.join(app.root_path, 'static', 'graphs', filename)
    plt.savefig(filepath)

    plt.close()

    return filename





