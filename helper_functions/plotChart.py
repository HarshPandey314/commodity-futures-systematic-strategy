import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
# import plotly.io as pio
# pio.renderers.default = 'browser'

def create_line_chart(df,items = []):
    fig = go.Figure();
    for i in range(len(items)):
        series = items[i]['series']
        color = items[i]['color']
        fig.add_trace(
        go.Scatter(
            x = df.index,
            y = series,
            mode = 'lines',
            line = dict(
                color=color,
                width = 0.7,
            ),
            name = items[i]['name'],
        )
    )

    fig.show()

def create_candleStick_chart(df, overlays=[], subplots=[],markers=[],barGraphs=[]):
    # fig = go.Figure()

    k = len(subplots) + len(barGraphs)
    main_chart_height = 1 - min(0.2*k,0.4);
    sub_chart_height =  0;
    if(subplots or barGraphs):  sub_chart_height = (min(0.2*k,0.4))/k

    row_heights = [main_chart_height]
    for i in range(k):
        row_heights.append(sub_chart_height)
    

    fig = make_subplots(
                rows=1 + k,
                cols=1,
                shared_xaxes= True,
                vertical_spacing= 0.03,
                row_heights= row_heights
        )

    fig.add_trace(
        go.Candlestick(
            x = df.index,
            open = df['Open'],
            close = df['Close'],
            high = df['High'],
            low = df['Low'],
            name = "candles",
        ),
        row=1,
        col=1,
    )

    for items in overlays:
        item = items[0]
        color = items[1]
        fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df[item],
            mode = 'lines',
            line = dict(
                color=color,
                width=0.5,
            ),
            name = item,
        ),
        row=1,
        col=1,
    )
    
    for item in markers:
        signal = df[item]
        buy_signal = (signal == 1)
        sell_signal = (signal == -1)
        fig.add_trace(
            go.Scatter(
                x = df.index[buy_signal].shift(1,freq='60min'),
                y = df['Low'][buy_signal] * 0.9999,
                mode = 'markers',
                marker= dict( symbol = 'triangle-up', color  = 'blue', size = 10),
                name = 'buy_triangle',
            )
        )
        fig.add_trace(
            go.Scatter(
                x = df.index[sell_signal].shift(1,freq='60min'),
                y = df['High'][sell_signal]*1.0001,
                mode = 'markers',
                marker= dict( symbol = 'triangle-down', color  = 'red', size = 10),
                name = 'sell_triangle',
            )
        )
    
    for i in range(len(subplots)):
        subplot_items = subplots[i];
        for j in range(len(subplot_items)):
            item = subplot_items[j]
            fig.add_trace(
            go.Scatter(
                x = df.index,
                y = df[item],
                mode = 'lines',
                line = dict(
                    color = 'red',
                    width = 0.5,
                ),
                name = item,
            ),
            row = i+2,
            col=1,
        )
            
    for i in range(len(barGraphs)):
        item = barGraphs[i];
        fig.add_trace(
            go.Bar(
                x = df.index,
                y = df[item],
                name = 'Volume',
                marker_color = 'blue',
            ),
            row = len(subplots) + i + 2,
            col=1,
        )

    # fig.update_layout(bargap=0)
    # fig.update_yaxes(range=[0, df['Volume'].max() * 0.5], row=len(subplots) + 2, col=1)
    fig.update_yaxes(fixedrange=False)
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        )
    fig.show()