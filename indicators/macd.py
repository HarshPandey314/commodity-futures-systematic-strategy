import pandas as pd;
import numpy as np

def macd(df,value = "Close", slow=26, fast=12, signal=9):
    df = df.copy()

    slow_ema = df[value].ewm(span = slow,adjust = False).mean()
    fast_ema = df[value].ewm(span = fast,adjust = False).mean()
    df["macd"] = fast_ema - slow_ema;
    df["macd_signal"] = df["macd"].ewm(span = signal,adjust = False).mean();
    df["macd_histogram"] = df["macd"] - df["macd_signal"]

    return df;