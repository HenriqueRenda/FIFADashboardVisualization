# importing the libraries
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
from dash_table import DataTable
# import plotly.graph_objs as go
#import matplotlib.pyplot as plt
#from tabulate import tabulate
#import plotly.graph_objects as go
#import numpy as np
#import seaborn as sns
import dash_bootstrap_components as dbc

################################################ importing the data ####################################################
df = pd.read_csv('players_21.csv')
df1 = df[df['age'] > 25] # dataset for players over 25
df2 = df[df['age'] <= 25] # dataset for players under 25

# variables for the analysis
skill_player = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
info_player = ['short_name','nationality', 'club_name', 'age', 'height_cm', 'weight_kg']
player1 = 'L. Messi'
player2 = 'K. Mbappé'


###################################################   Interactive Components   #########################################
# choice of the players
players_options_over_25 = []
for i in df1.index:
    players_options_over_25.append({'label': df1['long_name'][i], 'value':  df1['short_name'][i]})

players_options_under_25 = []
for i in df2.index:
    players_options_under_25.append({'label': df2['long_name'][i], 'value':  df2['short_name'][i]})

dropdown_player_over_25 = dcc.Dropdown(
        id='player1',
        options=players_options_over_25,
        value='L. Messi'
    )

dropdown_player_under_25 = dcc.Dropdown(
        id='player2',
        options=players_options_under_25,
        value='K. Mbappé'
    )

dashtable_1 = dash_table.DataTable(
        id='table1',
        columns=[{"name": i, "id": i} for i in info_player],
        data=df[df['short_name'] == player1].to_dict('records')
    )


dashtable_2 = dash_table.DataTable(
        id='table2',
        columns=[{"name": i, "id": i} for i in info_player],
        data=df[df['short_name'] == player2].to_dict('records')
    )

#dashtable_prova = df[df['short_name'] == player2][info_player].T






################################################  APP  #################################################################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# server = app.server

# defining the layout
app.layout = dbc.Container(
    [
        html.H2('Player-Comparison Tab'),

        dbc.Row([



            dbc.Col(
                [
                    dbc.Row(
                        dropdown_player_over_25
                    ),

                    dbc.Row(
                        dbc.Table(dashtable_1)
                       )
                ],
                sm=3
            ),

            #dbc.Col(add the man),

            dbc.Col(dcc.Graph(id='graph_example'),sm=6),

            #dbc.Col(add the man),

            dbc.Col(
                [
                    dbc.Row(
                        [
                            dropdown_player_under_25
                        ]
                    ),

                    dbc.Row(
                        [
                            dbc.Table(dashtable_2)
                            #dbc.Table.from_dataframe(dashtable_2, striped=True, bordered=True, hover=True)
                        ]
                    )
                ],
                sm=3
            )
        ])
    ]
)


###################################################   Callbacks   ######################################################

@app.callback(
    Output('graph_example', 'figure'),
    [
        Input('player1', 'value'),
        Input('player2', 'value')
    ]
)

###############################################   radar plot   #####################################################
def radar_player(player1, player2):

    df1_for_plot = pd.DataFrame(df1[df1['short_name'] == player1][skill_player].iloc[0]).reset_index()
    df1_for_plot['name'] = player1
    df1_for_plot.columns = ['skill', 'score', 'name']

    df2_for_plot = pd.DataFrame(df2[df2['short_name'] == player2][skill_player].iloc[0]).reset_index()
    df2_for_plot['name'] = player2
    df2_for_plot.columns = ['skill', 'score', 'name']

    df_for_plot = pd.concat([df1_for_plot, df2_for_plot], axis = 0)

    colors = ['red', 'blue']
    fig = px.line_polar(df_for_plot, r='score', theta="skill", color="name", line_close=True,
                        color_discrete_sequence=colors)
    fig.update_traces(fill='toself')
    fig.update_layout(
        plot_bgcolor = 'rgba(0, 0, 0, 0)',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font_color="white",
        font_size= 15
    )
    return fig

    ###############################################   table 1   ########################################################
@app.callback(
    Output('table1', 'data'),
    [Input('player1', 'value')]
)
def updateTable1(player1):
    table_updated1 = df[df['short_name'] == player1].to_dict('records')
    return table_updated1

    ###############################################   table 2   ########################################################
@app.callback(
    Output('table2', 'data'),
    [Input('player2', 'value')]
)

def updateTable2(player2):
    table_updated2 = df[df['short_name'] == player2].to_dict('records')
    return table_updated2



if __name__ == '__main__':
    app.run_server(debug=True)