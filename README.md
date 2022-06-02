# SF_Employee_Comp_dash

--------------------------------------------------
## Objectives:

1. Explore and discover the compensation details and high-level trends from historical datasets of San Francisco Controller Employees Total Compensation (TC) during past 4 years.

2. Provide visualized insights to help job-seekers learn more about how does SF Controller's Office pay to their employees.

[web_demo.mov](/web_demo.mov)


https://user-images.githubusercontent.com/57109686/169027905-fa1a7b0e-4e37-46ef-827e-cf601e28a8da.mov


--------------------------------------------------
**Screenshot**
![web_screenshot.png](/web_screenshot.png)
--------------------------------------------------
## Process and Output:

1. ETL Jupyter Notebook: [sf_comp_jupyter_analytics.ipynb](/sf_comp_jupyter_analytics.ipynb)

2. ETL python script:[data_clean.py]

3. Application script: [sf_comp_api_data.py](/sf_comp_api_data.py)

4. deploy to Web(TBC)

--------------------------------------------------
## Limitation and Next Steps:
Since time and scope limitation, this project focused on the job market and information from controller office since 2018, and the dashboard currently focus on aggregate information. Besides challegence from data, the large-scale data means huge page_load time when I deployed. Next steps I plan to:

* Introduce more datasets, cross and merge to draw more useful insights to job-seeker: 
    * for example, comparing to other cities controller compensation in the same period, 
    * or compare to non-gov job market)
* Increase page load speed, will add cache or dcc.store to temparay store and share data
* Add pretty style
* Deploy to heroku

--------------------------------------------------
### Data Resources:
The San Francisco Controller's Office maintains a database to record the salary and benefits paid to City employees since fiscal year 2013.
SF Controller's Office Employee Salary Data [origin_data_website](https://data.sfgov.org/City-Management-and-Ethics/Employee-Compensation/88g8-5mnd)

--------------------------------------------------
## ANALYTICS Part
The analysis process and data insights are in the ETL Jupyter Notebook  [sf_comp_jupyter_analytics.ipynb](/sf_comp_jupyter_analytics.ipynb)

### Scope and Assumption
This Analytics only considers 4 calendar years from 2018 to 2021.
Rows reduction from 759K to 168K, 
* (758604,22) ===> (168437, 22)
### columns info:
**Categorical Features:**
'organization_group_code', 
'job_family_code', 
'job_code', 
'year_type', 
'year', 
'organization_group', 
'department_code', 
'department', 
'union_code', 
'union', 
'job_family', 
'job', 
'employee_identifier', 

**Numerical Features:**
'salaries', 'overtime', 'other_salaries', 'total_salary', 'retirement', 'health_and_dental', 'other_benefits', 'total_benefits', 'total_compensation'
### Additional Details

Unique sample size in each categorical columns:
* Organization_group(6)
* department(51)
* job_family(56)
* job(1111)

Top 5 popular Job:
* Transit Operator 10805
* Special Nurse 6364
* Registered Nurse 5960
* Custodian 3438
* Firefighter 3077

--------------------------------------------------
## Dashboard Part Highlights
- API:
no username or password needed, query in API step to reduce the dataset size.
- Interactive Aggregate graph
Clients are able to choose the rank *top 5* or *bottom 5* to display.

- Next steps:
tore cleaned data to save load time
--------------------------------------------------
## My other dashboard projects

- ['Dirty' data clean ETL](https://github.com/susiexia/Movies-ETL/blob/master/movies_ETL.ipynb)
- [Deployed plotly Dashboard](https://susiexia.github.io/Plotly_Webpage/)
- [geoJSON Javascript project](https://github.com/susiexia/Mapping_Earthquakes)
- [Deployed Map URL:](https://susiexia.github.io/Mapping_Earthquakes/)
    * Traverse and retrieve GeoJSON data to populate an interactive geographical map about earthquakes and tectonic plates using JavaScript,leaflet.js libraries as well as Mapbox API.
- [another plotly Javascript project](https://github.com/susiexia/Plotly_Webpage)
