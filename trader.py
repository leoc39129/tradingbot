import robin_stocks.robinhood as r
import pandas as pd
import time
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from .backtest import *

def main():
    portfolio = init()
    #print(list(portfolio.keys()))
    #tickers = r.markets.get_all_stocks_from_market_tag('technology', 'symbol')
    
    #print(len(tickers))
    #for t in range(len(tickers)):
        #print(str(t) + ": " + tickers[t])
    #visualize_price(tickers[161:], '5year', 'day')
    file_names = os.listdir("Excel Sheets")
    tickers = []
    # Print the names of the files
    for file_name in file_names:
        tickers.append(file_name.split(".")[0])
    backtest(tickers)
    #visualize_price(list(portfolio.keys()), '3month')

def execute_trade(symbol, trade_type, amount, price):
    pass
    # Call your broker's API to execute trade
    # broker_api_url = f"https://api.broker.com/trade"
    # trade_payload = {
    #     "symbol": symbol,
    #     "type": trade_type,
    #     "amount": amount
    # }
    # response = requests.post(broker_api_url, json=trade_payload)

    # if response.status_code == 200:
    #     # Log the trade to the PostgreSQL database
    #     cursor.execute(
    #         "INSERT INTO trades (symbol, trade_type, amount, price) VALUES (%s, %s, %s, %s)",
    #         (symbol, trade_type, amount, price)
    #     )
    #     conn.commit()
    #     print(f"Trade executed: {trade_type} {amount} of {symbol} at {price}")

def init():
    load_dotenv()
    username = os.getenv("ROBINHOOD_USERNAME")
    password = os.getenv("ROBINHOOD_PASSWORD")

    login = r.authentication.login(username, password)
    portfolio = r.build_holdings()
    #print(portfolio)
    #for key in portfolio:
    #    print(key + ": " + portfolio[key])
    return portfolio

if __name__ == '__main__':
    main()