
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
from dash.dependencies import Input, Output, State

import pandas as pd
import preprocess as preprocess
from heatmap import heatmap
from markups.visualisation_3 import create_viz3


bike_counts_data_list = preprocess.load_bike_counts_data_list()
bike_counts_df = preprocess.get_bike_counts_df(bike_counts_data_list)

daily_bike_count = preprocess.get_daily_bike_count(bike_counts_df)
yearly_counters_count = preprocess.get_yearly_counters_count(bike_counts_df)
daily_bike_count_with_weather = preprocess.get_daily_bike_count_with_weather(
    bike_counts_data_list, bike_counts_df)

montreal_bike_paths = preprocess.load_montreal_bike_paths()
heatmap = heatmap(daily_bike_count)

interactive_map = create_viz3(yearly_counters_count, montreal_bike_paths)

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
        dcc.Graph(id='map-visualization',
                  figure=interactive_map,
                  style={'height': '700px'}),
        # dcc.Slider(
        #     id='year-slider',
        #     min=2019,
        #     max=2024,
        #     value=2024,
        #     marks={str(year): str(year) for year in range(2019, 2025)},
        #     step=None,
        #     className='rc-slider',
        #     updatemode='drag'
        # ),
        # html.Button('Play/Pause', id='play-pause-button'),
        # html.Button('Restart', id='restart-button'),
        # dcc.Interval(
        #     id='interval-component',
        #     interval=1*1000,  # en millisecondes
        #     n_intervals=0,
        #     max_intervals=2024-2019,  # Arrêtez l'animation après avoir parcouru toutes les années
        #     disabled=True
        # )
        # html.H3('Visualisation 3', className='viz-title'),
        # dcc.Graph(
        #     id='viz3',
        #     figure=generate_viz3_figure(),
        #     className='graph',
        # )
    ])
])


# @app.callback(
#     Output('year-slider', 'value'),
#     [Input('interval-component', 'n_intervals')]
# )
# def update_year(n):
#     return 2019 + n  # Mettez à jour l'année en fonction du nombre d'intervalles


# @app.callback(
#     Output('interval-component', 'disabled'),
#     [Input('play-pause-button', 'n_clicks'),
#      Input('restart-button', 'n_clicks')],
#     [State('interval-component', 'disabled')]
# )
# def toggle_animation(play_pause_clicks, restart_clicks, currently_disabled):
#     if not dash.callback_context.triggered:
#         return True
#     if 'play-pause-button' in dash.callback_context.triggered[0]['prop_id']:
#         return not currently_disabled
#     elif 'restart-button' in dash.callback_context.triggered[0]['prop_id']:
#         return True


# @app.callback(
#     Output('interval-component', 'n_intervals'),
#     [Input('restart-button', 'n_clicks')]
# )
# def reset_intervals(n):
#     return 0  # Réinitialisez les intervalles lorsque le bouton de redémarrage est cliqué


# @app.callback(
#     Output('map-visualization', 'figure'),
#     [Input('year-slider', 'value')]
# )
# def update_figure(selected_year):
#     # return generate_viz3_figure(selected_year)
#     create_viz3(yearly_counters_count, montreal_bike_paths)
