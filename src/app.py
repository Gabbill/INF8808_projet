
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Émile Watier, Gabriel Billard, Jonathan Tapiero, 
            Lana Pham, Nargisse Benbiga, Thomas Logeais
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import dash
import preprocess

from app_layout import get_app_layout
from visualizations.polar_bar_chart import create_seasonal_polar_chart
from visualizations.heatmap import heatmap
from visualizations.scatterplot import get_rain_figure, get_snow_figure, get_temperature_figure


# Data :
bike_counts_data_list = preprocess.load_bike_counts_data_list()
bike_counts_df = preprocess.get_bike_counts_df(bike_counts_data_list)

daily_bike_count = preprocess.get_daily_bike_count(bike_counts_df)
yearly_counters_count = preprocess.get_yearly_counters_count(bike_counts_df)
daily_bike_count_with_weather = preprocess.get_daily_bike_count_with_weather(
    bike_counts_data_list, bike_counts_df)

hourly_bike_count = preprocess.get_hourly_bike_count(bike_counts_df)

montreal_bike_paths = preprocess.load_montreal_bike_paths()

# HeatMap Graph
heatmap = heatmap(daily_bike_count)


# ScatterPlot Graph :
temperature_scatter_plot = get_temperature_figure(
    daily_bike_count_with_weather.copy(deep=True))
snow_scatter_plot = get_snow_figure(
    daily_bike_count_with_weather.copy(deep=True))
rain_scatter_plot = get_rain_figure(
    daily_bike_count_with_weather.copy(deep=True))

# Polar Bar Chart :
polar_bar_chart_winter = create_seasonal_polar_chart(
    hourly_bike_count, 'Hiver')
polar_bar_chart_spring = create_seasonal_polar_chart(
    hourly_bike_count, 'Printemps')
polar_bar_chart_summer = create_seasonal_polar_chart(hourly_bike_count, 'Été')
polar_bar_chart_fall = create_seasonal_polar_chart(
    hourly_bike_count, 'Automne')


#######

app = dash.Dash(__name__)
app.title = 'Le vélo à Montréal'

# TODO: Ajouter toutes les figures (heatmap, horloge, map, température, neige, pluie)
app.layout = get_app_layout(
    heatmap,
    0,
    0,
    temperature_scatter_plot,
    snow_scatter_plot,
    rain_scatter_plot
)
