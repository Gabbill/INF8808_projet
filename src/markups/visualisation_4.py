import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_dataframe():
    list_compteurs = [pd.read_csv(f'assets/comptage_velo_{year}.csv') for year in range(2019, 2025)]
    list_climate = [pd.read_csv(f'assets/en_climate_daily_QC_7025251_{year}_P1D.csv')  for year in range(2019, 2025)]

    # Compteurs communs aux années
    df_id_compteurs = [set(df['id_compteur'].unique()) for df in list_compteurs]
    common_id = set.intersection(*df_id_compteurs)

    # Regrouper les données des compteurs en un dataframe
    df_compteurs = pd.concat(list_compteurs, ignore_index=True)
    
    # Conserver seulement les données des compteurs communs et regrouper les données
    # d'une journée en une seule donnée
    df_compteurs = df_compteurs[df_compteurs['id_compteur'].isin(common_id)]
    df_compteurs = df_compteurs.groupby('date')['nb_passages'].sum().reset_index()

    # Regrouper les données de la météo en un dataframe
    df_climat = pd.concat(list_climate, ignore_index=True)[['Date/Time', 'Mean Temp (°C)', 'Total Rain (mm)', 'Total Snow (cm)']]
    df_climat.rename(columns={'Date/Time': 'date'}, inplace=True)
    
    return pd.merge(df_compteurs, df_climat, on='date', how='inner')


def temperature():
    fig = px.scatter(df, x='Mean Temp (°C)', y='nb_passages', hover_name='date')
    fig.update_layout(
        xaxis_title='Température moyenne (°C)',
        yaxis_title='Nombre de passages (milliers)'
    )
    fig.show()
    

def neige_ou_pluie(dataframe, is_rain=True):
    column_name = 'Total Rain (mm)'
    if not is_rain:
        column_name = 'Total Snow (cm)'

    mean_nb_passages_zero_rain = dataframe.loc[dataframe[column_name] == 0, 'nb_passages'].mean()
    dataframe.loc[dataframe[column_name] == 0, 'nb_passages'] = mean_nb_passages_zero_rain
    
    fig = px.scatter(dataframe, x=column_name, y='nb_passages', hover_name='date')
    
    fig.add_trace(
        go.Scatter(
            x=[dataframe[column_name].min(), dataframe[column_name].max()],
            y=[mean_nb_passages_zero_rain, mean_nb_passages_zero_rain],
            mode='lines',
            line=dict(color='gray', dash='dash'),
        )
    )
    
    xaxis_title = 'Quantité de pluie (mm)' if is_rain else 'Quantité de neige (cm)'
    fig.update_layout(
        xaxis_title=xaxis_title,
        yaxis_title='Nombre de passages (milliers)'
    )

    fig.show() 


df = get_dataframe()
temperature()
neige_ou_pluie(df.copy(deep=True))
neige_ou_pluie(df.copy(deep=True), False)
