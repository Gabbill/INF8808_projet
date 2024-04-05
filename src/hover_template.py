'''
La fonction suivante fait référence à l'info-bulle de la HeatMap.
'''


def heatmap_hover_template(week_day, date, bike_count):
    hover_template = f'<b style="color: #E55037">Date : </b><span>{week_day} le {date}</span><br>'
    hover_template += f'<b style="color: #E55037">Nombre de passages : </b><span>{bike_count}</span>'
    return hover_template


'''
La fonction suivante fait référence à l'info-bulle des nuages de points.
'''


def get_scatter_hover_template(label, x_unit):
    hover_template = "<b style ='color: #1f77b4;'>Date : </b><span >%{customdata}</span><br>"
    hover_template += "<b style ='color: #1f77b4;'>Nombre de passages : </b><span>%{y:.0f}</span><br>"
    hover_template += f"<b style='color: #1f77b4;'>{label} : </b>" + \
        "<span>%{x}" + f" {x_unit}</span><br>"
    return hover_template


'''
La fonction suivante fait référence à l'info-bulle de la moyenne des nuages de points.
'''


def get_mean_scatter_hover_template(mean_nb_passages_zero, x_info, x_unit):
    mean_hover = f"<b style='background-color: #d3d3d3;'>Moyenne de passages :</b><span> {mean_nb_passages_zero:.0f} </span><br>"
    mean_hover += f"<b style='background-color: #d3d3d3;'>Quantité de {x_info.lower()} :</b><span> 0</span> <span>{x_unit}</span>"
    mean_hover += '<extra></extra>'
    return mean_hover
