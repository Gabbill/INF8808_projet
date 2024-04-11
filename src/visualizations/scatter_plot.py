import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from hover_template import get_mean_scatter_hover_template, get_scatter_hover_template
from pandas import DataFrame


def get_temperature_figure(df: DataFrame):
    '''
    Scatter plot des passages selon la température
    '''
    hover_template_temperature = get_scatter_hover_template(
        'Température', '°C')
    return get_scatterplot_figure(df, 'Mean Temp (°C)', 'Température moyenne (°C)', hover_template_temperature)


def get_snow_figure(df: DataFrame):
    '''
    Scatter plot des passages selon la quantité de neige
    '''
    hover_template_neige = get_scatter_hover_template(
        'Quantité de neige', 'cm')
    return get_scatterplot_figure(df, 'Total Snow (cm)', 'Quantité de neige (cm)', hover_template_neige)


def get_rain_figure(df: DataFrame):
    '''
    Scatter plot des passages selon la quantité de pluie
    '''
    hover_template_pluie = get_scatter_hover_template(
        'Quantité de pluie', 'mm')
    return get_scatterplot_figure(df, 'Total Rain (mm)', 'Quantité de pluie (mm)', hover_template_pluie)


def get_scatterplot_figure(df: DataFrame, col: str, xaxis_title: str, hover_template: str):
    '''
    Tracer les différents nuages de points selon une variable météorologique
    '''
    mean_trace = None

    # Trace de la moyenne dans le cas de neige ou pluie
    if col in ['Total Rain (mm)', 'Total Snow (cm)']:
        mean_trace = add_mean_trace(df, col)
        df = df[df[col] != 0]

    # Nuage de Points
    fig = px.scatter(df, x=col, y='nb_passages',
                     custom_data=['formatted_date_x'])

    axis_layout = dict(
        showgrid=True,
        gridcolor='#E6E6E6',
        zerolinecolor='#E6E6E6'
    )

    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title='Nombre de passages',
        font=dict(size=12, color='black', family='Roboto'),
        xaxis=axis_layout,
        yaxis=axis_layout,
        plot_bgcolor='white',
        hoverlabel=dict(bgcolor='white'),
    )

    fig.update_traces(marker_color='#1f77b4', hovertemplate=hover_template)

    # Ajout de la trace de la moyenne si elle a été définie
    if mean_trace:
        fig.add_trace(mean_trace)
        fig.update_layout(legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ))

    return fig


def add_mean_trace(df: DataFrame, col: str):
    '''
    Dans le cas de graphique représentant la neige ou la pluie,
    la fonction trace un trait horizontale qui montre la
    moyenne des passages lorsque la quantité des précipitations est égale à 0.
    '''
    # Traitement des données et normalisation des valeurs de précipitations égales à 0 par leurs moyenne pour une meilleur lisibilité
    mean_nb_passages_zero = int(df.loc[df[col] == 0, 'nb_passages'].mean())

    df.loc[df[col] == 0, 'nb_passages'] = mean_nb_passages_zero
    x_values = np.linspace(df[col].min(), df[col].max(), 100)
    y_values = np.full_like(x_values, mean_nb_passages_zero)

    # Mise à jour des informations de la droite de moyenne
    x_info, x_unit = (
        'Pluie', 'mm') if col == 'Total Rain (mm)' else ('Neige', 'cm')

    # Traçage de la droite de points horizontale
    return go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        line=dict(color='black', dash='dash'),
        showlegend=True,
        name=f'Moyenne des passages à 0 {x_unit}',
        hovertemplate=get_mean_scatter_hover_template(
            mean_nb_passages_zero, x_info, x_unit),
        hoverlabel=dict(bgcolor='#EDEDED',
                        font=dict(color='#7E7E7E')),
    )
