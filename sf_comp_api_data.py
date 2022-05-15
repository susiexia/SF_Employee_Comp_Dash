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
    # client = Socrata("data.sfgov.org", None) # public, limit 1000 rows
    client = Socrata("data.sfgov.org",API_Token)

    results = client.get(socrata_dataset_identifier,limit = None)
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




if __name__ == '__main__':
    app.run_server(debug=True)
