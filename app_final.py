import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
from dash_table import DataTable
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Dataset Processing

#importing data
data = pd.read_csv('archive/players_21.csv')

#data cleaning
nonusefulcolumns = ['sofifa_id','player_url','long_name','league_rank']
nonusefulattributes = data.loc[:,'player_traits':]

df = data.copy()
df = df[df['player_positions'] != 'GK'] # filtering out all the goalkeepers
df1 = df[df['age'] > 25] # dataset for players over 25
df2 = df[df['age'] <= 25] # dataset for players under 25

# variables for the analysis
skill_player = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
info_player = ['short_name','nationality', 'club_name', 'age', 'height_cm', 'weight_kg']
skills1=['skill_curve','skill_dribbling','skill_fk_accuracy','skill_ball_control','skill_long_passing']
player1 = 'Lionel Andrés Messi Cuccittini'
player2 = 'Kylian Mbappé Lottin'


###################################################   Interactive Components   #########################################
# choice of the players
players_options_over_25 = []
for i in df1.index:
    players_options_over_25.append({'label': df1['long_name'][i], 'value':  df1['long_name'][i]})

players_options_under_25 = []
for i in df2.index:
    players_options_under_25.append({'label': df2['long_name'][i], 'value':  df2['long_name'][i]})

dropdown_player_over_25 = dcc.Dropdown(
        id='player1',
        options=players_options_over_25,
        value='Lionel Andrés Messi Cuccittini'
    )

dropdown_player_under_25 = dcc.Dropdown(
        id='player2',
        options=players_options_under_25,
        value='Kylian Mbappé Lottin'
    )

dashtable_1 = dash_table.DataTable(
        id='table1',
        columns=[{"name": i, "id": i} for i in info_player],
        data=df[df['long_name'] == player1].to_dict('records')
    )


dashtable_2 = dash_table.DataTable(
        id='table2',
        columns=[{"name": i, "id": i} for i in info_player],
        data=df[df['long_name'] == player2].to_dict('records')
    )



data.drop(nonusefulcolumns, axis=1, inplace=True)
data.drop(nonusefulattributes, axis=1, inplace=True)
data['isOver25'] = data['age'] > 25

################Components##############################################

options = [{'label': 'Overall', 'value': 'overall'},
           {'label': 'Potential', 'value': 'potential'},
           {'label': 'Value', 'value': 'value_eur'},
           {'label': 'Wage', 'value': 'wage_eur'},
           {'label': 'Height', 'value': 'height_cm'},
           {'label': 'Weight', 'value': 'weight_kg'},
           {'label': 'Pace', 'value': 'pace'},
           {'label': 'Shooting', 'value': 'shooting'},
           {'label': 'Passing', 'value': 'passing'},
           {'label': 'Dribbling', 'value': 'dribbling'},
           {'label': 'Defending', 'value': 'defending'},
           {'label': 'Physic', 'value': 'physic'}]
leagues = [ {'label':'Premier League', 'value':'English Premier League'},
            {'label':'Ligue 1', 'value':'French Ligue 1'},
            {'label':'Bundesliga', 'value':'German 1. Bundesliga'},
            {'label':'Serie A', 'value':'Italian Serie A'},
            {'label':'La Liga', 'value':'Spain Primera Division'}]
value_x =[{'label': 'Overall', 'value': 'overall'},
          {'label': 'Potential', 'value': 'potential'},
          {'label': 'Value', 'value': 'value_eur'},
          {'label': 'Wage', 'value': 'wage_eur'},]



metric1_dropdown = dcc.Dropdown(
                            id='drop1',
                            options=options,
                            value='overall'
                        )

metric2_dropdown = dcc.Dropdown(
                            id='drop2',
                            options=options,
                            value='potential'
                        )

metric3_dropdown = dcc.Dropdown(
                            id='drop3',
                            options=options,
                            value='value_eur'
                        )

metric_club_dropdown1 = dcc.Dropdown(
                            id='club-drop1',
                            options=leagues,
                            value='English Premier League'
                        )
metric_scatter_dropdown1 = dcc.Dropdown(
                            id='scatter-drop1',
                            options=value_x,
                            value='value_eur'
                        )
metric_scatter_dropdown2 = dcc.Dropdown(
                            id='scatter-drop2',
                            options=value_x,
                            value='wage_eur'
                        )

                       
age_slider = dcc.RangeSlider(
                            id='age_slider',
                            min=data['age'].min(),
                            max=data['age'].max(),
                            value=[data['age'].min(), data['age'].max()],
                            step=1,
                            marks={16: '16',
                                22: '20',
                                26: '24',
                                30: '28',
                                34: '32',
                                38: '36',
                                42: '40',
                                46: '44',
                                50: '48',
                                54: '52'}
                        )

########Dash App Layout##########################

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

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

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label('Choose a Attribute:'),
                html.Br(),
                metric1_dropdown,
            ]
        ),

        dbc.FormGroup(
            [
                html.Label('Choose a Attribute:'),
                html.Br(),
                metric2_dropdown,
            ]
        ),

        dbc.FormGroup(
            [
                html.Label('Choose a Attribute:'),
                html.Br(),
                metric3_dropdown
            ]
        ),
    ],
    body=True,
    className="controls",
)

