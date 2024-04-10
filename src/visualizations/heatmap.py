# Inspired by : https://github.com/brunorosilva/plotly-calplot/

import numpy as np
import plotly.graph_objects as go
import utils

from plotly.subplots import make_subplots
from hover_template import heatmap_hover_template


# Définition des constantes utilisées
YEARS = [2019, 2020, 2021, 2022, 2023]
WEEK_DAYS_NAMES = ['Lundi', 'Mardi', 'Mercredi',
                   'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
MONTH_POSITIONS = np.linspace(1.5, 50, 12)


'''

La fonction suivante permet de créer la Heatmap de 2019 à 2023 

'''


def get_heatmap(df):
    years_as_strings = [str(year) for year in YEARS]
    nb_years = len(YEARS)

    fig = make_subplots(
        rows=nb_years,
        cols=1,
        subplot_titles=years_as_strings,
        vertical_spacing=0.08,
    )

    for year_index, year in enumerate(YEARS):
        year_df = df.loc[df['date'].dt.year == year].reset_index()
        year_heatmap(year_df, fig, year_index)

    add_color_scale(fig, df['nb_passages'].min(), df['nb_passages'].max())
    update_layout(fig, nb_years)

    return fig


'''

Les fonctions suivantes permettent de générer les données nécessaires pour heatmap associée à une année.
On pourra alors ajouter les séparateurs de mois, les info-bulles ainsi que l'échelle de couleur.

'''


# Création d'une heatmap pour chaque année donnée
def year_heatmap(year_df, fig, year_index):
    week_days = [date.weekday() for date in year_df['date']]
    week_numbers = year_df['date'].dt.strftime('%W').astype(int).tolist()

    year_heatmap = [
        go.Heatmap(
            x=week_numbers,
            y=week_days,
            z=year_df['nb_passages'],
            xgap=1,
            ygap=1,
            showscale=False,
            colorscale='orrd',
            hovertext=get_hover_info(year_df, week_days),
            hoverinfo='text',
            hoverlabel=dict(bgcolor='white')
        )
    ]

    add_month_separators(year_heatmap, year_df, week_days, week_numbers)
    add_year_heatmap(fig, year_heatmap, year_index)


# Info-bulles de chaque jour de l'année
def get_hover_info(year_df, week_days):
    return [heatmap_hover_template(
            WEEK_DAYS_NAMES[week_days[index % 7]],
            row['formatted_date'],
            row['nb_passages']
            ) for index, row in year_df.iterrows()]


# Ajout de séparateurs de mois dans le graphique
def add_month_separators(year_heatmap, year_df, week_days, week_numbers):
    month_lines = dict(
        mode='lines',
        line=dict(color='#000000', width=2),
        hoverinfo='skip',
    )

    for date, week_day, week_number in zip(year_df['date'], week_days, week_numbers):
        if date.day != 1:
            continue

        year_heatmap += [go.Scatter(x=[week_number - 0.5, week_number - 0.5],
                                    y=[week_day - 0.5, 6.5], **month_lines)]
        if week_day:
            year_heatmap += [
                go.Scatter(
                    x=[week_number - 0.5, week_number + 0.5], y=[week_day - 0.5, week_day - 0.5], **month_lines
                ),
                go.Scatter(x=[week_number + 0.5, week_number + 0.5],
                           y=[week_day - 0.5, -0.5], **month_lines),
            ]


# Ajout d'une heatmap annuelle à la figure
def add_year_heatmap(fig, year_heatmap, year_index):
    fig.add_traces(
        year_heatmap,
        rows=[(year_index + 1)] * len(year_heatmap),
        cols=[1] * len(year_heatmap)
    )


# Définition de l'échelle de couleur de la heatmap
def add_color_scale(fig, min_value, max_value):
    fig.update_traces(
        zmin=min_value,
        zmax=max_value,
        selector=dict(type='heatmap'),
        showscale=True,
    )


# Mise à jour de la mise en page de la figure
def update_layout(fig, nb_years):
    fig_height = nb_years * 150
    french_months = [month.capitalize()
                     for month in utils.MONTH_NAMES.values()]

    layout = go.Layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            tickmode='array',
            ticktext=french_months,
            tickvals=MONTH_POSITIONS,
            fixedrange=True,
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            tickmode='array',
            ticktext=WEEK_DAYS_NAMES,
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            autorange='reversed',
            fixedrange=True,
        ),
        font=dict(size=9, color='#757575'),
        plot_bgcolor=('#fff'),
        margin=dict(t=20, b=20),
        showlegend=False,
        height=fig_height
    )

    fig.update_layout(layout)
    fig.update_xaxes(layout['xaxis'])
    fig.update_yaxes(layout['yaxis'])
