# Inspired by : https://github.com/brunorosilva/plotly-calplot/

import pandas as pd
import numpy as np
import preprocess
import plotly.graph_objects as go

from plotly.subplots import make_subplots


def heatmap(df):
    years = [2019, 2020, 2021, 2022, 2023]
    years_as_strings = [str(year) for year in years]
    nb_years = len(years)
    nb_columns = 1
    min_nb_bike_rides = df['nb_passages'].min()
    max_nb_bike_rides = df['nb_passages'].max()

    fig_height = 150 * nb_years

    fig = make_subplots(
        rows=nb_years,
        cols=nb_columns,
        subplot_titles=years_as_strings,
        vertical_spacing=0.08,
    )

    for i, year in enumerate(years):
        year_df = df.loc[df['date'].dt.year == year]
        # print(year_df)
        # fill_empty_with_zeros si ça marche pas
        yearly_heatmap(year_df, fig, fig_height, i)

    fig = apply_general_colorscaling(
        fig, min_nb_bike_rides, max_nb_bike_rides)
    fig = showscale_of_heatmaps(fig)

    return fig


def yearly_heatmap(yearly_df, fig, fig_height, row):
    month_names = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                   'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

    month_positions, week_days, week_numbers = get_date_coordinates(yearly_df)

    yearly_heatmap = [
        go.Heatmap(
            x=week_numbers,
            y=week_days,
            z=yearly_df['nb_passages'],
            xgap=1,
            ygap=1,
            showscale=False,
            colorscale='orrd',
        )
    ]

    month_lines = dict(
        mode='lines',
        line=dict(color='#000000', width=2),
        hoverinfo='skip',
    )

    for date, dow, wkn in zip(yearly_df['date'], week_days, week_numbers):
        if date.day == 1:
            yearly_heatmap += [go.Scatter(x=[wkn - 0.5, wkn - 0.5],
                                          y=[dow - 0.5, 6.5], **month_lines)]
            if dow:
                yearly_heatmap += [
                    go.Scatter(
                        x=[wkn - 0.5, wkn + 0.5], y=[dow - 0.5, dow - 0.5], **month_lines
                    ),
                    go.Scatter(x=[wkn + 0.5, wkn + 0.5],
                               y=[dow - 0.5, -0.5], **month_lines),
                ]

    layout = get_yearly_layout(month_names, month_positions)
    fig = update_plot_with_layout(fig, yearly_heatmap, layout, fig_height, row)

    return fig


def get_date_coordinates(df):
    # nb_days_each_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # if df.loc[df['date'].dt.month == 2, 'date'].max().day == 29:
    #     nb_days_each_month[1] = 29
    month_positions = np.linspace(1.5, 50, 12)
    week_days = [i.weekday() for i in df['date']]
    week_numbers = df['date'].dt.strftime('%W').astype(int).tolist()

    return month_positions, week_days, week_numbers


def get_yearly_layout(month_names, month_positions):
    return go.Layout(
        xaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            tickmode='array',
            ticktext=month_names,
            tickvals=month_positions,
        ),
        yaxis=dict(
            showline=False,
            showgrid=False,
            zeroline=False,
            tickmode='array',
            ticktext=['Lundi', 'Mardi', 'Mercredi',
                      'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            autorange='reversed',
        ),
        font=dict(size=10, color='#9e9e9e'),
        plot_bgcolor=('#fff'),
        margin=dict(t=20, b=20),
        showlegend=False,
    )


def update_plot_with_layout(fig, yearly_heatmap, layout, fig_height, row):
    fig.update_layout(layout)
    fig.update_xaxes(layout["xaxis"])
    fig.update_yaxes(layout["yaxis"])
    fig.update_layout(height=fig_height)

    rows = [(row + 1)] * len(yearly_heatmap)
    cols = [1] * len(yearly_heatmap)

    fig.add_traces(yearly_heatmap, rows=rows, cols=cols)
    return fig


def apply_general_colorscaling(fig, min_value, max_value):
    return fig.update_traces(
        selector=dict(type='heatmap'), zmax=max_value, zmin=min_value
    )


def showscale_of_heatmaps(fig):
    return fig.update_traces(
        showscale=True,
        selector=dict(type='heatmap'),
    )


# TODO :  À ENLEVER
bike_counts_data_list = preprocess.load_bike_counts_data_list()
bike_counts_df = preprocess.get_bike_counts_df(bike_counts_data_list)

daily_bike_count = preprocess.get_daily_bike_count(bike_counts_df)

fig = heatmap(daily_bike_count)
fig.show()