controls_club = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label('Choose a League:'),
                html.Br(),
                metric_club_dropdown1,
            ]
        ),
        dbc.FormGroup(
            [
                html.Label('Choose an attribute for x:'),
                html.Br(),
                metric_scatter_dropdown1,
            ]
        ),
        dbc.FormGroup(
            [
                html.Label('Choose an attribute for y:'),
                html.Br(),
                metric_scatter_dropdown2,
            ]
        ),
    ],
    body=True,
    className="controls",
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

                                dbc.Row(html.Img(src='/assets/player_1.png',className="playerImg"),
                                        ),

                                html.Br(),

                                dbc.Row(
                                    dbc.Table(dashtable_1)
                                ),

                                dbc.Row([
                                    dbc.Col([
                                        dcc.Graph(id='graph_example_1')
                                    ]
                                    ),
                                    dbc.Col([
                                        dcc.Graph(id='graph_example_3')
                                    ]
                                    )
                                ]
                                ),
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

                                dbc.Row(html.Img(src='/assets/player_3.png',className="playerImg"),
                                        ),

                                html.Br(),

                                dbc.Row(
                                    [
                                        dbc.Table(dashtable_2)
                                    ]
                                ),

                                dbc.Row([
                                        dbc.Col([
                                                dcc.Graph(id='graph_example_2')
                                            ]
                                        ),
                                        dbc.Col([
                                                dcc.Graph(id='graph_example_4')
                                            ]
                                            )
                                        ]
                                ),

                            ],
                            sm=3
                        )
                    ]),
                ]
            ),
            className=" mt-3"
        )
    ]
)

tab2_content = html.Div(
    [
        dbc.Card(    
            dbc.CardBody(
                [
                    html.H1("League Analysis"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls,sm=3),

                            dbc.Col(
                                dcc.Graph(id='league-graph1',className="LeagueBarPlot"),sm=3
                                ),

                            dbc.Col(
                                dcc.Graph(id='league-graph2',className="LeagueBarPlot"),sm=3
                                ),

                            dbc.Col(
                                dcc.Graph(id='league-graph3',className="LeagueBarPlot"),sm=3
                                ),
                        ],
                        align="center",
                    ),
                    
                    dbc.Row([
                        dbc.Label("Select Age:", style={'margin-left' : '5%', 'font-size': '20px'}),
                        dbc.Col(age_slider,align = "center")
                    ]),
                ]
            ),
        ),
        html.Br(),
        dbc.Card(    
            dbc.CardBody(
                [
                    html.H1("Clubs Analysis"),
                    html.Hr(),  
                    dbc.Row(
                        [
                        dbc.Col(controls_club,sm=2),

                        dbc.Col(
                            dcc.Graph(id='club-graph1',className="LeagueBarPlot"),sm=5
                        ),
                        dbc.Col(
                            dcc.Graph(id='club-graph2',className="LeagueBarPlot"),sm=5
                        )
                        ],
                        align="center",
                    ),     
                ]
            ),
            className=" mt-3"
        )
    ]
)    

app.layout = dbc.Container([
        #html.H1("Fifa Players Analysis"),
        navbar,

        dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Players"),
                dbc.Tab(tab2_content, label="League & Club"),
            ]
        ),
    ],
    fluid=True,
)

#########Callbacks########################################

@app.callback(
    [Output(component_id='league-graph1', component_property='figure'),
     Output(component_id='league-graph2', component_property='figure'),
     Output(component_id='league-graph3', component_property='figure')],
    [Input(component_id='drop1', component_property='value'),
     Input(component_id='drop2', component_property='value'),
     Input(component_id='drop3', component_property='value'), 
     Input(component_id="age_slider", component_property="value")]
)
###########Bar plot#######################################
def bar_plot(input_value1,input_value2,input_value3, age):

    filtered_by_age_data = data[(data['age'] >= age[0]) & (data['age'] <= age[1])]

    data_bar1 = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value1].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique()
    )

    data_bar2 = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value2].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique()
    )

    data_bar3 = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value3].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique()
    )

    layout_bar1 = dict(
                      xaxis=dict(title='League', tickangle=45),
                      yaxis=dict(title=input_value1),
                      )
    
    layout_bar2 = dict(
                      xaxis=dict(title='League',tickangle=45),
                      yaxis=dict(title=input_value2),
                      )
    
    layout_bar3 = dict(
                      xaxis=dict(title='League',tickangle=45),
                      yaxis=dict(title=input_value3),
                      )

    return go.Figure(data=data_bar1, layout=layout_bar1), \
           go.Figure(data=data_bar2, layout=layout_bar2), \
           go.Figure(data=data_bar3, layout=layout_bar3)

