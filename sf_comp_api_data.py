from operator import index
from statistics import mean, median

from matplotlib.cbook import violin_stats
from config import API_Token
from data_clean import data_clean
from sodapy import Socrata

import pandas as pd
import numpy as np
from scipy import stats


from dash import Dash, html, dcc, Input, Output 
import plotly.express as px

######################################################
# MVC - Model: 1.load  
# Connect and pull data from public Socrata API,with preliminary filter, then convert to DF
try:
    socrata_domain = 'data.sfgov.org,'
    socrata_dataset_identifier = '88g8-5mnd'
    client = Socrata("data.sfgov.org",API_Token)

    results = client.get_all(socrata_dataset_identifier, 
    where = "year in ('2018','2019','2020','2021','2022') and year_type = 'Calendar'" )

    df = pd.DataFrame(results)
    print(df.shape)
except:
    df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')
    print('unable extract data by calling API, loading csv instead', df.shape)

# MVC - Model: 2.data prep and clean
clean_df = data_clean(df)

# df['year']=df["year"].dt.year


# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


######################################################
# MVC - View  
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1("Analytics Dashboard of SF Controller Employee Compensation", style={"textAlign":"center"}),
    html.Hr(),
    html.P("xxxxxxxxxxxxx"),

    dcc.Slider(
        clean_df['year'].min(),
        clean_df['year'].max(),
        step=None,
        value=clean_df['year'].max(),
        marks={str(year): str(year) for year in clean_df['year'].unique()},
        id='year-slider'
    ),
    dcc.Graph(id='slider-bar'),

    html.Div([
        dcc.Dropdown(id="drop_year",
                    options=[
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020},
                     {"label": "2021", "value": 2021}],
                    multi=False,
                    value=2020,
                    style={'width': "30%"}
                    ),
        dcc.Dropdown(id="drop_segment",
                    options=[
                        {"label": "Organization_group(6)", "value": 'organization_group'},
                        {"label": "Departments(51)", "value": 'department'},
                        {"label": "Job_family(56)", "value": 'job_family'},
                        {"label": "Job(1111)", "value": 'job'}],
                    multi=False,
                    value='Organization_group(6)',
                    style={'width': "30%"}
                    ),

        dcc.RadioItems(
                ['Top 5', 'Bottom 5'],
                'Top 5',
                id='top_or_bottom',
                inline=True,
                style={'width': "30%", 'display': 'inline-block'}
            )                
        ]),
    dcc.Graph(id='segment_fig')
# VIOLIN 

    # html.Div(html.Div(id="drpdn-div", children=[], className="two columns"),className="row"),

    # dcc.Interval(id="timer", interval=1000*60, n_intervals=0),
    # dcc.Store(id="stored", data={}),

#    html.Div(id="output-div", children=[]), 
])



######################################################
# MVC - Control

# silder bar chart
@app.callback(
    Output('slider-bar', 'figure'),
    Input('year-slider', 'value'))
def update_bar_charts(Year):
    bar_df = clean_df[clean_df["year"] == Year]
    bar_agg_df = bar_df.groupby('organization_group')['total_compensation'].agg(['mean','median'])

    bar = px.bar(
        bar_agg_df,
        x= bar_agg_df.index,
        y=bar_agg_df['mean'],
    #    color=bar_agg_df['mean'],
    #    barmode='group',
        labels={"x": "Org Group", "y": "Avg Total Compensation"}, 
        hover_data=[bar_agg_df['mean'], bar_agg_df['median']],
        color_continuous_scale=px.colors.sequential.RdBu,
        text=bar_agg_df['mean'],
        title="Median TC by Organization_group"
    )
    bar.update_layout(
        title=dict(x=0.5), margin=dict(l=550, r=20, t=60, b=20), paper_bgcolor="#D6EAF8"
    )
    bar.update_traces(texttemplate="%{text:.2s}")
    return bar

# two_dropdown_fig
@app.callback(
    Output('segment_fig', 'figure'),
    Input('drop_year', 'value'),
    Input('drop_segment', 'value'),
    # Input('drop_metrics', 'value'),
    Input('top_or_bottom','value'))
def update_segment_fig(year, segment, metrics,top):
    year_df = clean_df[clean_df['year'] == year]

    if  top =='Top 5':
        fig = px.bar(
            x= year_df[segment].value_counts()[:5].index, 
            y = year_df[segment].value_counts()[:5],
#            hover_data= [segment]
            )
    else:
        fig = px.bar(
            x= year_df[segment].value_counts()[-5:].index, 
            y = year_df[segment].value_counts()[-5:],
#            hover_data= [segment]
            )        

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig



# auto pull data from API every 5 minutes, then store it in hidden div
# also, create a dropdown filter for next deep dive invastigate section
@app.callback(Output("stored", "data"),
            #  Output("drpdn-div", "children"),
            Input('year-slider', 'value'),
            Input("timer","n_intervals"))
def store_aggre(year,n):
    filtered_df = clean_df[clean_df.year == year]
    test_df = filtered_df[['organization_group','department','total_compensation']].groupby(['organization_group','department'])['total_compensation'].agg(['mean','median'])
    test_df.reset_index(inplace=True)
    print(test_df.shape)
    return test_df.to_dict('records')


    

    # results.to_dict('records'), dcc.Dropdown(id='animal-type',
    #                                            clearable=False,
    #                                            value="DOG",
    #                                            options=[{'label': x, 'value': x} for x in
    #                                                     df["year"].unique()])


# BREAK-DOWN VIZ: two input,once stored data changes or update, children of output-div update

# @app.callback(Output("output-div", "children"),
#               Input("year", "value"),
#               Input("stored", "data"),
# )
# def make_bars(year_select, data):
#     df = pd.DataFrame(data)

######################
#  violin
#  fig = px.violin(df, y="total_bill")


#     SUNBURST
#     df_sburst = df.dropna(subset=['chip_status'])
#     df_sburst = df_sburst[df_sburst["intake_type"].isin(["STRAY", "FOSTER", "OWNER SURRENDER"])]
#     fig_sunburst = px.sunburst(df_sburst, path=["year", "intake_type", "chip_status"])

######################

#     HISTOGRAM
#     df_hist = df[df["year"]==year_select]
#     fig_hist = px.histogram(df_hist, x="job")
#     fig_hist.update_xaxes(categoryorder="total descending")

#     STRIP CHART
#     fig_strip = px.strip(df_hist, x="animal_stay_days", y="intake_type")

#     Empirical Cumulative Distribution
#     df_ecdf = df[df["year"].isin(["DOG","CAT"])]
#     fig_ecdf = px.ecdf(df_ecdf, x="animal_stay_days", color="year")

#     LINE CHART
#     df_line = df.sort_values(by=["salary"], ascending=True)
#     df_line = df_line.groupby(
#         ["intake_time", "year"]).size().reset_index(name="count")
#     fig_line = px.line(df_line, x="intake_time", y="count",
#                        color="year", markers=True)

#     return [
#         html.Div([
#             html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
#             html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
#         ], className="row"),
#         html.H2("All Animals", style={"textAlign":"center"}),
#         html.Hr(),
#         html.Div([
#             html.Div([dcc.Graph(figure=fig_sunburst)], className="six columns"),
#             html.Div([dcc.Graph(figure=fig_ecdf)], className="six columns"),
#         ], className="row"),
#         html.Div([
#             html.Div([dcc.Graph(figure=fig_line)], className="twelve columns"),
#         ], className="row"),
#     ]

if __name__ == '__main__':
    app.run_server(debug=True)
