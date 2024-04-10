import plotly.express as px
import shapely.geometry
import numpy as np

colors = ['red', 'blue', 'purple', 'orange', 'green', 'yellow']


def create_viz3(yearly_counters_count, montreal_bike_paths):
    years = yearly_counters_count['Année'].unique()
    color_discrete_map = {
        str(years[i]): colors[i] for i in range(len(years))
    }
    lats = []
    lons = []
    names = []
    for feature, name in zip(montreal_bike_paths.geometry, montreal_bike_paths.NOM_ARR_VILLE_DESC):
        if not isinstance(feature, shapely.geometry.linestring.LineString):
            continue

        linestrings = [feature]

        for linestring in linestrings:
            x, y = linestring.xy
            # None to create a gap in the line
            lats.extend(y.tolist() + [None])
            lons.extend(x.tolist() + [None])
            names.extend([name]*len(y) + [None])
    # For earch year, all id_counter should be represented with its corresponding "Annee_implante"

    for compteur_id in yearly_counters_count['id_compteur'].unique():
        compteurs = yearly_counters_count[yearly_counters_count['id_compteur'] == compteur_id]
        for year in years:
            if year not in compteurs['Année'].values:
                yearly_counters_count.loc[len(yearly_counters_count)] = [compteur_id, compteurs['longitude'].values[0],
                                                                         compteurs['latitude'].values[0], year, 0, compteurs['Annee_implante'].values[0]]
    compteurs = px.scatter_mapbox(
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
        custom_data=['Annee_implante']
    )
    compteurs.update_traces(
        mode='markers',
        marker=dict(sizemin=6),
        hovertemplate='<b>Année d\'implantation: %{customdata[0]}</b><br>Nombre de passages: %{marker.size}<br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
    )
    compteurs.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=10,
        mapbox_center={'lat': np.mean([lat for lat in yearly_counters_count["latitude"] if lat is not None]),
                       'lon': np.mean([lon for lon in yearly_counters_count["longitude"] if lon is not None])},
        showlegend=True,
        legend_title_text="Année d'implémentation des compteurs",
    )
    compteurs.add_scattermapbox(lat=lats, lon=lons, mode='lines', line=dict(
        color='rgba(18,87,25,0.6)'), hoverinfo='skip', name='Pistes cyclables')
    return compteurs
