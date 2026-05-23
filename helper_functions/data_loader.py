import pandas as pd
import numpy as np
import yfinance as yf

def data_loader(contract_name = 'ZS=F', period = '365d'):

    df_daily = yf.download(contract_name,period = period,interval='1d')
    df_daily.columns = df_daily.columns.droplevel(1);
    if df_daily.index.tz is None:
        df_daily.index = df_daily.index.tz_localize('UTC')
    else:
        df_daily.index = df_daily.index.tz_convert('UTC')

    df_60 = yf.download(contract_name,period = period, interval = '60m')
    df_60.columns = df_60.columns.droplevel(1)

    # Filter to main trading hours only (CME grain futures: 8:30 AM - 1:20 PM CT = 13:30 - 18:20 UTC)
    df_60 = df_60.between_time('13:30', '18:20')
    df_60 = df_60[df_60.index.dayofweek < 5] #Remove weekends
    # print(df_60);

    df_240 = df_60.resample('240min').agg({
        'Open' : 'first',
        'Close' : 'last',
        'High' : 'max',
        'Low' : 'min',
        'Volume' : 'sum',
    }).dropna()

    # print(df_240)
    # print(df_60.index[0]," ",df_60.index[-1])
    # print(df_240.index[0]," ",df_240.index[-1])
    # print(f'{len(df_60)} - rows in 60 min')
    # print(f'{len(df_240)} - rows in 240 min')

    return {
        'df_60' : df_60,
        'df_240' : df_240,
        'df_daily' : df_daily,
    }


