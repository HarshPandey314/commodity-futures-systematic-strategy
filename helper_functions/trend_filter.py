import pandas as pd
import numpy as np
from indicators.ema import ema
from indicators.obv import obv

def trend_filter(df,ema_list = [20,50,100],obv_ema_period=20):

    df = df.copy();
    
    df = ema(df=df,ema_list=ema_list);

    bullish_condition = pd.Series(True, index= df.index)
    for ema_val in ema_list:
        bullish_condition &= (df['Low'] > df[f'ema_{ema_val}'])
    bearish_condition = pd.Series(True, index= df.index)
    for ema_val in ema_list:
        bearish_condition &= (df['High'] < df[f'ema_{ema_val}'])

    # added obv indicator as well
    df = obv(df)
    df['obv_ema'] = df['obv'].ewm(span = obv_ema_period,adjust=False).mean()

    bullish_condition_obv = df['obv'] > df['obv_ema']
    bearish_condition_obv = df['obv'] < df['obv_ema']

    bullish_condition &= bullish_condition_obv
    bearish_condition &= bearish_condition_obv

    df['trend_signal'] = 0;
    df.loc[bullish_condition,'trend_signal'] = 1;
    df.loc[bearish_condition,'trend_signal'] = -1;

    return df;
