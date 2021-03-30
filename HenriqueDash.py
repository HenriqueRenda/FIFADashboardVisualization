import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dataset Processing

#importing data
data = pd.read_csv('archive/players_21.csv')

#data cleaning
nonusefulcolumns = ['sofifa_id','player_url','long_name','league_rank']
nonusefulattributes = data.loc[:,'player_traits':]

data.drop(nonusefulcolumns, axis=1, inplace=True)
data.drop(nonusefulattributes, axis=1, inplace=True)


##############################################################

app = dash.Dash(__name__)

server = app.server

options = [{'label': 'Height', 'value': 'height_cm'},
           {'label': 'Weight', 'value': 'weight_kg'},
           {'label': 'Potential', 'value': 'potential'},
           {'label': 'Overall', 'value': 'overall'}]

app.layout = html.Div([
    html.H1("League Analysis by Age"),

    html.Br(),

    html.Label('Choose a Attribute:'),
    dcc.Dropdown(
        id='drop',
        options=options,
        value='overall'
    ),

    dcc.Graph(
        id='example-graph'
    ),

    html.Br(),

    dcc.RangeSlider(
        id='age_slider',
        min=data['age'].min(),
        max=data['age'].max(),
        value=[data['age'].min(), data['age'].max()],
        step=1,
        marks={16: '16',
               18: '18',
               22: '22',
               26: '26',
               30: '30',
               34: '34',
               38: '38',
               42: '42',
               46: '46',
               50: '50',
               54: '54'}
    )
])


@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='drop', component_property='value'), 
     Input(component_id="age_slider", component_property="value")]
)



def update_graph(input_value, age):
    filtered_by_age_data = data[(data['age'] >= age[0]) & (data['age'] <= age[1])]

    data_bar = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique(),
        textposition='outside'
    )

    layout_bar = dict(xaxis=dict(title='League'),
                      yaxis=dict(title=input_value),
                      height=400,
                      template='plotly_dark')

    fig = go.Figure(data=data_bar, layout=layout_bar)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

