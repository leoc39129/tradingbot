'''
Notes:

Set up a class/model that is abstractable?

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

def buy_cond(fd, td, day):
    # fd is the last three days of 50 day moving averages
    # td is the last three days of 200 day moving averages
    return (fd[day] > td[day]) and (fd[day] - fd[day-2] > 0) and (td[day] - td[day-2] > 0) and (fd[day] - td[day] < .15*td[day])

def sell_cond(fd, td, day):
    fd_slope = (fd[day] - fd[day-2]) * .5
    td_slope = (td[day] - td[day-2]) * .5  
    return (fd[day] > td[day]) and (fd_slope < 0) and (td_slope > 0) and (abs(fd_slope) > td_slope)