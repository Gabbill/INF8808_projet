
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
import preprocess

from app_layout import get_app_layout
from visualizations.polar_bar_chart import get_seasonal_polar_chart
from visualizations.heatmap import get_heatmap
from visualizations.scatterplot import get_rain_figure, get_snow_figure, get_temperature_figure


# Récupération des données
bike_counts_data_list = preprocess.load_bike_counts_data_list()
bike_counts_df = preprocess.get_bike_counts_df(bike_counts_data_list)

daily_bike_count = preprocess.get_daily_bike_count(bike_counts_df)
hourly_bike_count = preprocess.get_hourly_bike_count(bike_counts_df)
yearly_counters_count = preprocess.get_yearly_counters_count(bike_counts_df)
daily_bike_count_with_weather = preprocess.get_daily_bike_count_with_weather(
    bike_counts_data_list, bike_counts_df)

# montreal_bike_paths = preprocess.load_montreal_bike_paths()

# Visualisation 1 - Heatmap
get_heatmap = get_heatmap(daily_bike_count)

# Visualisation 2 - Polar Bar Chart
polar_bar_chart_winter = get_seasonal_polar_chart(
    hourly_bike_count, 'Hiver')
polar_bar_chart_spring = get_seasonal_polar_chart(
    hourly_bike_count, 'Printemps')
polar_bar_chart_summer = get_seasonal_polar_chart(hourly_bike_count, 'Été')
polar_bar_chart_fall = get_seasonal_polar_chart(
    hourly_bike_count, 'Automne')

# Visualisation 3 - Carte
# TODO : insérer la visualisation ici

# Visualisation 4 - Scatter Plot
temperature_scatter_plot = get_temperature_figure(
    daily_bike_count_with_weather.copy(deep=True))
snow_scatter_plot = get_snow_figure(
    daily_bike_count_with_weather.copy(deep=True))
rain_scatter_plot = get_rain_figure(
    daily_bike_count_with_weather.copy(deep=True))


#######

app = dash.Dash(__name__)
app.title = 'Le vélo à Montréal'
server = app.server

# TODO: Ajouter toutes les figures (heatmap, horloge, map, température, neige, pluie)
app.layout = get_app_layout(
    get_heatmap,
    polar_bar_chart_winter,
    polar_bar_chart_spring,
    polar_bar_chart_summer,
    polar_bar_chart_fall,
    0,
    temperature_scatter_plot,
    snow_scatter_plot,
    rain_scatter_plot
)
