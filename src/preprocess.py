import pandas as pd
import geopandas as gpd
import utils


'''

Les fonctions suivantes permettent de charger les diffèrentes bases de données utilisés dans notre projet.

'''


# Chargement des données de comptage de vélos
def load_bike_counts_data_list():
    return [pd.read_csv(f'assets/data/comptage_velo_{year}.csv') for year in range(2019, 2025)]


# Chargement des données météorologiques
def load_weather_data_list():
    return [pd.read_csv(f'assets/data/en_climate_daily_QC_7025251_{year}_P1D.csv') for year in range(2019, 2025)]


# Chargement des données d'emplacements des compteurs de vélos
def load_counters_locations():
    return pd.read_csv('assets/data/localisation_des_compteurs_velo.csv')


# Chargement des données des pistes cyclables
def load_montreal_bike_paths():
    return gpd.read_file('assets/data/reseau_cyclable.geojson')


# Combinaison des diverses données de comptages de vélos
def get_bike_counts_df(bike_counts_data_list):
    return pd.concat(bike_counts_data_list, ignore_index=True)


# Données des compteurs de vélos communs de 2019 à 2024
def get_common_counters_2019_to_2024(bike_counts_data_list):
    df_id_compteurs = [set(df['id_compteur'].unique())
                       for df in bike_counts_data_list]
    return set.intersection(*df_id_compteurs)


'''

Les fonctions suivantes sont utilisés dans le pre-process de chaque visualisation.

'''


# Visualisation 1 : Heatmap
# Nombre quotidien de passages à vélo
def get_daily_bike_count(bike_counts_df):
    df = bike_counts_df.groupby('date')['nb_passages'].sum().reset_index()
    df['date'] = pd.to_datetime(df['date'])
    df['formatted_date'] = df['date'].dt.strftime(
        '%d %B %Y').apply(utils.translate_date)
    return df


# Visualisation 2 : Polar bar chart
# Détermination de la saison en fonction du mois
def get_season(month):
    if month in [12, 1, 2]:
        return 'Hiver'
    elif month in [3, 4, 5]:
        return 'Printemps'
    elif month in [6, 7, 8]:
        return 'Été'
    elif month in [9, 10, 11]:
        return 'Automne'


# Nombre de passages horaire pour chaque saison
def get_hourly_bike_count(bike_counts_df):
    bike_counts_df['date'] = pd.to_datetime(bike_counts_df['date'])
    bike_counts_df['season'] = bike_counts_df['date'].dt.month.apply(
        get_season)

    df = bike_counts_df.groupby(['heure', 'season'])[
        'nb_passages'].sum().reset_index()
    df['heure'] = pd.to_datetime(df['heure']).dt.strftime('%Hh')
    df = df.groupby(['heure', 'season'], as_index=False)['nb_passages'].sum()
    return df


# Visualisation 3 : Carte des compteurs et des pistes cyclables
# Calcul du nombre annuel de passages de vélos par compteur et intégration des données d'emplacement
def get_yearly_counters_count(bike_counts_df):
    bike_counts_df['Année'] = pd.to_datetime(bike_counts_df['date']).dt.year
    yearly_count = bike_counts_df.groupby(['id_compteur', 'longitude', 'latitude', 'Année'])[
        'nb_passages'].sum().reset_index()

    counters_locations_df = load_counters_locations()[['ID', 'Annee_implante']]
    counters_locations_df.rename(columns={'ID': 'id_compteur'}, inplace=True)
    counters_locations_df.loc[counters_locations_df['Annee_implante']
                              < 2019, 'Annee_implante'] = 2019
    counters_locations_df['Annee_implante'] = counters_locations_df['Annee_implante'].astype(
        str)

    return pd.merge(yearly_count, counters_locations_df, on='id_compteur', how='inner')


# Visualisation 4 : Scatter plot
# Traitement et fusion des nombres de passages quotidiens avec les données météorologiques
def get_daily_bike_count_with_weather(bike_counts_data_list, bike_counts_df):
    common_counters = get_common_counters_2019_to_2024(bike_counts_data_list)
    normalized_bike_counts = bike_counts_df[bike_counts_df['id_compteur'].isin(
        common_counters)]
    normalized_bike_counts = get_daily_bike_count(normalized_bike_counts)

    weather_data_list = load_weather_data_list()
    df_weather = pd.concat(weather_data_list, ignore_index=True)[
        ['Date/Time', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)']]

    df_weather.rename(columns={'Date/Time': 'date'}, inplace=True)
    df_weather['date'] = pd.to_datetime(df_weather['date'])
    df_weather['formatted_date'] = df_weather['date'].dt.strftime(
        '%d %B %Y').apply(utils.translate_date)

    return pd.merge(normalized_bike_counts, df_weather, on='date', how='inner')
