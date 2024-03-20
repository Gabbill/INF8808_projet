import pandas as pd
import geopandas as gpd


def load_bike_counts_data_list():
    return [pd.read_csv(f'assets/comptage_velo_{year}.csv') for year in range(2019, 2025)]


def load_weather_data_list():
    return [pd.read_csv(f'assets/en_climate_daily_QC_7025251_{year}_P1D.csv') for year in range(2019, 2025)]


def load_counters_locations():
    return pd.read_csv('assets/localisation_des_compteurs_velo.csv')


def load_montreal_bike_paths():
    return gpd.read_file('assets/reseau_cyclable.geojson')


def get_bike_counts_df(bike_counts_data_list):
    return pd.concat(bike_counts_data_list, ignore_index=True)


def get_common_counters_2019_to_2024(bike_counts_data_list):
    df_id_compteurs = [set(df['id_compteur'].unique()) for df in bike_counts_data_list]
    return set.intersection(*df_id_compteurs)


# Visualisation 1
def get_daily_bike_count(bike_counts_df):
    return bike_counts_df.groupby('date')['nb_passages'].sum().reset_index()


# Visualisation 2
def get_hourly_bike_count(bike_counts_df):
    pass


# Visualisation 3
def get_yearly_counters_count(bike_counts_df):
    bike_counts_df['Année'] = pd.to_datetime(bike_counts_df['date']).dt.year
    yearly_count = bike_counts_df.groupby(['id_compteur', 'longitude', 'latitude', 'Année'])['nb_passages'].sum().reset_index()
    
    counters_locations_df = load_counters_locations()[['ID', 'Annee_implante']]
    counters_locations_df.rename(columns={'ID': 'id_compteur'}, inplace=True)
    counters_locations_df.loc[counters_locations_df['Annee_implante'] < 2019, 'Annee_implante'] = 2019
    counters_locations_df['Annee_implante'] = counters_locations_df['Annee_implante'].astype(str)
    
    return pd.merge(yearly_count, counters_locations_df, on='id_compteur', how='inner')


# Visualisation 4
def get_daily_bike_count_with_weather(bike_counts_data_list, bike_counts_df):
    common_counters = get_common_counters_2019_to_2024(bike_counts_data_list)
    normalized_bike_counts = bike_counts_df[bike_counts_df['id_compteur'].isin(common_counters)]
    normalized_bike_counts = get_daily_bike_count(normalized_bike_counts)

    weather_data_list = load_weather_data_list()
    df_weather = pd.concat(weather_data_list, ignore_index=True)[['Date/Time', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)']]
    df_weather.rename(columns={'Date/Time': 'date'}, inplace=True)
    
    return pd.merge(normalized_bike_counts, df_weather, on='date', how='inner')