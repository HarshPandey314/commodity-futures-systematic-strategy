import pandas as pd
import numpy as np

def bollinger_bands(df,value="Close", period=20, multiplier=2 ):
    df = df.copy()

    df["bb_mid_band"] = df[value].rolling(window = period).mean()
    rolling_std = multiplier*df[value].rolling(window = period).std();
    df["bb_upper_band"] = df["bb_mid_band"] + rolling_std
    df["bb_lower_band"] = df["bb_mid_band"] - rolling_std
    df["bb_width_percent"] = (df["bb_upper_band"] - df["bb_lower_band"])/df["bb_mid_band"]

    return df;