#----------------Callbacks for 2nd tab, clubs analysis----------------#
@app.callback(
    [Output(component_id='club-graph1', component_property='figure'),
     Output(component_id='club-graph2', component_property='figure')],
    [Input(component_id='club-drop1', component_property='value'),
    Input(component_id='scatter-drop1', component_property='value'),
    Input(component_id='scatter-drop2', component_property='value')]
)

###########Bar plot#######################################
def plots_clubs(league,x_val,y_val):
    # Scatter plot
    plot_df = data[data['league_name'] == league].sort_values('overall',ascending = False).head(100)
    fig1 = px.scatter(data_frame  = plot_df, x=x_val, y=y_val,color="isOver25", size = 'potential',
                        color_discrete_sequence=['red','royalblue'], hover_name ='short_name'
                        ,  title = ('Wage and Value of top 100 players in '+league))    
    # Bar plot
    plot_df = data[data['league_name'] == league].groupby(['club_name','isOver25']).count()['short_name'].reset_index()
    plot_df = pd.pivot_table(plot_df, values='short_name', index=['club_name'],
                    columns=['isOver25'], aggfunc=np.sum).reset_index()
    x = plot_df['club_name']
    y = plot_df.iloc[:,-2:].div(plot_df.iloc[:,-2:].sum(axis=1), axis=0)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(y=x,x=y[False],name='Under 25y',orientation='h'))
    fig2.add_trace(go.Bar(y=x,x=y[True],name='Over 25y',orientation='h'))
    fig2.update_layout(barmode='stack')
    return fig1,fig2

#----------------Callbacks for 1st tab, clubs analysis----------------#

@app.callback(
    [
        Output('graph_example', 'figure'),
        Output('table1', 'data'),
        Output('graph_example_1', 'figure'),
        Output('graph_example_3', 'figure'),
        Output('table2', 'data'),
        Output('graph_example_2', 'figure'),
        Output('graph_example_4', 'figure')
    ],
    [
        Input('player1', 'value'),
        Input('player2', 'value')
    ]
)

###############################################   radar plot   #####################################################

def tab_1_function(player1, player2):

    # scatterpolar
    df1_for_plot = pd.DataFrame(df1[df1['long_name'] == player1][skill_player].iloc[0])
    df1_for_plot.columns = ['score']
    df2_for_plot = pd.DataFrame(df2[df2['long_name'] == player2][skill_player].iloc[0])
    df2_for_plot.columns = ['score']
    fig = go.Figure(data=go.Scatterpolar(
      r=df1_for_plot['score'],
      theta=df1_for_plot.index,
      fill='toself',
        name = player1
    ))
    fig.add_trace(go.Scatterpolar(
          r=df2_for_plot['score'],
          theta=df2_for_plot.index,
          fill='toself',
          name= player2
    ))
    fig.update_layout(
      polar=dict(
          hole=0.2,
          bgcolor="white",
     radialaxis=dict(
          visible=True,
            type='linear',
            autotypenumbers='strict',
            autorange=False,
            range=[30, 100],
            angle=90,
            showline=False,
    #         showgrid=False
            gridcolor='black'
        )
      ),
      showlegend=True,
      template="plotly_dark",
              plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            font_color="black",
            font_size= 15
    )

    # table 1
    table_updated1 = df[df['long_name'] == player1].to_dict('records')

    # gauge plot 1
    df1_for_plot = pd.DataFrame(df1[df1['long_name'] == player1]['potential'])
    df1_for_plot['name'] = player2
    gauge1 = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=df1_for_plot.potential.iloc[0],
    mode="gauge+number",
    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "red"}}))

    # barplot 1
    df1_for_plot = pd.DataFrame(df1[df1['long_name'] == player1][skills1].iloc[0].reset_index())
    df1_for_plot.rename(columns={df1_for_plot.columns[1]: 'counts'}, inplace=True)
    df1_for_plot.rename(columns={df1_for_plot.columns[0]: 'skills'}, inplace=True)
    barplot1 = px.bar(df1_for_plot, x='counts', y='skills', orientation='h')
    barplot1.update_traces(marker_color='red')

    # table 2
    table_updated2 = df[df['long_name'] == player2].to_dict('records')

    # gauge plot 2
    df2_for_plot = pd.DataFrame(df2[df2['long_name'] == player2]['potential'])
    df2_for_plot['name'] = player2
    gauge2 = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=df2_for_plot.potential.iloc[0],
    mode="gauge+number",
    gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "blue"}}))

    # bar plot 2
    df2_for_plot = pd.DataFrame(df2[df2['long_name'] == player2][skills1].iloc[0].reset_index())
    df2_for_plot.rename(columns={df2_for_plot.columns[1]:'counts'}, inplace=True )
    df2_for_plot.rename(columns={df2_for_plot.columns[0]:'skills'}, inplace=True )
    barplot2 = px.bar(df2_for_plot,x='counts',y='skills',orientation='h')
    barplot2.update_traces(marker_color='blue')

    # outputs
    return fig, table_updated1, gauge1, barplot1, table_updated2, gauge2, barplot2



if __name__ == '__main__':
    app.run_server(debug=True)

