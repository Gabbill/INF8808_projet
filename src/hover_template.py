
'''
La fonction suivante fait référence à l'info-bulle de la HeatMap.
'''


def heatmap_hover_template(week_day, date, bike_count):
    return f'<b>{week_day} le {date}</b><br><span>{bike_count} passages</span>'


'''
La fonction suivante fait référence à l'info-bulle des nuages de points.
'''


def get_scatter_hover_template(label, x_unit):
    hover_label = "<b style ='color: #1f77b4;'> Date :</b><span > %{customdata[2]}</span><br>"
    hover_label += "<b style ='color: #1f77b4;'> Nombre de Passages :</b><span > %{customdata[1]:.0f}</span><br>"
    hover_label += f"<b style='color: #1f77b4;'> {label} :</b>" + \
        "<span > %{customdata[0]}</span>" + f"</span> {x_unit}</span><br>"
    return hover_label


'''
La fonction suivante fait référence à l'info-bulle de la moyenne des nuages de points.
'''


def get_mean_scatter_hover_template(mean_nb_passages_zero, x_info, x_unit):
    mean_hover = f"<b style='background-color: #d3d3d3;'> Moyenne de Passages :</b><span> {mean_nb_passages_zero:.0f} </span><br>"
    mean_hover += f"<b style='background-color: #d3d3d3;'> Quantité de {x_info}:</b><span> 0</span> <span>{x_unit}</span>"
    mean_hover += '<extra></extra>'
    return mean_hover
