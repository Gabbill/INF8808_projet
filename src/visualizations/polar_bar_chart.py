import plotly.graph_objects as go
import hover_template


def create_seasonal_polar_chart(df, season):
    seasonal_data = df[df['season'] == season]

    fig = go.Figure()

    fig.add_trace(go.Barpolar(
        r=seasonal_data['nb_passages'],
        theta=seasonal_data['heure'],
        marker_color='#1f77b4',
        marker_line_color='grey',
        marker_line_width=1,
        opacity=1,
        hovertemplate=hover_template.get_polar_chart_hover_template()
    ))

    tickfont_settings = dict(size=12, color='black', family="Arial Bold")
    tickfont_settings_circle = dict(size=10, color='black', family="Arial Bold")


    max_val = seasonal_data['nb_passages'].max()
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_val + max_val * 0.1],
                gridcolor='grey',
                tickfont=tickfont_settings_circle 
            ),
            angularaxis=dict(
                tickmode='array',
                tickvals=[i + 0.5 for i in range(24)],
                ticktext=[str(i) + 'h' for i in range(24)],
                rotation=82.5,
                direction="counterclockwise",
                layer="above traces",
                gridcolor='grey',
                tickfont=tickfont_settings
            )
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(size=10, family='Roboto'),
        title=dict(
            text=f"Utilisation des pistes cyclables ({season})",
            font=dict(size=12),
        ),
        title_x=0.5,
    )

    return fig
