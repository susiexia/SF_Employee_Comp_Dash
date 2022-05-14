from config import API_Token
import pandas as pd
from sodapy import Socrata

from dash import Dash, html, dcc, Input, Output 
import plotly.express as px

# data source: https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd

# Connect and pull data from public Socrata API, then convert to DF


socrata_domain = 'data.sfgov.org,'
socrata_dataset_identifier = '88g8-5mnd'
# client = Socrata("data.sfgov.org", None) # non public, limit 1000 rows

client = Socrata("data.sfgov.org",
                  API_Token)

results = client.get(socrata_dataset_identifier,limit = None)
# Convert data into a pandas dataframe
df = pd.DataFrame(results)

print(df.shape)
exit()

