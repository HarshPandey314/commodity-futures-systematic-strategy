import pandas as pd
import numpy as np

def obv(df):
    df = df.copy();

    signaled_volume = np.where(
        df['Close'].diff() > 0, 
        df['Volume'], 
        np.where(df['Close'].diff() < 0, -df['Volume'], 0)
        );
    df['obv'] = signaled_volume.cumsum();

    return df;