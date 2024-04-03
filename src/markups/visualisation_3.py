import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import shapely.geometry
import numpy as np
import pandas as pd

def get_compteurs_dataframe(selected_year):
    localisation_data = pd.read_csv('assets/data/localisation_des_compteurs_velo.csv')
    localisation_data = localisation_data[localisation_data['Annee_implante'] >= 2019]

    compteurs = pd.read_csv(f'assets/data/comptage_velo_{selected_year}.csv')
    compteurs['date'] = pd.to_datetime(compteurs['date'])
    compteurs = compteurs[compteurs['date'].dt.year <= selected_year]
    compteurs = compteurs.groupby(['id_compteur', 'longitude', 'latitude'])['nb_passages'].sum().reset_index()
    
    localisation_compteurs = localisation_data[['ID', 'Annee_implante']].copy()
    localisation_compteurs.rename(columns={'ID': 'id_compteur'}, inplace=True)
    
    localisation_compteurs['Annee_implante'] = localisation_compteurs['Annee_implante'].astype(str)
    
    return pd.merge(compteurs, localisation_compteurs, on='id_compteur', how='inner')

def pistes_cyclables(geo_df_cycl):
    lats = []
    lons = []
    names = []

    for feature, name in zip(geo_df_cycl.geometry, geo_df_cycl.NOM_ARR_VILLE_DESC):
        if not isinstance(feature, shapely.geometry.linestring.LineString):
            continue
        
        linestrings = [feature]
        
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            names = np.append(names, [name]*len(y))
            lats = np.append(lats, None) 
            lons = np.append(lons, None)  
            names = np.append(names, None)  

    fig = px.line_mapbox(lat=lats, lon=lons, hover_name=names, 
                        mapbox_style='open-street-map', zoom=11)
    fig.update_traces(line=dict(color='rgba(18,87,25,0.6)'))
    fig.add_trace(go.Scattermapbox(mode='none', name='Pistes cyclables', 
                                   marker=dict(color='rgba(18,87,25,0.6)'), showlegend=True))
    
    return fig


def add_compteurs(fig: go.Figure, compteurs_dataframe):
    color_discrete_map = {
        '2019': 'red', 
        '2020': 'blue', 
        '2021': 'purple', 
        '2022': 'orange',
        '2023': 'green',
        '2024': 'yellow'
    }
    
    compteurs = px.scatter_mapbox(
        compteurs_dataframe,
        lat='latitude',
        lon='longitude',
        size='nb_passages',
        color='Annee_implante',
        color_discrete_map=color_discrete_map,
        labels={'color': 'Année d\'implantation'}
    )
    
    compteurs.update_traces(
        mode='markers',
        marker=dict(sizemin=6)
    )

    fig.add_traces(list(compteurs.select_traces()))

    fig.update_layout(legend_title_text='Légende')


def generate_viz3_figure(selected_year):
    geo_df_cycl = gpd.read_file('assets/data/reseau_cyclable.geojson')
    compteurs_dataframe = get_compteurs_dataframe(selected_year)

    fig = pistes_cyclables(geo_df_cycl)
    add_compteurs(fig, compteurs_dataframe)

    return fig
