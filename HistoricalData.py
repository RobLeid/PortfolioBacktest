import pandas as pd
import pandas_datareader as reader

##Start date and end date
start_date = '2009-06-25'
end_date = '2022-05-28'

##List of stocks to pull data for
stock_list = ['SPY', 'TMF', 'UPRO']

##Create dataframe with range of dates, so each stock's adj close can be merged in
adj_close = pd.DataFrame({'Date': pd.date_range(start = start_date, end = end_date)})

##iterate through list of stocks
for i in range(len(stock_list)):
    ##query yahoo finance for adj close of each stock in list
    df = reader.DataReader(name = stock_list[i], data_source = 'yahoo', start = start_date, end = end_date)['Adj Close'].reset_index()
    ##rename adj close column to include ticker symbol
    df.rename(columns={'Adj Close': stock_list[i] +' Adj Close'}, inplace=True)
    ##merge each ticker's adj close into dataframe
    adj_close = pd.merge(adj_close, df)

print(adj_close)



