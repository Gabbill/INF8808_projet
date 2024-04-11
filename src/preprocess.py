import pandas as pd
import geopandas as gpd
import utils
import shapely.geometry


# Les fonctions suivantes permettent de charger les diverses données utilisées
# au sein de notre projet.


def load_bike_counts_data_list():
    '''
    Chargement des données de comptage de vélos
    '''
    return [pd.read_csv(f'assets/data/comptage_velo_{year}.csv') for year in range(2019, 2025)]


def load_weather_data_list():
    '''
    Chargement des données météorologiques
    '''
    return [pd.read_csv(f'assets/data/en_climate_daily_QC_7025251_{year}_P1D.csv') for year in range(2019, 2025)]


def load_counters_locations():
    '''
    Chargement des données d'emplacements des compteurs de vélos
    '''
    return pd.read_csv('assets/data/localisation_des_compteurs_velo.csv')


def load_montreal_bike_paths():
    '''
    Chargement des données des pistes cyclables
    '''
    montreal_bike_paths = gpd.read_file('assets/data/reseau_cyclable.geojson')
    lats = []
    lons = []
    names = []

    for feature, name in zip(montreal_bike_paths.geometry, montreal_bike_paths.NOM_ARR_VILLE_DESC):
        if not isinstance(feature, shapely.geometry.linestring.LineString):
            continue

        x, y = feature.xy
        # None pour créer un écart dans la ligne
        lats.extend(y.tolist() + [None])
        lons.extend(x.tolist() + [None])
        names.extend([name] * (len(x) + 1))

    return lats, lons, names


def get_bike_counts_df(bike_counts_data_list):
    '''
    Combinaison des diverses données de comptages de vélos
    '''
    return pd.concat(bike_counts_data_list, ignore_index=True)


def get_common_counters_2019_to_2024(bike_counts_data_list):
    '''
    Données des compteurs de vélos communs de 2019 à 2024
    '''
    df_id_compteurs = [set(df['id_compteur'].unique())
                       for df in bike_counts_data_list]
    return set.intersection(*df_id_compteurs)


# Les fonctions suivantes sont utilisées pour l'obtention des données nécessaires
# à chaque visualisation


def get_daily_bike_count(bike_counts_df):
    '''
    Visualisation 1 : Heatmap
    Nombre quotidien de passages à vélo
    '''
    # Nombre de passages quotidien
    df = bike_counts_df.groupby('date')['nb_passages'].sum().reset_index()

    # Ajout de la date formattée (JJ mois AAAA)
    df['date'] = pd.to_datetime(df['date'])
    df['formatted_date'] = df['date'].dt.strftime(
        '%d %B %Y').apply(utils.translate_date)
    return df


def get_hourly_bike_count(bike_counts_df):
    '''
    Visualisation 2 : Polar bar chart
    Nombre de passages horaire pour chaque saison
    '''
    # Ajout de la saison
    bike_counts_df['date'] = pd.to_datetime(bike_counts_df['date'])
    bike_counts_df['season'] = bike_counts_df['date'].dt.month.apply(
        get_season)

    # Nombre de passages par heure pour chaque saison
    df = bike_counts_df.groupby(['heure', 'season'])[
        'nb_passages'].sum().reset_index()
    df['heure'] = pd.to_datetime(df['heure']).dt.strftime('%Hh')
    df = df.groupby(['heure', 'season'], as_index=False)['nb_passages'].sum()

    return df


def get_season(month):
    '''
    Détermination de la saison en fonction du mois
    '''
    if month in [12, 1, 2]:
        return 'Hiver'
    elif month in [3, 4, 5]:
        return 'Printemps'
    elif month in [6, 7, 8]:
        return 'Été'
    elif month in [9, 10, 11]:
        return 'Automne'


def get_yearly_counters_count(bike_counts_df):
    '''
    Visualisation 3 : Carte des compteurs et des pistes cyclables
    Nombre annuel de passages à vélo par compteur et l'emplacement des compteurs
    '''
    # Nombre de passages à vélo annuel pour chaque compteur
    bike_counts_df['Année'] = pd.to_datetime(bike_counts_df['date']).dt.year
    yearly_count = bike_counts_df.groupby(['id_compteur', 'longitude', 'latitude', 'Année'])[
        'nb_passages'].sum().reset_index()

    # Modification de l'année implantée à 2019 si elle est inférieure à 2019
    counters_locations_df = load_counters_locations()[['ID', 'Annee_implante']]
    counters_locations_df.rename(columns={'ID': 'id_compteur'}, inplace=True)
    counters_locations_df.loc[counters_locations_df['Annee_implante']
                              < 2019, 'Annee_implante'] = 2019
    counters_locations_df['Annee_implante'] = counters_locations_df['Annee_implante'].astype(
        str)

    # Ajout de l'année d'implantation pour chaque compteur
    yearly_count = pd.merge(
        yearly_count, counters_locations_df, on='id_compteur', how='inner')

    years = yearly_count['Année'].unique()
    for counter_id in yearly_count['id_compteur'].unique():
        counter = yearly_count[yearly_count['id_compteur'] == counter_id]
        for year in years:
            if year not in counter['Année'].values:
                yearly_count.loc[len(yearly_count)] = [counter_id, counter['longitude'].values[0],
                                                       counter['latitude'].values[0], year, 0, counter['Annee_implante'].values[0]]

    # Nombre de passages par jour
    yearly_count['passages_par_jour'] = yearly_count['nb_passages'] / 365

    # Le nombre de passage doit être à 0 si l'année d'implantation est supérieure à l'année de comptage
    yearly_count.loc[yearly_count['Année']
                     < yearly_count['Annee_implante'].astype(int), 'nb_passages'] = 0

    # Retrait des enregistrements de l'année 2024
    yearly_count = yearly_count[yearly_count['Année'] < 2024]

    return yearly_count


def get_daily_bike_count_with_weather(bike_counts_data_list, bike_counts_df):
    '''
    Visualisation 4 : Scatter plot
    Traitement et fusion des nombres de passages quotidiens avec les données météorologiques
    '''
    # Considérer seulement les compteurs communs aux années 2019 à 2024
    common_counters = get_common_counters_2019_to_2024(bike_counts_data_list)
    normalized_bike_counts = bike_counts_df[bike_counts_df['id_compteur'].isin(
        common_counters)]

    # Nombre de passages quotidien pour les compteurs communs aux années 2019 à 2024
    normalized_bike_counts = get_daily_bike_count(normalized_bike_counts)

    # Ajout des données météorologiques pour chaque jour
    weather_data_list = load_weather_data_list()
    df_weather = pd.concat(weather_data_list, ignore_index=True)[
        ['Date/Time', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)']]

    # Ajout de la date formattée (JJ mois AAAA)
    df_weather.rename(columns={'Date/Time': 'date'}, inplace=True)
    df_weather['date'] = pd.to_datetime(df_weather['date'])
    df_weather['formatted_date'] = df_weather['date'].dt.strftime(
        '%d %B %Y').apply(utils.translate_date)

    return pd.merge(normalized_bike_counts, df_weather, on='date', how='inner')
