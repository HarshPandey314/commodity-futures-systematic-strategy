import pandas as pd
import numpy as np
from indicators.macd import macd
from indicators.rsi import rsi

def signal_macd_rsi(df,slow_ema = 26,fast_ema=12,signal_period = 9,rsi_period=14):

    df = df.copy()

    df = macd(df,slow=slow_ema,fast = fast_ema,signal=signal_period);
    df = rsi(df,period=rsi_period)

    df['Volume_avg'] = df['Volume'].rolling(20).mean();

    bullish_condition = ( 
        (df['macd'] > df['macd_signal']) &
        (df['macd'].shift(1) < df['macd_signal'].shift(1)) &
        (df['rsi'] > 50) &
        (df['Volume'] > df['Volume_avg'])
        )
    bearish_condition = ( 
        (df['macd'] < df['macd_signal']) &
        (df['macd'].shift(1) > df['macd_signal'].shift(1)) &
        (df['rsi'] < 50) &
        (df['Volume'] > df['Volume_avg'])
        )
    
    df['signal_macd_rsi'] = 0;
    df.loc[bullish_condition,'signal_macd_rsi'] = 1;
    df.loc[bearish_condition,'signal_macd_rsi'] = -1;
    
    return df;
