# data prep lib
import os
import pandas as pd
from sodapy import Socrata

# dcc = dash_core_components 
# from dash.dependencies import Input, Output, State

from dash import Dash, html, dcc, Input, Output 

import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__)


# import dataset, simple groupby for test
df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')

test_df = df.groupby(['Year Type','Year','Job'])[['Salaries','Total Compensation']].mean()
test_df.reset_index(inplace=True)
# print(test_df[:5])

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


# App layout
app.layout = html.Div([
    html.H1("SF Employment Job Dashboard", style={'text-align','center'}),
    dcc.Dropdown(id="select_year_type", #id (string; optional): The ID of this component, used to identify dash components in callbacks. The ID needs to be unique across all of the components in an app.
    options=[
        {"label":"Calendar_type", "value":'Calendar'},
        {"label":"Fiscal_type", "value":'Fiscal'}],
        multi=False,
        value='Calendar',
        style={'width':"40%"}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})
])


# execute py file
if __name__ == '__main__':
    app.run_server(debug=True)
    