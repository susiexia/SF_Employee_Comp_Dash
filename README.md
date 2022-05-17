# SF_Employee_Comp_dash
--------------------------------------------------
## Objectives:

Discover the high level trends and compensation component detaila in San Francisco Controller Employees Total Compensation (TC) during past 5 years.

--------------------------------------------------
## Output:
- ETL Jupyter Notebook  [sf_comp_jupyter_analytics.ipynb](/sf_comp_jupyter_analytics.ipynb)

- Application script [sf_comp_api_data.py](/sf_comp_api_data.py)

--------------------------------------------------

## Next Steps:
* Pretty style
* deploy to heroku
* introduce more dataset, merge and find more insights (for exa)

--------------------------------------------------

![challenge_Result.PNG](/challenge_Result.PNG)

--------------------------------------------------
--------------------------------------------------
### Data Resources:

The San Francisco Controller's Office maintains a database of the salary and benefits paid to City employees since fiscal year 2013.
SF Controller's Office Employee Salary Data [data_website](https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd)

## Scope and Assumption

This Analytics only considers 4 calendar years from 2018 to 2021.
Rows reduction from 759K to 168K, 
 (758604,22) ===> (168437, 22)

### columns info:
['organization_group_code', 'job_family_code', 'job_code', 'year_type', 'year', 'organization_group', 'department_code', 'department', 'union_code', 'union', 'job_family', 'job', 'employee_identifier', 'salaries', 'overtime', 'other_salaries', 'total_salary', 'retirement', 'health_and_dental', 'other_benefits', 'total_benefits', 'total_compensation']

--------------------------------------------------
## ANALYTICS Part
- ETL Jupyter Notebook  [sf_comp_jupyter_analytics.ipynb](/sf_comp_jupyter_analytics.ipynb)
### Insights

Unique number:
* Organization_group(6)
* department(51)
* job_family(56)
* job(1111)
employee nunique:
same employee joined different department,
duplicate different year but same employeee, assume: 
Job grunularity, keep the last record for each duplicated employee. 


--------------------------------------------------
## Dashboard Part
API:
no username or password needed

interval, auto update in seconds, then dcc.store to store API data in dictory file,(on the clients side)

store cleaned data 

## My other dashboard projects

- ['Dirty' data clean ETL](https://github.com/susiexia/Movies-ETL/blob/master/movies_ETL.ipynb)


- [geoJSON Javascript project](https://github.com/susiexia/Mapping_Earthquakes)
* [Deployed Map URL:](https://susiexia.github.io/Mapping_Earthquakes/)
* Traverse and retrieve GeoJSON data to populate an interactive geographical map about earthquakes and tectonic plates using JavaScript,leaflet.js libraries as well as Mapbox API.

- [another plotly Javascript project](https://github.com/susiexia/Plotly_Webpage)
* [Deployed plotly Dashboard](https://susiexia.github.io/Plotly_Webpage/)