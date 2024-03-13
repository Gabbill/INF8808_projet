import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import contextily as ctx


localisation_data = pd.read_csv('assets/localisation_des_compteurs_velo.csv')
gdf = gpd.GeoDataFrame(localisation_data, geometry=gpd.points_from_xy(
    localisation_data.Longitude, localisation_data.Latitude), crs="EPSG:4326")
gdf = gdf.to_crs(epsg=3857)  # Convertir en Web Mercator pour contextily

fig, ax = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(bottom=0.2)

AXE_COLOR = 'lightgoldenrodyellow'
ax_slider = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=AXE_COLOR)
slider = Slider(ax_slider, 'Année', 2010, 2023, valinit=2019, valstep=1)


# def update(val):

#     ax.clear()
#     annee = int(slider.val)
#     data_annee = gdf[gdf['Annee_implante'] == annee]
#     data_annee_active = data_annee[data_annee['Statut'] == 'Actif']
#     data_annee_inactive = data_annee[data_annee['Statut'] != 'Actif']

#     data_annee_active.plot(ax=ax, color='green', marker='o', label='Actif')
#     data_annee_inactive.plot(
#         ax=ax, color='red', marker='x', label='Inactif/En maintenance')
#     ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
#     ax.set_title(f'Compteurs de vélo à Montréal en {annee}')
#     ax.axis('off')  # Désactiver l'affichage des axes
def update(year):

    ax.clear()
    # annee = int(slider.val)
    year_df = pd.read_csv('assets/comptage_velo_' + str(year) + '.csv')
    nb_passages_df = year_df[["id_compteur", "nb_passages"]].groupby(
        "id_compteur").sum().reset_index()
    passages_max = nb_passages_df["nb_passages"].max()
    passages_min = nb_passages_df["nb_passages"].min()
    comteurs_actifs = gdf[gdf['Statut'] == "Actif"]
    comteurs_actifs = comteurs_actifs[comteurs_actifs['Annee_implante'] <= year]
    comteurs_actifs = comteurs_actifs.merge(nb_passages_df[[
                                            'id_compteur', 'nb_passages']], left_on='ID', right_on='id_compteur', how='left')
    comteurs_inactifs = gdf[gdf['Statut'] != "Actif"]
    comteurs_inactifs = comteurs_inactifs[comteurs_inactifs['Annee_implante'] <= year]

    comteurs_actifs.plot(
        ax=ax, color='green', marker='o', label='Actif', markersize=comteurs_actifs["nb_passages"]*100/passages_max)
    comteurs_inactifs.plot(
        ax=ax, color='red', marker='x', label='Inactif/En maintenance')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_title(f'Compteurs de vélo à Montréal en {year}')
    ax.axis('off')  # Désactiver l'affichage des axes

    ax.legend()


update(2019)  # Initialiser avec l'année 2019
slider.on_changed(update)
plt.show()
