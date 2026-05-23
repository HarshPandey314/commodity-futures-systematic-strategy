import pandas as pd
import numpy as np

def rsi(df, value ="Close", period = 14):
    df = df.copy();

    delta_p = df[value].diff()
    gain = delta_p.clip(lower=0)
    loss = -delta_p.clip(upper=0)

    avg_gain = gain.ewm(alpha = 1/period, adjust = False).mean()
    avg_loss = loss.ewm(alpha = 1/period, adjust = False).mean()

    rs = avg_gain/avg_loss
    df["rsi"] = 100 - 100/(1+rs);

    return df;
