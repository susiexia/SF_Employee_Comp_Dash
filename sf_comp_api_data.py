
from flask_caching import Cache
from config import API_Token
from data_clean import data_clean
from sodapy import Socrata

import pandas as pd

from dash import Dash, html, dcc, Input, Output, exceptions 
import plotly.express as px
import plotly.figure_factory as ff

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
    print('----------Data Loaded----------/n', df.shape)
except:
    df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')
    print('!!!unable extract data by calling API, loading csv instead!!!', df.shape)

# MVC - Model: 2.data prep and clean
clean_df = data_clean(df)
print(clean_df.head())

# help function
def aggrgate_df(target, column_name,  sort_by_item, top = True):

    df = target.copy()
    agg_df = pd.DataFrame(df.groupby(column_name)[['salaries', 'overtime', 'other_salaries', 'total_salary', 'retirement', 'health_and_dental', 'other_benefits', 'total_benefits', 'total_compensation']].mean())
    agg_df['pct_benefit'] = agg_df['total_benefits']/agg_df['total_compensation']

    top_agg = agg_df.sort_values(by=[sort_by_item], ascending=False)
    bom_agg = agg_df.sort_values(by=[sort_by_item], ascending=True)
    #agg_df.reset_index(inplace=True)
    if top:
        top_5_df = top_agg.iloc[0:5]
        return top_5_df
    else:
        less_5_df = bom_agg.iloc[0:5]
        return less_5_df

######################################################
# MVC - View  
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H3("Analytics Dashboard of SF Controller Employee Compensation", style={"textAlign":"center"}),
    html.H4("Analytics Dashboard", style={"textAlign":"center"}),

    html.Hr(),
    html.H6("Discover compensation from aggregated insights"),
    html.P("Which year are you looking for?"),

    dcc.Slider(id='year_slider', value=2018, min=2018, max=2021, step=1,
         marks={"2018":'2018', "2019":'2019',"2020":'2020',"2021":'2021'}
     ),
    html.P("Which segment are you looking for?"),    
    html.Div([
        dcc.RadioItems(id="drop_top",
                options = [
                     {"label": "Top 5", "value": 'top'},
                     {"label": "Bottom 5", "value": 'bottom'}],
                value = 'top',
                style={'width': "50%", 'display': 'inline-block'}
            ),                
        dcc.Dropdown(id="drop_segment",
                    options=[
                        {"label": "Organization_group", "value": 'organization_group'},
                        {"label": "department", "value": 'department'},
                        {"label": "job_family", "value": 'job_family'},
                        {"label": "job", "value": 'job'}],
                    multi=False,
                    value="organization_group",
                    style={'width': "50%", 'display': 'inline-block'}
                    )
    ]),
    html.Div(id='output_container', children=[]),
    html.Hr(),
    html.Div([
            html.Div([dcc.Graph(id = 'slider_graph')], className="six columns"),
            html.Div([dcc.Graph(id = 'pct_graph')], className="six columns"),
        ], className="row"),

    html.Hr(),
    
    html.Div([
        html.H6("Deep Dive Into Popular Job Choice"),
        dcc.RadioItems(id="three_job",
                    options=[
                     {"label": "Transit Operator", "value": 'Transit Operator'},
                     {"label": "Special Nurse", "value": 'Special Nurse'},
                     {"label": "Firefighter", "value": 'Firefighter'}],
                    value='Firefighter',
                    style={'width': "90%",'display': 'inline-block'}
                    ),
        html.Div(id='second_container', children=[]),
        html.Div([
            dcc.Graph(id ='distplot_graph')
        ])
    ]
    )
    #dcc.Store(id="stored", data={}),
])

######################################################
# MVC - Control

# dimension charts
@app.callback(
    [
        Output('output_container', 'children'), 
        Output('slider_graph', 'figure'),
        Output('pct_graph', 'figure')
        ],
    [   
        Input('year_slider', 'value'),
        Input('drop_top','value'),
        Input('drop_segment', 'value')
        ])
