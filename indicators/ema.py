import pandas as pd
import numpy as np

def ema(df, value="Close", ema_list = [20,50,100]):
    df = df.copy();

    for ema_value in ema_list:
        ema_col = f"ema_{ema_value}";
        df[ema_col] = df[value].ewm(span = ema_value,adjust = False).mean()
    
    return df;

