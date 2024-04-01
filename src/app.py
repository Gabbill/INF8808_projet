
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Équipe 09
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import preprocess
from heatmap import heatmap
from scatterplot import get_rain_figure


# Data :
bike_counts_data_list = preprocess.load_bike_counts_data_list()
bike_counts_df = preprocess.get_bike_counts_df(bike_counts_data_list)

daily_bike_count = preprocess.get_daily_bike_count(bike_counts_df)
yearly_counters_count = preprocess.get_yearly_counters_count(bike_counts_df)
daily_bike_count_with_weather = preprocess.get_daily_bike_count_with_weather(
    bike_counts_data_list, bike_counts_df)

montreal_bike_paths = preprocess.load_montreal_bike_paths()

# HeatMap Graph
heatmap = heatmap(daily_bike_count)


# ScatterPlot Graph :
scatterplot = get_temperature_figure(daily_bike_count_with_weather)
scatterplot = get_snow_figure(daily_bike_count_with_weather)
scatterplot = get_rain_figure(daily_bike_count_with_weather)
#######

app = dash.Dash(__name__)
app.title = 'TP3 | INF8808'


app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Trees planted in Montreal neighborhoods'),
        html.H2('From 2010 to 2020')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(
            id='scatterplot',  # was heatmap before
            className='graph',
            figure=scatterplot,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
        dcc.Graph(
            id='line-chart',
            className='graph',
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )
    ])
])

# Callback pour réinitialiser le zoom du scatterplot avec deux clique


@app.callback(
    Output('scatterplot', 'relayoutData'),
    [Input('scatterplot', 'clickData')]
)
def reset_zoom(clickData):
    if clickData and 'dblclick' in clickData['event']:
        return {'autosize': True}


if __name__ == '__main__':
    app.run_server(debug=True)
