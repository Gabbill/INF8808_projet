# Inspired by : https://github.com/brunorosilva/plotly-calplot/

import numpy as np
import preprocess as preprocess
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from hover_template import heatmap_hover_template

YEARS = [2019, 2020, 2021, 2022, 2023]
WEEK_DAYS_NAMES = ['Lundi', 'Mardi', 'Mercredi',
                   'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
MONTH_POSITIONS = np.linspace(1.5, 50, 12)
MONTH_NAMES = {
    'January': 'janvier',
    'February': 'février',
    'March': 'mars',
    'April': 'avril',
    'May': 'mai',
    'June': 'juin',
    'July': 'juillet',
    'August': 'août',
    'September': 'septembre',
    'October': 'octobre',
    'November': 'novembre',
    'December': 'décembre'
}


def heatmap(df):
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

    fig_height = 150 * nb_years
    update_layout(fig, fig_height)

    return fig


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
            hoverinfo='text'
        )
    ]

    add_month_separators(year_heatmap, year_df, week_days, week_numbers)
    add_year_heatmap(fig, year_heatmap, year_index)


def get_hover_info(year_df, week_days):
    year_df['formatted_date'] = year_df['date'].dt.strftime(
        '%d %B %Y').apply(translate_date)

    return [heatmap_hover_template(
            WEEK_DAYS_NAMES[week_days[index % 7]],
            row['formatted_date'],
            row['nb_passages']
            ) for index, row in year_df.iterrows()]


def translate_date(date_string):
    for eng_month, fr_month in MONTH_NAMES.items():
        if eng_month in date_string:
            return date_string.replace(eng_month, fr_month)
    return date_string


def add_month_separators(year_heatmap, year_df, week_days, week_numbers):
    month_lines = dict(
        mode='lines',
        line=dict(color='#000000', width=2),
        hoverinfo='skip',
    )

    for date, dow, wkn in zip(year_df['date'], week_days, week_numbers):
        if date.day != 1:
            continue

        year_heatmap += [go.Scatter(x=[wkn - 0.5, wkn - 0.5],
                                    y=[dow - 0.5, 6.5], **month_lines)]
        if dow:
            year_heatmap += [
                go.Scatter(
                    x=[wkn - 0.5, wkn + 0.5], y=[dow - 0.5, dow - 0.5], **month_lines
                ),
                go.Scatter(x=[wkn + 0.5, wkn + 0.5],
                           y=[dow - 0.5, -0.5], **month_lines),
            ]


def add_year_heatmap(fig, year_heatmap, year_index):
    fig.add_traces(
        year_heatmap,
        rows=[(year_index + 1)] * len(year_heatmap),
        cols=[1] * len(year_heatmap)
    )


def add_color_scale(fig, min_value, max_value):
    fig.update_traces(
        zmin=min_value,
        zmax=max_value,
        selector=dict(type='heatmap'),
        showscale=True,
    )


def update_layout(fig, fig_height):
    french_months = [month.capitalize() for month in MONTH_NAMES.values()]
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
        font=dict(size=10, color='#757575'),
        plot_bgcolor=('#fff'),
        margin=dict(t=20, b=20),
        showlegend=False,
        height=fig_height
    )

    fig.update_layout(layout)
    fig.update_xaxes(layout['xaxis'])
    fig.update_yaxes(layout['yaxis'])
