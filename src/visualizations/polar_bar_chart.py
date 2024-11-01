import plotly.graph_objects as go

from hover_template import get_polar_chart_hover_template
from pandas import DataFrame


def get_seasonal_polar_chart(df: DataFrame, season: str):
    '''
    Obtention d'un polar bar chart représentant l'achalandage des compteurs à vélo
    par heure au cours des quatre saisons à Montréal.
    '''
    # Récupération des données liées à la saison
    seasonal_data = df[df['season'] == season]

    fig = go.Figure()

    # Polar bar chart
    fig.add_trace(go.Barpolar(
        r=seasonal_data['nb_passages'],
        theta=seasonal_data['heure'],
        marker_color='#1f77b4',
        marker_line_color='#80878C',
        marker_line_width=1,
        opacity=1,
        hovertemplate=get_polar_chart_hover_template()
    ))

    # Calcul de la valeur maximal des passages pour définir l'intervalle radiale
    max_val = seasonal_data['nb_passages'].max()

    # Configuration de la mise en page du graphique
    fig.update_layout(
        # Paramètres des axes radiale et angulaire
        polar=dict(
            radialaxis=dict(
                range=[0, max_val + max_val * 0.1],
                gridcolor='#B6BFC7',
                tickfont=dict(size=10, color='black', family='Roboto'),
                linecolor='#B6BFC7',
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=[i+0.5 for i in range(24)],
                ticktext=[str((i + 1) % 24) + 'h' for i in range(24)],
                rotation=82.5,
                direction='clockwise',
                layer='above traces',
                gridcolor='#B6BFC7',
                linecolor='#B6BFC7',
                tickfont=dict(size=12, color='black', family='Roboto')
            )
        ),
        # Options des paramètres de marges, polices et titre du graphique
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(size=10, family='Roboto'),
        title=dict(
            text=f'Utilisation des pistes cyclables ({season})',
            font=dict(size=15),
        ),
        title_x=0.5,
        dragmode=False,
        hoverlabel=dict(bgcolor='white')
    )

    return fig
