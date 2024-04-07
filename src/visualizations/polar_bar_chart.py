import plotly.graph_objects as go
import hover_template


def get_seasonal_polar_chart(df, season):
    seasonal_data = df[df['season'] == season]

    fig = go.Figure()
    fig.add_trace(go.Barpolar(
        r=seasonal_data['nb_passages'],
        theta=seasonal_data['heure'],
        marker_color='#1f77b4',
        marker_line_color='#80878C',
        marker_line_width=1,
        opacity=1,
        hovertemplate=hover_template.get_polar_chart_hover_template()
    ))

    max_val = seasonal_data['nb_passages'].max()

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, max_val + max_val * 0.1],
                gridcolor='#B6BFC7',
                tickfont=dict(size=10, color='black', family='Roboto')
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
