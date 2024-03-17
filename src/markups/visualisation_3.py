import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import shapely.geometry
import numpy as np
import pandas as pd


def get_compteurs_dataframe():
    list_compteurs = [pd.read_csv(f'../../assets/comptage_velo_{year}.csv') for year in range(2019, 2023)]
    list_compteurs = [compteurs.groupby(['id_compteur', 'longitude', 'latitude'])['nb_passages'].sum().reset_index() for compteurs in list_compteurs]
    df_compteurs = pd.concat(list_compteurs, ignore_index=True)
    
    localisation_compteurs = localisation_data[['ID', 'Annee_implante']].copy()
    localisation_compteurs.rename(columns={'ID': 'id_compteur'}, inplace=True)
    localisation_compteurs.loc[localisation_compteurs['Annee_implante'] < 2019, 'Annee_implante'] = 2019
    localisation_compteurs['Annee_implante'] = localisation_compteurs['Annee_implante'].astype(str)
    
    return pd.merge(df_compteurs, localisation_compteurs, on='id_compteur', how='inner')


def pistes_cyclables():
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
    
    return fig
    

def add_compteurs_2019(fig: go.Figure):
    compteurs = px.scatter_mapbox(
        compteurs_dataframe,
        lat='latitude',
        lon='longitude',
        size='nb_passages',
        color='Annee_implante',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    
    compteurs.update_traces(
        mode='markers', 
        marker=dict(sizemin=6)
    )

    fig.add_traces(list(compteurs.select_traces()))
    

geo_df_cycl = gpd.read_file("../../assets/reseau_cyclable.geojson")
localisation_data = pd.read_csv('../../assets/localisation_des_compteurs_velo.csv')
compteurs_dataframe = get_compteurs_dataframe()

fig = pistes_cyclables()
add_compteurs_2019(fig)

fig.show()