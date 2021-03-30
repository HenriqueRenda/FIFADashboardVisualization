import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
#from tabulate import tabulate
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import seaborn as sns

# importing the data

df = pd.read_csv('players_21.csv')

players_options = []
for i in df.index:
    players_options.append({'label': df['long_name'][i], 'value':  df['short_name'][i]})

# The app itself
app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Player-Comparison Tab'),

    html.Label('Select Player 1'),
    dcc.Dropdown(
        id='player1',
        options=players_options,
        value='L. Messi'
    ),

    html.Label('Select Player 2'),
    dcc.Dropdown(
        id='player2',
        options=players_options,
        value='Cristiano Ronaldo'
    ),

    dcc.Graph(id='graph_example')
])

@app.callback(
    Output('graph_example', 'figure'),
    [Input('player1', 'value'),
     Input('player2', 'value')]
)

# function for the plot
def radar_player(player1, player2):
    info_player = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    df1 = pd.DataFrame(df[df['short_name'] == player1][info_player].iloc[0]).reset_index()
    df1['name'] = player1
    df1.columns = ['skill', 'score', 'name']

    df2 = pd.DataFrame(df[df['short_name'] == player2][info_player].iloc[0]).reset_index()
    df2['name'] = player2
    df2.columns = ['skill', 'score', 'name']

    df_for_plot = pd.concat([df1, df2], axis = 0)

    colors = ['red', 'blue']
    fig = px.line_polar(df_for_plot, r='score', theta="skill", color="name", line_close=True,
                        color_discrete_sequence=colors,
                        template="plotly_dark")
    fig.update_traces(fill='toself')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)