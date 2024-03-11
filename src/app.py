
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd


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
        )
    ])
])
