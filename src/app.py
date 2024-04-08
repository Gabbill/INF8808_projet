
# -*- coding: utf-8 -*-

'''
    Nom du fichier : app.py
    Auteurs : Émile Watier, Gabriel Billard, Jonathan Tapiero, 
            Lana Pham, Nargisse Benbiga, Thomas Logeais
    Cours: INF8808
    Version de Python: 3.8

    Ce fichier est le point d'entrée de notre application Dash.
'''

import dash
import plotly

from app_layout import get_app_layout

app = dash.Dash(__name__)
app.title = 'Le vélo à Montréal'
server = app.server

# Read Visualisation 1 - Heatmap
heatmap = plotly.io.read_json('json/heatmap.json')

# Read Visualisation 2 - Polar Bar Charts
polar_bar_chart_winter = plotly.io.read_json(
    'json/polar_bar_chart_winter.json')
polar_bar_chart_spring = plotly.io.read_json(
    'json/polar_bar_chart_spring.json')
polar_bar_chart_summer = plotly.io.read_json(
    'json/polar_bar_chart_summer.json')
polar_bar_chart_fall = plotly.io.read_json('json/polar_bar_chart_fall.json')

# Read Visualisation 3 - Carte (assuming this is a Plotly figure)
# TODO décommenté le code ci-dessous
# map = plotly.io.read_json('json/map.json')
map = 0  # TODO à retirer

# Read Visualisation 4 - Scatter Plots
temperature_scatter_plot = plotly.io.read_json(
    'json/temperature_scatter_plot.json')
snow_scatter_plot = plotly.io.read_json('json/snow_scatter_plot.json')
rain_scatter_plot = plotly.io.read_json('json/rain_scatter_plot.json')

app.layout = get_app_layout(
    heatmap,
    polar_bar_chart_winter,
    polar_bar_chart_spring,
    polar_bar_chart_summer,
    polar_bar_chart_fall,
    map,
    temperature_scatter_plot,
    snow_scatter_plot,
    rain_scatter_plot
)
