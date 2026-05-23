import pandas as pd
import numpy as np
from indicators.ema import ema

def signal_ema_crossover(df,fast_ema=20,slow_ema=50):
    df = df.copy()
    
    df = ema(df, ema_list=[slow_ema,fast_ema])

    bullish_signal = (   (df[f'ema_{fast_ema}'] > df[f'ema_{slow_ema}']) 
                        & 
                        (df[f'ema_{fast_ema}'].shift(1) < df[f'ema_{slow_ema}'].shift(1)))
                    
    bearish_signal = (   (df[f'ema_{fast_ema}'] < df[f'ema_{slow_ema}']) 
                        & 
                        (df[f'ema_{fast_ema}'].shift(1) > df[f'ema_{slow_ema}'].shift(1)))
                    

    df['signal_ema_cross'] = 0;
    df.loc[bullish_signal,'signal_ema_cross'] = 1
    df.loc[bearish_signal,'signal_ema_cross'] = -1

    return df;