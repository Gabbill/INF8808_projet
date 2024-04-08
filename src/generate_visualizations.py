import preprocess

from visualizations.polar_bar_chart import get_seasonal_polar_chart
from visualizations.heatmap import get_heatmap
from visualizations.scatter_plot import get_rain_figure, get_snow_figure, get_temperature_figure


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
heatmap = get_heatmap(daily_bike_count)
heatmap.write_json('json/heatmap.json')

# Visualisation 2 - Polar Bar Chart
polar_bar_chart_winter = get_seasonal_polar_chart(
    hourly_bike_count, 'Hiver')
polar_bar_chart_spring = get_seasonal_polar_chart(
    hourly_bike_count, 'Printemps')
polar_bar_chart_summer = get_seasonal_polar_chart(hourly_bike_count, 'Été')
polar_bar_chart_fall = get_seasonal_polar_chart(
    hourly_bike_count, 'Automne')
polar_bar_chart_winter.write_json('json/polar_bar_chart_winter.json')
polar_bar_chart_spring.write_json('json/polar_bar_chart_spring.json')
polar_bar_chart_summer.write_json('json/polar_bar_chart_summer.json')
polar_bar_chart_fall.write_json('json/polar_bar_chart_fall.json')

# Visualisation 3 - Carte
# TODO : insérer la visualisation ici et décommenté le code ici et dans app.py
# map = TODO
# map.write_json('json/map.json')

# Visualisation 4 - Scatter Plot
temperature_scatter_plot = get_temperature_figure(
    daily_bike_count_with_weather.copy(deep=True))
snow_scatter_plot = get_snow_figure(
    daily_bike_count_with_weather.copy(deep=True))
rain_scatter_plot = get_rain_figure(
    daily_bike_count_with_weather.copy(deep=True))
temperature_scatter_plot.write_json('json/temperature_scatter_plot.json')
snow_scatter_plot.write_json('json/snow_scatter_plot.json')
rain_scatter_plot.write_json('json/rain_scatter_plot.json')
