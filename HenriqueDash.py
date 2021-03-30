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

metric_dropdown = dcc.Dropdown(
                            id='drop',
                            options=options,
                            value='overall'
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

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Label('Choose a Attribute:'),
    html.Br(),
    metric_dropdown,
    dcc.Graph(
        id='example-graph'
    ),
    html.Br(),
    age_slider
    
])

#########Callbacks########################################

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='drop', component_property='value'), 
     Input(component_id="age_slider", component_property="value")]
)


###########Bar plot#######################################

def bar_plot(input_value, age):
    filtered_by_age_data = data[(data['age'] >= age[0]) & (data['age'] <= age[1])]

    data_bar = dict(
        type='bar',
        y=filtered_by_age_data.groupby('league_name').median()[input_value].sort_values(ascending=False).head(5),
        x=filtered_by_age_data['league_name'].unique(),
        textposition='outside'
    )

    layout_bar = dict(title='League Analysis by Age',
                      xaxis=dict(title='League'),
                      yaxis=dict(title=input_value),
                      height=400,
                      template='plotly_dark')

    fig = go.Figure(data=data_bar, layout=layout_bar)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

