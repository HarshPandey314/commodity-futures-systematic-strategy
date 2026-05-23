import pandas as pd
import numpy as np

def atr(df,period = 14):
    df = df.copy()

    tr1 = df['High'] - df['Low']
    tr2 = abs(df['High'] - df['Close'].shift(1))
    tr3 = abs(df['Low'] - df['Close'].shift(1))

    tr_df = pd.DataFrame({
        "tr1" : tr1,
        "tr2" : tr2,
        "tr3" : tr3,
        })

    tr = tr_df.max(axis=1)

    df["atr"] = tr.ewm(alpha = 1/period, adjust=False).mean()

    return df;