from config import API_Token
from sodapy import Socrata

import pandas as pd
import numpy as np
from scipy import stats

try:
    socrata_domain = 'data.sfgov.org,'
    socrata_dataset_identifier = '88g8-5mnd'
    client = Socrata("data.sfgov.org",API_Token)

    results = client.get_all(socrata_dataset_identifier, 
    where = "year in ('2018','2019','2020','2021','2022') and year_type = 'Calendar'" )

    df = pd.DataFrame(results)
    # print(df.shape)
    
except:
    df = pd.read_csv('plotly_dash/data/Employee_Compensation.csv')
    print('unable extract data by calling API, loading entire csv instead', df.shape)

def data_clean(df):
    # column transform
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    column_name = df.columns.tolist()
    # list and group columns
    numerical_column_names = [ 'year', 'salaries', 'overtime', 'other_salaries', 'total_salary', 
                    'retirement', 'health_and_dental', 'other_benefits', 'total_benefits', 'total_compensation']
    irrelavant_column_name = ['organization_group_code', 'job_family_code', 'job_code', 'year_type', 
                    'department_code',  'union_code', 'union']
    # change data type
    for column in column_name:
        if column in numerical_column_names:
            if column == 'year':
                df[column] = df[column].astype('int')
            else:
                df[column] = df[column].astype('float64')
    #print(df.dtypes)

    # drop off irrelevent information, records with negative and zero values 
    df.drop(irrelavant_column_name, axis=1, inplace=True)
    df.drop_duplicates(subset=['employee_identifier'], keep='last',ignore_index=True)
    df = df[(df['salaries']>=0)&(df['overtime']>=0)&(df['other_salaries']>=0)&(df['retirement']>=0)&(df['health_and_dental']>=0)&
                            (df['total_salary']>0)&(df['total_benefits']>0)&(df['total_compensation']>0)]
    # debug
    if not all((df['total_salary']!=0)&(df['total_benefits']!=0)&(df['total_compensation']!=0)):
        print('Please check the data duplicate section')
    
    #print(df.shape)

    # outliers
    def outlier_remove(df):
        outlier_df = df.copy()
        outlier_df['ts_zscore'] = np.abs(stats.zscore(outlier_df['total_salary']))
        outlier_df['tb_zscore'] = np.abs(stats.zscore(outlier_df['total_salary']))
        outlier_df['tc_zscore'] = np.abs(stats.zscore(outlier_df['total_compensation']))

        outlier_clean_df = outlier_df.loc[(outlier_df['ts_zscore']< 3)&(outlier_df['tb_zscore']< 3)&(outlier_df['tc_zscore']< 3)]
        outlier_clean_df= outlier_clean_df.drop(['ts_zscore','tb_zscore','tc_zscore'], axis=1)
        return outlier_clean_df
    
    # call
    res =  outlier_remove(df)
    print(res.shape)
    print('----------Data is clean----------')
    # output dataframes:
    return res

    # high_level_df = df.drop(['salaries', 'overtime', 'other_salaries',
    # 'retirement','health_and_dental', 'other_benefits'], axis =1)
    # return clean_df


if __name__ == '__main__':
    clean_df = data_clean(df)
    print(clean_df.shape)
