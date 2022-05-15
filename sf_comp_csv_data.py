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

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


fig = px.bar(test_df, x="year_type", y="Total Compensation")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    html.H4(children='SF COMP TABLE'),
    generate_table(test_df),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),
    dcc.Graph(id='graph-with-slider')
])

# App layout
# app.layout = html.Div(
#    html.H1("SF Employment Job Dashboard", style={'text-align','center'}),
#    html.P("SF Employee compensation Yearly"),
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

#    dcc.Graph(id='year_type', figure={}),
#    dcc.Interval(id="timer", interval=1000*60, n_intervals=0), # 60 sec update
#    dcc.Store(id="stored", data={})
# )

# app callback to connect component interactive
@app.callback(
   [Output(component_id='output_container', component_property='children'),
    Output(component_id='year_type', component_property='figure')],
   [Input(component_id='select_year_type', component_property='value')]
)
def update_graph(option_slctd):
   print(option_slctd)
   print(type(option_slctd))

   container = "The year chosen by user was: {}".format(option_slctd)

   dff = test_df.copy()
   dff = dff[dff["Year Type"] == option_slctd]
   dff = dff[dff["Year"] == 2022]

   # Plotly Express
   fig = px.bar(df, x="Year Type", y="Total Compensation")

   return container, fig

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig
# timely trigger

# @app.callback(Output("stored", "data"),
# #              Output("drpdn-div", "children"),
#               Input("timer","n_intervals")
# )
# def get_drpdn_and_df(n):
#     print(test_df[:5])

#     return df.to_dict('records')




# execute py file
if __name__ == '__main__':
    app.run_server(debug=True)
    