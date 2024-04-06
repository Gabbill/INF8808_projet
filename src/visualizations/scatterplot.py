import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from hover_template import get_mean_scatter_hover_template, get_scatter_hover_template


'''

Chacune des fonctions suivantes permet d'obtenir le nuages de points
de la température, de la neige et de la pluie.

'''


# Visualisation de la température
def get_temperature_figure(data):
    hover_template_temperature = get_scatter_hover_template(
        'Température', '°C')
    return get_scatterplot_figure(data, 'Mean Temp (°C)', 'Température moyenne (°C)', hover_template_temperature)


# Visualisation de la neige
def get_snow_figure(data):
    hover_template_neige = get_scatter_hover_template(
        'Quantité de neige', 'cm')
    return get_scatterplot_figure(data, 'Total Snow (cm)', 'Quantité de neige (cm)', hover_template_neige)


# Visualisation de la pluie
def get_rain_figure(data):
    hover_template_pluie = get_scatter_hover_template(
        'Quantité de pluie', 'mm')
    return get_scatterplot_figure(data, 'Total Rain (mm)', 'Quantité de pluie (mm)', hover_template_pluie)


'''

La fonction suivante permet de tracer les différents nuages de points.
On pourra l'utiliser ensuite directement pour choisir la variable à représenter.

'''


def get_scatterplot_figure(data, x_column, x_title, hover_template):
    # Trace de la moyenne dans le cas de neige ou pluie
    mean_trace = add_mean_trace(data, x_column)

    # Nuage de Points
    fig = px.scatter(data, x=x_column, y='nb_passages',
                     custom_data=['formatted_date_x'])

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title='Nombre de passages (milliers)',
        font=dict(size=12, color='black', family='Roboto'),
        xaxis=dict(showgrid=True, gridcolor='#E6E6E6'),
        yaxis=dict(showgrid=True, gridcolor='#E6E6E6'),
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor='white'),
        dragmode=False,

    )

    fig.update_traces(marker_color='#1f77b4', hovertemplate=hover_template)

    # Ajout de la trace de la moyenne si elle a été définie
    if mean_trace:
        fig.add_trace(mean_trace)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    return fig


'''

Dans le cas de graphique représentant la neige ou la pluie,
la fonction suivante trace un trait horizontale qui montre la
moyenne des passages quand la quantité des précipitations est égale à 0.

'''


def add_mean_trace(data, x_column):
    if x_column not in ["Total Rain (mm)", "Total Snow (cm)"]:
        return

    # Traitement des données et normalisation des valeurs de précipitations égales à 0 par leurs moyenne pour une meilleur lisibilité
    mean_nb_passages_zero = data.loc[data[x_column]
                                     == 0, 'nb_passages'].mean()
    data.loc[data[x_column] == 0, 'nb_passages'] = mean_nb_passages_zero
    x_values = np.linspace(data[x_column].min(), data[x_column].max(), 100)
    y_values = np.full_like(x_values, mean_nb_passages_zero)

    # Mise à jour des informations de la droite de moyenne
    x_info, x_unit = (
        "Pluie", "mm") if x_column == "Total Rain (mm)" else ("Neige", "cm")

    # Traçage de la droite de points horizontale
    return go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        line=dict(color='#9E9E9E', dash='dash'),
        showlegend=True,
        name=f"Moyenne des passages à 0 {x_unit}",
        hovertemplate=get_mean_scatter_hover_template(
            mean_nb_passages_zero, x_info, x_unit),
        hoverlabel=dict(bgcolor="#EDEDED",
                        font=dict(color="#7E7E7E")),
    )
