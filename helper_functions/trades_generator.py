import pandas as pd
import numpy as np
from indicators.atr import atr

def checkExit(df,i,pos,trades,total_profit,target_factor,stop_factor):
    if (pos == 0 or len(trades) == 0):
        return pos, total_profit

    target = trades[-1]['entryPrice'] + pos*(target_factor*df.iloc[i]['atr'])
    stopLoss = trades[-1]['entryPrice'] - pos*(stop_factor*df.iloc[i]['atr'])
    if (pos == 1):
        if(df.iloc[i]['High'] >= target):
            trades[-1]['exitDate'] = df.index[i]
            trades[-1]['exitPrice'] = target
            pos=0
        elif(df.iloc[i]['Low'] <= stopLoss):
            trades[-1]['exitDate'] = df.index[i]
            trades[-1]['exitPrice'] = stopLoss
            pos=0
        if(df.iloc[i]['High'] >= target or df.iloc[i]['Low'] <= stopLoss):
            total_profit += trades[-1]['exitPrice'] - trades[-1]['entryPrice']
    elif(pos == -1):
        if(df.iloc[i]['Low'] <= target):
            trades[-1]['exitDate'] = df.index[i]
            trades[-1]['exitPrice'] = target
            pos=0
        elif(df.iloc[i]['High'] >= stopLoss):
            trades[-1]['exitDate'] = df.index[i]
            trades[-1]['exitPrice'] = stopLoss
            pos=0
        if(df.iloc[i]['Low'] <= target or df.iloc[i]['High'] >= stopLoss):
            total_profit += trades[-1]['entryPrice'] - trades[-1]['exitPrice'] 

    return pos,total_profit

def trades_generator(df):
    df = df.copy()

    final_signal = df['final_signal']
    df = atr(df)

    pos=0
    entryPrice = 0
    target_factor = 5
    stop_factor = 1.5
    target = pd.Series(np.nan,index=df.index)
    stopLoss = pd.Series(np.nan,index=df.index)
    trade_position = pd.Series(0,index=df.index)

    equity_curve = []
    drawdown = []
    peak_equity_pnl = -1e5;
    total_profit =0
    trades = []

    for i in range(len(df)-1):
        
        curr_equity = total_profit
        if(pos != 0):   curr_equity += pos*(df.iloc[i]['Close'] - trades[-1]['entryPrice'])
        equity_curve.append(curr_equity)

        peak_equity_pnl = max(peak_equity_pnl,curr_equity)
        curr_drawdown =  curr_equity - peak_equity_pnl
        drawdown.append(curr_drawdown)

        pos, total_profit = checkExit(df,i,pos,trades,total_profit,target_factor,stop_factor)

        if(final_signal.iloc[i] != 0):

            if(pos==0 or final_signal.iloc[i] == -pos):
                if(pos != 0 and final_signal.iloc[i] == -pos):
                    trades[-1]['exitDate'] = df.index[i]
                    trades[-1]['exitPrice'] = df.iloc[i]['Close']
                    total_profit += (trades[-1]['exitPrice'] - trades[-1]['entryPrice'])*pos
                    pos=0
                pos = final_signal.iloc[i];
                entryPrice = df.iloc[i+1]['Open']
                # trade_position[i+1] = pos;
                trades.append({
                    'entryDate' : df.index[i+1],
                    'entryPrice' : df.iloc[i+1]['Open'],
                    'initial_target' : entryPrice + (pos*df.iloc[i+1]['atr']*target_factor),
                    'initial_stopLoss' : entryPrice - (pos*df.iloc[i+1]['atr']*stop_factor),
                    'side' : ('buy' if final_signal.iloc[i] == 1 else 'sell'),
                })

          
    if (pos != 0):
        trades[-1]['exitDate'] = df.index[-1]
        trades[-1]['exitPrice'] = df.iloc[-1]['Close']
        total_profit += (trades[-1]['exitPrice'] - trades[-1]['entryPrice']) * pos    
        

    # print(f"Total trades: {len(trades)}")
    # print(df['final_signal'].value_counts())
    trades_df = pd.DataFrame(trades)
    # print(trades_df)
    trades_df['pnl'] = np.where(trades_df['side'] == 'buy',
                                trades_df['exitPrice'] - trades_df['entryPrice'],
                                -1*(trades_df['exitPrice'] - trades_df['entryPrice'])
                                )
    trades_df['pct_return'] = (trades_df['pnl']/trades_df['entryPrice'])*100

    return trades_df,equity_curve,drawdown



