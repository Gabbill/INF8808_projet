import plotly.express as px
import geopandas as gpd
import shapely.geometry
import numpy as np
import pandas as pd
import wget
import plotly.graph_objects as go

geo_df_cycl = gpd.read_file("assets/reseau_cyclable.geojson")
localisation_data = pd.read_csv('assets/localisation_des_compteurs_velo.csv')
gdf = gpd.GeoDataFrame(localisation_data, geometry=gpd.points_from_xy(
    localisation_data.Longitude, localisation_data.Latitude), crs="EPSG:4326")
gdf = gdf.to_crs(epsg=3857)  # Convertir en Web Mercator pour contextily
lats = []
lons = []
names = []

for feature, name in zip(geo_df_cycl.geometry, geo_df_cycl.ID_CYCL):
    if isinstance(feature, shapely.geometry.linestring.LineString):
        linestrings = [feature]
    elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
        linestrings = feature.geoms
    else:
        continue
    for linestring in linestrings:
        x, y = linestring.xy
        lats = np.append(lats, y)
        lons = np.append(lons, x)
        names = np.append(names, [name]*len(y))
        lats = np.append(lats, None)
        lons = np.append(lons, None)
        names = np.append(names, None)

print("before lines")

fig = px.line_mapbox(lat=lats, lon=lons, hover_name=names,
                     mapbox_style="open-street-map", zoom=11)
print("before scatter")

fig.add_scattermapbox(lat=gdf.Latitude, lon=gdf.Longitude, hoverinfo='text',
                      text=gdf.Nom, mode='markers', marker=dict(size=8, color='red'))
fig.add_densitymapbox(lat=gdf.Latitude, lon=gdf.Longitude, radius=40)

fig.show()
