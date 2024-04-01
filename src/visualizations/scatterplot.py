import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import hover_template


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

    # On met à jour les informations de la droite de moyenne
    x_info, x_unit = (
        "Pluie", "mm") if x_column == "Total Rain (mm)" else ("Neige", "cm")

    # On trace notre droite de points horizontale
    mean_trace = go.Scatter(x=x_values,
                            y=y_values,
                            mode='lines',
                            line=dict(color='#9E9E9E', dash='dash'),
                            showlegend=True,  # Mettre true pour obtenir la droite comme une légende
                            name=f"Moyenne des passages à 0 {x_unit}",
                            )

    mean_trace.update(hovertemplate=hover_template.get_mean_scatter_hover_template(mean_nb_passages_zero, x_info, x_unit),
                      hoverlabel=dict(bgcolor="#EDEDED", font=dict(color="#7E7E7E")))

    return mean_trace


'''

La fonction suivante permet de tracer les différents nuages de points.
On pourra l'utiliser ensuite directement pour choisir la variable à représenter.

'''


def get_scatterplot_figure(data, x_column, x_title, hover_template):
    # Appel de la fonction pour ajouter la trace de la moyenne dans le cas de neige ou pluie
    mean_trace = add_mean_trace(data, x_column)

    # Nuage de Points
    fig = px.scatter(data, x=x_column, y='nb_passages',
                     custom_data=[x_column, 'nb_passages', 'date'])
    fig.update_layout(
        xaxis_title=x_title,
        xaxis_tickangle=0,
        yaxis_title='Nombre de passages (milliers)',
        font=dict(size=12, color='black', family='Roboto'),
        xaxis=dict(showgrid=True, gridcolor='#E6E6E6'),
        yaxis=dict(showgrid=True, gridcolor='#E6E6E6'),
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor='white')
    )
    fig.update_traces(marker_color='#1f77b4', hovertemplate=hover_template)

    # Ajoute la trace de la moyenne si elle a été définie
    if mean_trace:
        fig.add_trace(mean_trace)

    return fig


'''

Chacune des fonctions suivantes permet d'obtenir le nuages de points
de la météo, de la neige et de la pluie.

'''

# Visualisation de la température


def get_temperature_figure(data):
    hover_template_temperature = hover_template.get_scatter_hover_template(
        'Température', '°C')
    return get_scatterplot_figure(data, 'Mean Temp (°C)', 'Température moyenne (°C)', hover_template_temperature)


# Visualisation de la neige
def get_snow_figure(data):
    hover_template_neige = hover_template.get_scatter_hover_template(
        'Quantité de neige', 'cm')
    return get_scatterplot_figure(data, 'Total Snow (cm)', 'Quantité de neige (cm)', hover_template_neige)


# Visualisation de la pluie
def get_rain_figure(data):
    hover_template_pluie = hover_template.get_scatter_hover_template(
        'Quantité de pluie ', 'mm')
    return get_scatterplot_figure(data, 'Total Rain (mm)', 'Quantité de pluie (mm)', hover_template_pluie)
