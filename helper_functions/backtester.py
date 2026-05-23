import pandas as pd
import numpy as np

def backtest_func(df,signal):
    df = df.copy()

    trades = []
    curr_pos=0
    desired_pos=0
    equity_curve = []
    drawdown = []
    total_pnl = 0
    peak_equity_pnl=0
    for i in range(1,len(df)-1):
        desired_pos = signal.iloc[i];
        bullish_condition = desired_pos > curr_pos
        bearish_condition = desired_pos < curr_pos

        if(curr_pos != 0): 
            curr_equity_pnl = total_pnl + curr_pos*(df.iloc[i]['Close'] - trades[-1]['entryPrice']) 
        else:  curr_equity_pnl = total_pnl  

        equity_curve.append(curr_equity_pnl)
        if(i==1):   peak_equity_pnl = curr_equity_pnl
        else:       peak_equity_pnl = max(peak_equity_pnl,curr_equity_pnl)
        
        curr_drawdown =  curr_equity_pnl - peak_equity_pnl
        drawdown.append(curr_drawdown)

        if(bullish_condition):
            #initiate long position
            if(curr_pos != 0):
                trades[-1]["exitDate"] = df.index[i+1]
                trades[-1]["exitPrice"] = df.iloc[i+1]['Open']
                trades[-1]["pnl"] = trades[-1]["exitPrice"] - trades[-1]["entryPrice"]
                total_pnl += trades[-1]['pnl']
            trades.append({
                "entryDate" : df.index[i+1],
                "entryPrice" : df.iloc[i+1]['Open'],
                "side" : "buy",
            })
            curr_pos = 1;
        elif(bearish_condition) :
            #initialte short posotion
            if(curr_pos != 0):
                trades[-1]["exitDate"] = df.index[i+1]
                trades[-1]["exitPrice"] = df.iloc[i+1]['Open']
                trades[-1]["pnl"] = trades[-1]["entryPrice"] - trades[-1]["exitPrice"]
                total_pnl += trades[-1]['pnl']
            trades.append({
                "entryDate" : df.index[i+1],
                "entryPrice" : df.iloc[i+1]['Open'],
                "side" : "sell",
            })
            curr_pos = -1;

    if(curr_pos != 0):
        if(curr_pos == 1):
            trades[-1]["exitDate"] = df.index[-1]
            trades[-1]["exitPrice"] = df.iloc[-1]['Close']
            trades[-1]["pnl"] = trades[-1]["exitPrice"] - trades[-1]["entryPrice"]
        else:
            trades[-1]["exitDate"] = df.index[-1]
            trades[-1]["exitPrice"] = df.iloc[-1]['Close']
            trades[-1]["pnl"] = trades[-1]["entryPrice"] - trades[-1]["exitPrice"]
        total_pnl += trades[-1]['pnl']
        equity_curve.append(total_pnl)
        peak_equity_pnl = max(peak_equity_pnl,total_pnl)
        drawdown.append(total_pnl - peak_equity_pnl)

    trades_df = pd.DataFrame(trades)
    trades_df = trades_df[['entryDate','exitDate','side','entryPrice','exitPrice','pnl']]
    trades_df['pct_return'] = (trades_df['pnl']/trades_df['entryPrice'])*100 

    return {
        "trades_df" : trades_df,
        "equity_curve" : equity_curve,
        "drawdown" : drawdown,
    };