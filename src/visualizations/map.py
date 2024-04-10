import plotly.express as px
import shapely.geometry
import numpy as np
import hover_template
from pandas import DataFrame
colors = ['red', 'blue', 'purple', 'orange', 'green', 'yellow']


def get_map(yearly_counters_count: DataFrame, montreal_bike_paths: tuple[list, list]):
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
        opacity=1,
        labels={'color': 'Année d\'implantation'},
        custom_data=['Annee_implante'],
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
    # Permet de garder le template de l'info-bulle pour chaque frame
    for frame in fig.frames:
        for data in frame.data:
            data.hovertemplate = hover_template.get_map_hover_template()
            data.hoverlabel = dict(
                bgcolor="white",
                bordercolor="black",
            )
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=10,
        mapbox_center={'lat': np.mean([lat for lat in yearly_counters_count["latitude"] if lat is not None]),
                       'lon': np.mean([lon for lon in yearly_counters_count["longitude"] if lon is not None])},
        showlegend=True,
        legend_title_text="Année d'implémentation des compteurs",
    )
    # Ajout des pistes cyclables
    fig.add_scattermapbox(lat=montreal_bike_paths[0], lon=montreal_bike_paths[1], mode='lines', line=dict(
        color='rgba(18,87,25,0.6)'), hoverinfo='skip', name='Pistes cyclables')
    return fig
