# importing the libraries
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
from dash_table import DataTable
#import plotly.graph_objs as go
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
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
skills1=['skill_curve','skill_dribbling','skill_fk_accuracy','skill_ball_control','skill_long_passing']
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









################################################  APP  #################################################################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# server = app.server

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src='/assets/logo.png', height="150px")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
    ],
    color="#3A2657",
    dark=True,
)

controls_player_1 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label('Choose an old-school Player:'),
                html.Br(),
                dropdown_player_over_25,
            ]
        ),
    ],
    body=True,
)

controls_player_2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label('Choose a new generation Player:'),
                html.Br(),
                dropdown_player_under_25,
            ]
        ),
    ],
    body=True,
)


tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Phuc and Henrique's Work", className="card-text"),
        ]
    ),
    className=" mt-3",
)

tab1_content = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H2('Player-Comparison Tab'),

                    dbc.Row([

                        dbc.Col(
                            [
                                dbc.Row(
                                    controls_player_1
                                ),

                                html.Br(),

                                dbc.Row(html.Img(src='/assets/player_2.png', height="400px")
                                        ),

                                html.Br(),

                                dbc.Row(
                                    dbc.Table(dashtable_1)
                                ),

                                dbc.Row(dcc.Graph(id='graph_example_1')
                                        ),

                                dbc.Row(dcc.Graph(id='graph_example_3')
                                        )
                            ],
                            sm=3,
                            align="center"
                        ),

                        dbc.Col(dcc.Graph(id='graph_example'), sm=6),

                        # dbc.Col(add the man),

                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        controls_player_2
                                    ]
                                ),

                                html.Br(),

                                dbc.Row(html.Img(src='/assets/player_2.png', height="400px")
                                        ),

                                html.Br(),

                                dbc.Row(
                                    [
                                        dbc.Table(dashtable_2)
                                    ]
                                ),

                                dbc.Row(
                                    dcc.Graph(id='graph_example_2')
                                ),

                                dbc.Row(
                                    dcc.Graph(id='graph_example_4')
                                )
                            ],
                            sm=3
                        )
                    ])

                ]
            ),
            className=" mt-3"
        )
    ]
)

app.layout = dbc.Container([
    # html.H1("Fifa Players Analysis"),
    navbar,

    dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="Tab 1"),
            dbc.Tab(tab2_content, label="Tab 2"),
        ]
    ),
],
    fluid=True,
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
        font_color="black",
        font_size= 15
    )
    return fig

    ###############################################   table 1   ########################################################
@app.callback(
    [
        Output('table1', 'data'),
        Output('graph_example_1', 'figure'),
        Output('graph_example_3', 'figure')
    ],
    [Input('player1', 'value')]
)

def updateTable1(player1):
    table_updated1 = df[df['short_name'] == player1].to_dict('records')
#    return table_updated1

    df1_for_plot = pd.DataFrame(df1[df1['short_name'] == player1]['potential'])
    df1_for_plot['name'] = player2
    gauge1 = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=df1_for_plot.potential.iloc[0],
    mode="gauge+number",
    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "red"}}))

    # barplots
    df1_for_plot = pd.DataFrame(df1[df1['short_name'] == player1][skills1].iloc[0].reset_index())
    df1_for_plot.rename(columns={df1_for_plot.columns[1]: 'counts'}, inplace=True)
    df1_for_plot.rename(columns={df1_for_plot.columns[0]: 'skills'}, inplace=True)
    barplot1 = px.bar(df1_for_plot, x='counts', y='skills', orientation='h')
    barplot1.update_traces(marker_color='red')
    return table_updated1, gauge1, barplot1


    ###############################################   table 2   ########################################################
@app.callback(
    [
        Output('table2', 'data'),
        Output('graph_example_2', 'figure'),
        Output('graph_example_4', 'figure')
    ],
    [Input('player2', 'value')]
)

def updateTable2(player2):
    table_updated2 = df[df['short_name'] == player2].to_dict('records')

    df2_for_plot = pd.DataFrame(df2[df2['short_name'] == player2]['potential'])
    df2_for_plot['name'] = player2
    gauge2 = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=df2_for_plot.potential.iloc[0],
    mode="gauge+number",
    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "blue"}}))

    df2_for_plot = pd.DataFrame(df2[df2['short_name'] == player2][skills1].iloc[0].reset_index())
    df2_for_plot.rename(columns={df2_for_plot.columns[1]:'counts'}, inplace=True )
    df2_for_plot.rename(columns={df2_for_plot.columns[0]:'skills'}, inplace=True )
    barplot2 = px.bar(df2_for_plot,x='counts',y='skills',orientation='h')
    barplot2.update_traces(marker_color='blue')

    return table_updated2, gauge2, barplot2



if __name__ == '__main__':
    app.run_server(debug=True)