def update_silder_charts(year_value, top_or_bottom, segment_value):

    print(type(year_value))
    print(year_value)
    slider_df = clean_df.copy()
    container = f"Aggregated Data Insight with Year of {year_value} and segment in the view of {segment_value}"
    print(slider_df.head(2), 'The before slider df info')
    
    
    slider_df = slider_df[slider_df['year'] == year_value]

    if len(slider_df.index)==0:
        raise exceptions.PreventUpdate
    else:
        print(slider_df.head(10), 'The after slider df info')

    # sort_by_item: 'pct_benefit' or 'total_compensation"
        if top_or_bottom == 'top':
            print('--------Top run--------')
            top_slider_df = slider_df.copy()
            # top_df = aggrgate_df(slider_df,segment_value, 'total_compensation',top=True)
            # print(top_df.columns)
            # print(top_df.head(3))
            # print('-------------!!!Top end!!!!-------')

            bar = px.bar(
                data_frame= aggrgate_df(top_slider_df,segment_value,'total_compensation', top=True),
                x=aggrgate_df(top_slider_df,segment_value,'total_compensation', top=True).index.tolist(),
                y=['total_salary','total_benefits'],
                labels={"x": segment_value, "y": "Avg Total Compensation"}, 
                hover_data=['total_compensation'],
            #    text=top_df.index.tolist(),
                title="Total Compensation in Top 5 {}".format(segment_value)
            )

            pct_bar = px.bar(
                data_frame= aggrgate_df(top_slider_df,segment_value,'pct_benefit', top=True),
                x=aggrgate_df(top_slider_df,segment_value,'pct_benefit', top=True).index.tolist(),

                y=['pct_benefit','total_compensation'],
                labels={"x": segment_value, "y": "Benefit Percentage"}, 
                hover_data=['total_compensation'],
            #    text=top_df.index.tolist(),
                title="Benefit of TC percentage in Top 5 {}".format(segment_value)
            )

        elif top_or_bottom =='bottom':
            print('--------Bottom run--------')
            bottom_slider_df = slider_df.copy()

            bar = px.bar(
                data_frame= aggrgate_df(bottom_slider_df,segment_value,'total_compensation', top=False),
                x=aggrgate_df(bottom_slider_df,segment_value,'total_compensation', top=False).index.tolist(),
                y=['total_salary','total_benefits'],
                labels={"x": 'Dimension', "y": "Avg Total Compensation"}, 
                hover_data=['total_compensation'],
                title="Total Compensation in Bottom 5 {}".format(segment_value)
            )
            pct_bar = px.bar(
                data_frame= aggrgate_df(bottom_slider_df,segment_value,'pct_benefit', top=False),
                x=aggrgate_df(bottom_slider_df,segment_value,'pct_benefit', top=False).index.tolist(),

                y=['pct_benefit','total_compensation'],
                labels={"x": 'Dimension', "y": "Benefit Percentage"}, 
                hover_data=['total_compensation'],
                title="Benefit percentage in Top 5 {}".format(segment_value)
            )
        else:
            raise exceptions.PreventUpdate
    return container, bar, pct_bar

@app.callback(
    [Output('second_container', 'children'), 
    Output('distplot_graph','figure')],
    Input('three_job','value')
)
def update_distplot(job_value):
    dist_df = clean_df.copy()
    print(job_value)
    print(type(job_value))
    print('----distribution begin!!!!!------')
    print(dist_df.head(9))

    second_container = f"The Year-over-Year changes in distribution in {job_value} job"
    #yr_lst = [2018,2019,2020,2021]
    dist_df = dist_df[dist_df['job'] ==job_value]
    
    if len(dist_df.index)==0:
        raise exceptions.PreventUpdate
    else:
        print('----distribution data ready!!!!!------')
        print(f'The distribution df is {dist_df.shape}')

        #dist_fig = ff.create_distplot(dist_df,'total_compensation')
        fig = px.histogram(dist_df, "total_compensation", color='year', marginal='box')
    
    return second_container, fig

if __name__ == '__main__':
    app.run_server(debug=True)
