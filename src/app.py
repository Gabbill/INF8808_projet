
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
import preprocess as preprocess
from heatmap import heatmap
from markups.visualisation_3 import generate_viz3_figure



bike_counts_data_list = preprocess.load_bike_counts_data_list()
bike_counts_df = preprocess.get_bike_counts_df(bike_counts_data_list)

daily_bike_count = preprocess.get_daily_bike_count(bike_counts_df)
yearly_counters_count = preprocess.get_yearly_counters_count(bike_counts_df)
daily_bike_count_with_weather = preprocess.get_daily_bike_count_with_weather(
    bike_counts_data_list, bike_counts_df)

montreal_bike_paths = preprocess.load_montreal_bike_paths()

heatmap = heatmap(daily_bike_count)


app = dash.Dash(__name__)
app.title = 'TP3 | INF8808'


app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Trees planted in Montreal neighborhoods'),
        html.H2('From 2010 to 2020')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(
            id='heatmap',
            className='graph',
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
        ),
         dcc.Slider(
        id='year-slider',
        min=2019,
        max=2024,
        value=2024,
        marks={str(year): str(year) for year in range(2019, 2025)},
        step=None
    ),
        dcc.Graph(id='map-visualization')
        # html.H3('Visualisation 3', className='viz-title'),
        # dcc.Graph(
        #     id='viz3',
        #     figure=generate_viz3_figure(), 
        #     className='graph',
        # )
    ])
])

@app.callback(
    Output('map-visualization', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    return generate_viz3_figure(selected_year)

