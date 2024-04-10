import plotly.express as px
import shapely.geometry
import plotly.graph_objects as go
import numpy as np
import hover_template
from pandas import DataFrame
colors = ['#E55137', '#1F77B4', '#D247C4', '#EECA48', '#31C0B7', '#37C031']


def get_map(yearly_counters_count: DataFrame, montreal_bike_paths: tuple[list, list]):
    yearly_counters_count['passages_per_day'] = yearly_counters_count['nb_passages'] / 365
    years = yearly_counters_count['Année'].unique()
    color_discrete_map = {
        str(years[i]): colors[i] for i in range(len(years))
    }
    # Ajout des compteurs
    fig = px.scatter_mapbox(
        yearly_counters_count,
        animation_frame='Année',
        animation_group='Annee_implante',
        lat='latitude',
        lon='longitude',
        size='nb_passages',
        color='Annee_implante',
        color_discrete_map=color_discrete_map,
        opacity=0.85,
        labels={'color': 'Année d\'implantation'},
        custom_data=['Annee_implante', 'passages_per_day'],
    )
    fig.update_traces(
        mode='markers',
        marker=dict(sizemin=6),
        hovertemplate=hover_template.get_map_hover_template(),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="black",
        )
    )
    bike_paths_trace = go.Scattermapbox(lat=montreal_bike_paths[0], lon=montreal_bike_paths[1], mode='lines', line=dict(
        color='rgba(18,87,25,0.6)'), hoverinfo='skip', name='Pistes cyclables')
    # Permet de garder le template de l'info-bulle pour chaque frame
    for frame in fig.frames:
        frame.data += (bike_paths_trace,)
        for data in frame.data:
            # ignore bike paths for hover template
            if data.name == 'Pistes cyclables':
                continue
            data.hovertemplate = hover_template.get_map_hover_template()
            data.hoverlabel = dict(
                bgcolor="white",
                bordercolor="black",
            )
        frame.data = [frame.data[-1]] + list(frame.data[:-1])
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=10,
        mapbox_center={'lat': np.mean([lat for lat in yearly_counters_count["latitude"] if lat is not None]),
                       'lon': np.mean([lon for lon in yearly_counters_count["longitude"] if lon is not None])},
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            title_text="Année d'implémentation des compteurs",
        )
    )
    # Ajout des pistes cyclables
    fig.add_trace(bike_paths_trace)

    # Réorganiser les traces pour que les pistes cyclables soient en dessous
    fig.data = [fig.data[-1]] + list(fig.data[:-1])

    return fig
