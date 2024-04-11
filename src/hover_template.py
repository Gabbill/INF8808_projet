'''
La fonction suivante fait référence à l'info-bulle de la Heatmap.
'''


def heatmap_hover_template(week_day: str, date: str, bike_count: int):
    hover_template = f'<b style="color: #E55037">Date : </b><span>{week_day} le {date}</span><br>'
    hover_template += f'<b style="color: #E55037">Nombre de passages : </b><span>{bike_count}</span>'
    return hover_template


'''
La fonction suivante fait référence à l'info-bulle de l'horloge.
'''


def get_polar_chart_hover_template():
    hover_template = "<b style='color: #1f77b4;'>Heure : </b><span>%{theta}</span><br>"
    hover_template += "<b style='color: #1f77b4;'>Nombre de passages : </b><span>%{r:.0f}</span>"
    hover_template += "<extra></extra>"
    return hover_template


'''
La fonction suivante fait référence à l'info-bulle des compteurs de la carte.
'''


def get_map_counters_hover_template():
    hover_template = "<b style='color: #ffffff;'>Année d'implantation : </b><span style='color: #ffffff;>%{customdata[0]}</span><br>"
    hover_template += "<b style='color: #ffffff;'>Nombre de passages par jour : </b><span style='color: #ffffff;>%{customdata[1]:.0f}</span><br>"
    hover_template += "<extra></extra>"
    return hover_template


'''
La fonction suivante fait référence à l'info-bulle des pistes cyclables de la carte.
'''


def get_map_bike_paths_hover_template():
    hover_template = "<b style='color: rgba(18,87,25,0.8);'>Arrondissement : </b><span>%{customdata}</span>"
    hover_template += "<extra></extra>"
    return hover_template


'''
La fonction suivante fait référence à l'info-bulle de la moyenne des nuages de points.
'''


def get_mean_scatter_hover_template(mean_nb_passages_zero: float, x_info: str, x_unit: str):
    mean_hover = f"<b style='background-color: #d3d3d3;'>Moyenne de passages :</b><span> {mean_nb_passages_zero:.0f} </span><br>"
    mean_hover += f"<b style='background-color: #d3d3d3;'>Quantité de {x_info.lower()} :</b><span> 0</span> <span>{x_unit}</span>"
    mean_hover += '<extra></extra>'
    return mean_hover


'''
La fonction suivante fait référence à l'info-bulle des nuages de points.
'''


def get_scatter_hover_template(label: str, x_unit: str):
    hover_template = "<b style ='color: #1f77b4;'>Date : </b><span >%{customdata}</span><br>"
    hover_template += "<b style ='color: #1f77b4;'>Nombre de passages : </b><span>%{y:.0f}</span><br>"
    hover_template += f"<b style='color: #1f77b4;'>{label} : </b>" + \
        "<span>%{x}" + f" {x_unit}</span><br>"
    return hover_template
