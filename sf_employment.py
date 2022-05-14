# data prep lib
import os
import pandas as pd
from sodapy import Socrata

# dash lib
import dash
import plotly.express as px
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)


# import dataset, simple groupby for test
df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')

test_df = df.groupby(['Year Type','Year','Job'])[['Salaries','Total Compensation']].mean()
test_df.reset_index(inplace=True)
print(test_df[:5])
