import pandas as pd
import numpy as np
import datetime as dt

def analyze_trades(df,equity_curve,drawdown):
    metrics = {}
    metrics["total_pnl"] = df['pnl'].sum()
    metrics["num_trades"] = len(df)
    metrics["win_rate"] = ((df.pnl > 0).mean())*100
    metrics["loss_rate"] = ((df.pnl <= 0).mean())*100
    metrics["avg_trade_return"] = df.pct_return.mean()
    metrics["avg_win_pct_return"] = df[df.pct_return > 0].pct_return.mean()
    metrics["avg_loss_pct_return"] = abs(df[df.pct_return < 0].pct_return.mean())
    metrics["avg_winning_trade_pnl"] = df[df.pnl > 0].pnl.mean()
    metrics["avg_losing_trade_pnl"] = df[df.pnl <= 0].pnl.mean()
    metrics["largest_winner"] = df.pnl.max()
    metrics["largest_loser"] = df.pnl.min()
    metrics["gross_profit"] = df[(df.pnl > 0)].pnl.sum()
    metrics["gross_loss"] = abs(df[(df.pnl < 0)].pnl.sum())
    metrics["profit_factor"] = metrics["gross_profit"]/metrics["gross_loss"]
    # metrics["equity_curve"] = equity_curve
    # metrics["drawdown"] = drawdown
    metrics["max_drawdown"] = min(drawdown)
    metrics["avg_drawdown"] = sum(drawdown)/len(drawdown)
    metrics['final_equity'] = equity_curve[-1]
    metrics["riskReward"] = metrics["avg_winning_trade_pnl"]/abs(metrics["avg_losing_trade_pnl"])
    metrics["expectancy"] = (metrics["win_rate"]*metrics["avg_win_pct_return"] 
                                 - metrics["loss_rate"]*metrics["avg_loss_pct_return"])/100

    returns = df['pnl'] / df['entryPrice']
    metrics['sharpe_ratio'] = (returns.mean() / returns.std()) * np.sqrt(252)

    losses = (df['pnl'] < 0).astype(int)
    max_consec = 0
    current = 0
    for val in losses:
        if val == 1:
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 0
    metrics['max_consecutive_losses'] = max_consec
    # print(metrics)

    return metrics