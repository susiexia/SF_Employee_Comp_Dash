# plotly_dash
Practice in plotly/dash with python

## Objectives:

Discover the high level trends and compensation component detail in San Francisco Controller Employees Total Compensation (TC) during past 5 years.

compensation breakdown by org, department, job 
yoy

## scope

union information
Asumption

data

The San Francisco Controller's Office maintains a database of the salary and benefits paid to City employees since fiscal year 2013.
SF Controller's Office Employee Salary Data
https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd

## Assumption:
only consider 4 calendar years: 2018 to 2022,  calendar 
Rows reduction from 759K to 168K, 
 (758604,22) ===> (168437, 22)

### columns:
['organization_group_code', 'job_family_code', 'job_code', 'year_type', 'year', 'organization_group', 'department_code', 'department', 'union_code', 'union', 'job_family', 'job', 'employee_identifier', 'salaries', 'overtime', 'other_salaries', 'total_salary', 'retirement', 'health_and_dental', 'other_benefits', 'total_benefits', 'total_compensation']


## ANALYTICS

### Insights

EDA:

numerical // categorical


employee nunique:
same employee joined different department,
duplicate different year but same employeee, assume: 
Job grunularity, keep the last record for each duplicated employee. 


========
DASHBOARD VISUALIZATIONS
API:
no username or password needed

interval, auto update in seconds, then dcc.store to store API data in dictory file,(on the clients side)

store cleaned data 

chained callback

CSV FORMAT:



Jupyter NB: 
analytics, find trends, insights