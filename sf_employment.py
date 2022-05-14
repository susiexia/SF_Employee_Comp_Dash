# data prep lib
import os
import pandas as pd
from sodapy import Socrata

# dcc = dash_core_components 
# from dash.dependencies import Input, Output, State
# import plotly.graph_objects as go

from dash import Dash, html, dcc, Input, Output 
import plotly.express as px



app = Dash(__name__)


# import dataset, simple groupby for test
df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')

test_df = df.groupby(['Year Type','Year'])[['Salaries','Total Compensation']].mean()
test_df.reset_index(inplace=True)

print(test_df[:5])


fig = px.bar(test_df, x="Year Type", y="Total Compensation")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# App layout
#app.layout = html.Div(
#    html.H1("SF Employment Job Dashboard", style={'text-align','center'})
#    ,
#    dcc.Dropdown(id="select_year_type", #id (string; optional): The ID of this component, used to identify dash components in callbacks. The ID needs to be unique across all of the components in an app.
#    options=[
#        {"label":"Calendar_type", "value":"Calendar"},
#        {"label":"Fiscal_type", "value":"Fiscal"}],
#        multi=False,
#        value='Calendar',
#        style={'width':"40%"}
#    ),
#    html.Div(id='output_container', children=[]),
#    html.Br(),
#
#    dcc.Graph(id='year_type', figure={})
#)

# app callback to connect component interactive
#@app.callback(
#    [Output(component_id='output_container', component_property='children'),
#     Output(component_id='year_type', component_property='figure')],
#    [Input(component_id='select_year_type', component_property='value')]
#)
#def update_graph(option_slctd):
#    print(option_slctd)
#    print(type(option_slctd))
#
#    container = "The year chosen by user was: {}".format(option_slctd)
#
#    dff = test_df.copy()
#   dff = dff[dff["Year Type"] == option_slctd]
#    dff = dff[dff["Year"] == 2022]
#
#    # Plotly Express
#    fig = px.bar(df, x="Year Type", y="Total Compensation")
#
#    return container, fig
# execute py file
if __name__ == '__main__':
    app.run_server(debug=True)
    