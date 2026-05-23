import pandas as pd
import numpy as np
from helper_functions.trend_filter import trend_filter
from helper_functions.signal_ema_crossover import signal_ema_crossover
from helper_functions.signal_macd_rsi import signal_macd_rsi


def final_signal_generator(df_daily,df_240,df_60):
    df_daily = df_daily.copy()
    df_240 = df_240.copy()
    df_60 = df_60.copy()

    df_daily = trend_filter(df_daily,ema_list=[20,50,100])

    df_60['trend_signal_daily'] = df_daily['trend_signal'].reindex(df_60.index,method='ffill')

    df_240 = signal_ema_crossover(df_240,slow_ema=50,fast_ema=20)
    df_60['entry_signal_240'] = df_240['signal_ema_cross'].reindex(df_60.index,method='ffill')

    df_60 = signal_macd_rsi(df_60)
    df_60['entry_signal_60'] = df_60['signal_macd_rsi']

    # Combining signals in all timeframes

    bullish_condition = ((df_60['trend_signal_daily']==1) &
                                ((df_60['entry_signal_240']==1) | 
                                    (df_60['entry_signal_60']==1)
                                ))
    bearish_condition = ((df_60['trend_signal_daily']==-1) &
                                ((df_60['entry_signal_240']==-1) | 
                                    (df_60['entry_signal_60']==-1)
                                ))

    df_60['final_signal'] = 0;
    df_60.loc[bullish_condition,'final_signal'] = 1;
    df_60.loc[bearish_condition,'final_signal'] = -1;

    return df_daily,df_240,df_60;