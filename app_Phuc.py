import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

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
)

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("Lorenzo and Catarina's Work", className="card-text"),
        ]
    ),
    className=" mt-3",
)

tab2_content = html.Div(
    [
        dbc.Card(    
            dbc.CardBody(
                [
                    html.H1("League and Clubs Analysis"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls,sm=3),

                            dbc.Col(
                                dcc.Graph(id='example-graph1'),sm=3
                                ),

                            dbc.Col(
                                dcc.Graph(id='example-graph2'),sm=3
                                ),

                            dbc.Col(
                                dcc.Graph(id='example-graph3'),sm=3
                                ),
                        ],
                        align="center",
                    ),
                    
                    dbc.Row(
                        [
                            dbc.Col(age_slider)
                        ],
                        align="center",
                    ),
                ]
            ),
            className=" mt-3" 
        ),
        html.Br(),
        dbc.Card(    
            dbc.CardBody(
                [
                    html.H1("Clubs Analysis"),
                    html.Hr(),  
                    dbc.Row(
                        [
                        dbc.Col(controls_club,width=2),

                        dbc.Col(
                            dbc.Card([
                                dcc.Graph(id='club-graph1')
                            ]),width=5
                        ),

                        dbc.Col(
                            dbc.Card([
                                dcc.Graph(id='club-graph2')
                            ]),width=5
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
                dbc.Tab(tab1_content, label="Tab 1"),
                dbc.Tab(tab2_content, label="Tab 2"),
            ]
        ),
    ],
    fluid=True,
)

#########Callbacks########################################

@app.callback(
    [Output(component_id='example-graph1', component_property='figure'),
     Output(component_id='example-graph2', component_property='figure'),
     Output(component_id='example-graph3', component_property='figure')],
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
        x=filtered_by_age_data['league_name'].unique(),
        textposition='outside'
    )

    data_bar2 = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value2].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique(),
        textposition='outside'
    )

    data_bar3 = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value3].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique(),
        textposition='outside'
    )

    layout_bar1 = dict(
                      xaxis=dict(title='League'),
                      yaxis=dict(title=input_value1))
    
    layout_bar2 = dict(
                      xaxis=dict(title='League'),
                      yaxis=dict(title=input_value2))
    
    layout_bar3 = dict(
                      xaxis=dict(title='League'),
                      yaxis=dict(title=input_value3))

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


if __name__ == '__main__':
    app.run_server(debug=True)

