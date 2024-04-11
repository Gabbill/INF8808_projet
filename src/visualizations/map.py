import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from pandas import DataFrame
from hover_template import get_map_counters_hover_template, get_map_bike_paths_hover_template

COLORS = ['#E55137', '#1F77B4', '#D247C4', '#EECA48', '#31C0B7', '#37C031']


def get_map(df: DataFrame, montreal_bike_paths: tuple[list, list, list]):
    '''
    Obtention de la carte avec les compteurs à vélo ainsi que les pistes cyclables
    de 2019 à 2023
    '''
    fig = add_bike_counters(df)
    fig = add_bike_paths(fig, montreal_bike_paths)
    return fig


def add_bike_counters(df: DataFrame):
    '''
    Ajout des compteurs à vélo sur la carte
    '''
    years = df['Année'].unique()
    color_discrete_map = {
        str(years[i]): COLORS[i] for i in range(len(years))
    }

    fig = px.scatter_mapbox(
        df,
        animation_frame='Année',
        animation_group='Annee_implante',
        lat='latitude',
        lon='longitude',
        size='nb_passages',
        color='Annee_implante',
        color_discrete_map=color_discrete_map,
        opacity=0.85,
        labels=dict(color="Année d'implantation"),
        custom_data=['Annee_implante', 'passages_par_jour'],
    )

    fig.update_traces(
        mode='markers',
        marker=dict(sizemin=6),
        hovertemplate=get_map_counters_hover_template(),
    )

    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=10,
        mapbox_center={'lat': np.mean([lat for lat in df['latitude'] if lat is not None]),
                       'lon': np.mean([lon for lon in df['longitude'] if lon is not None])},
        showlegend=True,
        legend=dict(
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01,
            title_text="Année d'implémentation des compteurs",
        )
    )

    return fig


def add_bike_paths(fig: go.Figure, montreal_bike_paths: tuple[list, list]):
    '''
    Ajout des pistes cyclables sur la carte
    '''
    bike_paths_trace = go.Scattermapbox(
        lat=montreal_bike_paths[0],
        lon=montreal_bike_paths[1],
        mode='lines',
        line=dict(color='rgba(18,87,25,0.6)'),
        hovertemplate=get_map_bike_paths_hover_template(),
        hoverlabel=dict(
            bgcolor='white',
            bordercolor='black',
        ),
        name='Pistes cyclables',
        customdata=montreal_bike_paths[2]
    )

    fig.add_trace(bike_paths_trace)
    update_animation_hover_template(fig.frames, bike_paths_trace)

    # Réorganisation des traces pour que les pistes cyclables soient en dessous
    fig.data = [fig.data[-1]] + list(fig.data[:-1])

    # Modification du préfixe du slider
    fig['layout']['sliders'][0]['currentvalue']['prefix'] = 'Année affichée : '

    return fig


def update_animation_hover_template(frames: tuple[go.Frame], bike_paths_trace: go.Scattermapbox):
    '''
    Définit l'info-bulle pour chaque frame de l'animation
    '''
    for frame in frames:
        frame.data += (bike_paths_trace,)
        for data in frame.data:
            if data.name == 'Pistes cyclables':
                data.hovertemplate = get_map_bike_paths_hover_template()
            else:
                data.hovertemplate = get_map_counters_hover_template()

        frame.data = [frame.data[-1]] + list(frame.data[:-1])
