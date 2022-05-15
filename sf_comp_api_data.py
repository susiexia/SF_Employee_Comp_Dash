from config import API_Token
import pandas as pd
from sodapy import Socrata

from dash import Dash, html, dcc, Input, Output 
import plotly.express as px

# data source: https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd

# Connect and pull data from public Socrata API, then convert to DF
try:
    socrata_domain = 'data.sfgov.org,'
    socrata_dataset_identifier = '88g8-5mnd'
    client = Socrata("data.sfgov.org",API_Token)

    results = client.get(socrata_dataset_identifier,limit = None)
   
    # or df = pd.read_json('')

    df = pd.DataFrame(results)
    print(df.shape)
except:
    df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')
    print('unable extract data by calling API, loading csv instead', df.shape)

def aggregated_yr(df):
    test_df = df[df['year_type']=='Calendar']
#    test_df.reset_index(inplace=True)
    return test_df



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



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1("Analytics Dashboard of Dallas Animal Shelter (Dash Plotly)", style={"textAlign":"center"}),
    html.Hr(),
    html.P("xxxxxxxxxxxxx"),


    html.Div(html.Div(id="drpdn-div", children=[], className="two columns"),className="row"),

    dcc.Interval(id="timer", interval=1000*60, n_intervals=0),
    dcc.Store(id="stored", data={}),

#    html.Div(id="output-div", children=[]), 
])



# auto pull data from API every 5 minutes, then store it in hidden div
# also, create a dropdown filter for next deep dive invastigate section
@app.callback(Output("stored", "data"),
              Output("drpdn-div", "children"),
              Input("timer","n_intervals")
)
def get_drpdn_and_df(n):
    results = aggregated_yr(df)

    print(results.iloc[:, :4].head())

    return results.to_dict('records'), dcc.Dropdown(id='animal-type',
                                               clearable=False,
                                               value="DOG",
                                               options=[{'label': x, 'value': x} for x in
                                                        df["year"].unique()])


# BREAK-DOWN VIZ: two input,once stored data changes or update, children of output-div update

# @app.callback(Output("output-div", "children"),
#               Input("year", "value"),
#               Input("stored", "data"),
# )
# def make_bars(year_select, data):
#     df = pd.DataFrame(data)

#     HISTOGRAM
#     df_hist = df[df["year"]==year_select]
#     fig_hist = px.histogram(df_hist, x="job")
#     fig_hist.update_xaxes(categoryorder="total descending")

#     STRIP CHART
#     fig_strip = px.strip(df_hist, x="animal_stay_days", y="intake_type")

#     SUNBURST
#     df_sburst = df.dropna(subset=['chip_status'])
#     df_sburst = df_sburst[df_sburst["intake_type"].isin(["STRAY", "FOSTER", "OWNER SURRENDER"])]
#     fig_sunburst = px.sunburst(df_sburst, path=["year", "intake_type", "chip_status"])

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
