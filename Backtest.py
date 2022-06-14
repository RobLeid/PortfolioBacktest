import pandas as pd
import pandas_datareader as reader
import numpy as np
from datetime import date

##Start date and end date, although start date may get clipped if data not available, ie. company not public yet or ETF created after start date
start_date = '2000-01-01'
end_date =  date.today()

###List of stocks to pull data for with portfolio weights
portfolio = {'UPRO': 0.55, 'TMF' : 0.45}

###Check if portfolio values add up to 1, if not raise exception
if sum(portfolio.values()) != 1:
    raise Exception('Portfolio values should add up to 1')

###Start with SPY 
adj_close = reader.DataReader(name = 'SPY',data_source = 'yahoo', start = start_date, end = end_date)['Adj Close'].reset_index().rename(columns={'Adj Close' : 'SPY Adj Close'})
adj_close['SPY Return'] = adj_close['SPY Adj Close'].pct_change()
adj_close.drop(columns='SPY Adj Close', inplace=True)

##Get adjusted close for each part of the portfolio and calculate returns
for i in portfolio.keys():
    df = reader.DataReader(name = i, data_source = 'yahoo', start = start_date, end = end_date)['Adj Close'].reset_index().rename(columns={'Adj Close' : i + ' Adj Close'})
    df[i + ' Return'] = df[i + ' Adj Close'].pct_change()
    df.drop(columns=(i + ' Adj Close'), inplace=True)
    adj_close = pd.merge(adj_close, df)

##Drop first row because there is no return value
adj_close.drop(index=0, inplace=True)

##Summary time
spy_avg_return = np.mean(adj_close['SPY Return'])

##get portfolio average return
portfolio_avg_return = 0
for i in portfolio:
    component_return = np.mean(adj_close[i + ' Return'])
    weighted_return = portfolio[i] * component_return
    portfolio_avg_return += weighted_return
    
###Print start and end date of dataframe, which may differ from initial inputs based on availability of data. Also minus the first date because we removed that because return is null
print('AVERAGE YEARLY RETURNS BETWEEN {} AND {}'.format(adj_close['Date'].iloc[0].strftime('%Y-%m-%d'), adj_close['Date'].iloc[-1].strftime('%Y-%m-%d')))

###Average portfolio return rounded to 3 decimal points. Multiplied by 252 trading days per year
print("SPY AVG YEARLY RETURN: " + str(round(spy_avg_return*252*100,3)) +"%")
print("PORTFOLIO AVG YEARLY RETURN: " + str(round(portfolio_avg_return*252*100,3)) +"%")