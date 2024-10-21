import robin_stocks.robinhood as r
import pandas as pd
import time
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

'''
Notes:

***** TRADING STRATEGIES *******
Golden Cross: When a short term moving average crosses over a long term moving average. Typically when the 50 day moving average crosses to be above 
    the 200 day moving average. Typically buy when this happens, sell later at a profit.

https://learn.bybit.com/strategies/golden-cross-trading-strategies/

To test:
    HOLD: If 50 day MVA > 200 day MVA AND both slopes positive
    SELL: If 50 day MVA > 200 day MVA AND if 50 day MVA is falling at a greater rate than the 200 day MVA is gaining 
            [ abs(50 day MVA slope) > (200 day MVA slope) ]
    BUY: If 50 day MVA is within 15% of 200 day MVA, 50 day > 200 day, and both slopes are positive

    Improvements: Change % on buy? Look at a larger splice for slope?
'''

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

def buy_cond(fd, td, day):
    # fd is the last three days of 50 day moving averages
    # td is the last three days of 200 day moving averages
    return (fd[day] > td[day]) and (fd[day] - fd[day-2] > 0) and (td[day] - td[day-2] > 0) and (fd[day] - td[day] < .15*td[day])

def sell_cond(fd, td, day):
    fd_slope = (fd[day] - fd[day-2]) * .5
    td_slope = (td[day] - td[day-2]) * .5  
    return (fd[day] > td[day]) and (fd_slope < 0) and (td_slope > 0) and (abs(fd_slope) > td_slope)

def backtest(ticker_list):
    backtest_df = pd.DataFrame()

    cur_df = pd.read_excel("Excel Sheets/QCOM.xlsx")
    backtest_df["date"] = cur_df["begins_at"]

    pft_val = 0
    units_dict = {}
    price_dict = {}

    for t in ticker_list:
        cur_df = pd.read_excel("Excel Sheets/" + str(t) + ".xlsx")
        backtest_df[str(t) + "mvg_avg_50"] = cur_df["mvg_avg_50"]
        backtest_df[str(t) + "mvg_avg_200"] = cur_df["mvg_avg_200"]
        backtest_df[str(t) + "open_price"] = cur_df["open_price"]

        #pft_val += cur_df.loc[199]["open_price"]

        units_dict[t] = 0
        price_dict[t] = cur_df.loc[199]["open_price"]

    profit_daily = []
    pft_log = []
    value = []
    #print(pft_val)
    #print(units_dict)
    #print(price_dict)
    #backtest_df.to_excel("collective_info.xlsx")
    
    bankroll = 1000000
    bank = bankroll

    

    with open('log.txt', 'w') as f:
        for day in range(199, len(backtest_df)):
        #for day in range(199, 201):    
            # for logging purposes
            #print(day)
            pft_val = 0

            for t in ticker_list:
                
                # Update unit price
                price_dict[t] = backtest_df.loc[day][t + "open_price"]

                if bank > price_dict[t] and buy_cond(backtest_df.loc[day-2:day][t + "mvg_avg_50"], backtest_df.loc[day-2:day][t + "mvg_avg_200"], day):
                    # BUY #
                    units_dict[t] += 1
                    price_dict[t] = backtest_df.loc[day][t + "open_price"]

                    f.write(backtest_df.loc[day]["date"].strftime('%m/%d/%Y') + ": Bought one share of " + str(t) + "       Bank: " + str(bank) + "\n")

                    bank -= price_dict[t]

                elif units_dict[t] > 0 and sell_cond(backtest_df.loc[day-2:day][t + "mvg_avg_50"], backtest_df.loc[day-2:day][t + "mvg_avg_200"], day):
                    # SELL #
                    units_dict[t] -= 1
                    price_dict[t] = backtest_df.loc[day][t + "open_price"]

                    f.write(backtest_df.loc[day]["date"].strftime('%m/%d/%Y') + ": Sold one share of " + str(t) + "       Bank: " + str(bank) + "\n")

                    bank += price_dict[t]

                # ELSE HOLD

                pft_val += (units_dict[t] * price_dict[t])

            pft_log.append(pft_val)
            value.append(pft_val + bank)
            print(pft_val + bank)
            profits = pft_val + bank - bankroll
            profit_daily.append(profits)

    print("Portfolio Start Value: " + str(round(pft_log[0], 2)))
    print("Portfolio End Value: " + str(round(pft_log[-1], 2)))
    print("Profits: " + str(round(profit_daily[-1], 2)))
    print("Percent Change: " + str(round(((pft_log[-1] - bankroll) / bankroll)*100, 2)) + "%")
    #print("Bank: " + str(bank))

    final_df = pd.DataFrame()
    final_df["Value"] = value
    final_df["Day"] = [x for x in range(1000, len(backtest_df))]

    ax = final_df.plot(x = 'Day', y='Value', figsize=(14,7))
    #ax.plot(final_df["Day"], final_df["Value"])
    plt.show()


def visualize_price(ticker_list, span, interval):   
    # Span: [day, week, month, 3month, year, 5year]
    for t in range(len(ticker_list)):   #len(ticket_list)
        name = str(r.get_name_by_symbol(ticker_list[t]))
        hist = r.stocks.get_stock_historicals(ticker_list[t], span=span, bounds='regular', interval=interval)
        #print(hist)
        hist_df = pd.DataFrame()
        for i in range(len(hist)):
            df = pd.DataFrame(hist[i], index = [i])
            hist_df = pd.concat([hist_df,df])
        hist_df.begins_at = pd.to_datetime(hist_df.begins_at, infer_datetime_format=True)
        hist_df.open_price = hist_df.open_price.astype('float32')
        hist_df.close_price = hist_df.close_price.astype('float32')
        hist_df.high_price = hist_df.high_price.astype('float32')
        hist_df.low_price = hist_df.low_price.astype('float32')

        hist_df["mvg_avg_50"] = hist_df['open_price'].rolling(window=50).mean()
        hist_df["mvg_avg_50"] = hist_df["mvg_avg_50"].fillna(method='bfill')

        hist_df["mvg_avg_200"] = hist_df['open_price'].rolling(window=200).mean()
        hist_df["mvg_avg_200"] = hist_df["mvg_avg_200"].fillna(method='bfill')

        hist_df.to_excel("Excel Sheets/" + ticker_list[t] + ".xlsx")
        #print(hist_df.head())

        ax = hist_df.plot(x = 'begins_at', y = 'open_price', label= ticker_list[t] + " Open Price", figsize = (16,8))
        #ax.fill_between(hist_df.begins_at, hist_df.low_price, hist_df.high_price, alpha=0.5)

        ax.plot(hist_df['begins_at'][200:], hist_df['mvg_avg_200'][200:], label="200 Day MVA")
        ax.plot(hist_df['begins_at'][50:], hist_df['mvg_avg_50'][50:], label="50 Day MVA")

        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.legend()
        ax.set_title(name)
        plt.savefig("Graphs/" + ticker_list[t] + ".png")
        plt.close()
    return

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