
"""Script to filter meter readings contained in 'meter_readings.csv'

This script allows the user to meter readings by meter_id, month and year based on user inputs into the console.

Example of inputting months for February (2nd month), April (4th month) and May (5th month) would be: 2,4,5

Example of inputting the years 2012 and 2013 would be: 2012, 2013

This script requires that `pandas` and 'numpy' to be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * clean_consumption_data
    * filter_meter_data
    * Filter_month
    * filter_year
    * main - the main function of the script
"""

import pandas as pd
import numpy as np

def main():
    
    data = pd.read_csv('ee_coding_challenge_dataset.csv')
    df = pd.DataFrame(data)
    
    df = clean_consumption_data(df)

    df['DateTime'] = pd.to_datetime(df['DateTime'], dayfirst=True)
    df.set_index(pd.DatetimeIndex(df['DateTime']), inplace = True) 
    df.drop(columns = ['DateTime'], inplace = True)

    user_input = ''
    
    user_input = input('Would you like to filter by meter_id? [y/n]')
    
    while user_input not in {'Y', 'y', 'N', 'n'}:
        user_input = input('Please select [y/n].')
    
    if user_input in {'y', 'Y'}:
        user_input = input('Please enter the meter_id.')
        df_filter = filter_meter_id(df, user_input)
        
    elif user_input in {'n', 'N'}:
        df_filter = df
        pass
     

    user_input = input('Would you like to filter by month [y/n]?')

    while user_input not in {'Y', 'y', 'N', 'n'}:
        user_input = input('Please select [y/n].')
    
    if user_input in {'y', 'Y'}:
        user_input = input('Please enter the numbers of the months separated by commas.')
        df_filter = filter_month(df_filter, user_input)
    
    elif user_input in {'n', 'N'}:
        pass

    user_input = input('Would you like to filter by year? [y/n]')

    while user_input not in {'Y', 'y', 'N', 'n'}:
        user_input = input('Please select [y/n].')
    
    if user_input in {'y', 'Y'}:
        user_input = input('Please enter the numbers of the years separated by commas (data only exists for 2013).')
        df_filter = filter_year(df_filter, user_input)
    
    elif user_input in {'n', 'N'}:
        pass
    
    print(df_filter)

def clean_consumption_data(df):
    
    """Takes in a dataframe containg meter readings and removes all rows in which:
        
        * consumption reading is below 0 (not possible)
        * consumption reading is above 3 (too high)
        * consumption reading is equal to zero (generally not possible)
    """
    
    df = df[(df['consumption']>0) & (df['consumption']<3) & (df['consumption']!=0)]
    
    return df

def filter_meter_id(df, m_id):
    
    """Takes in a dataframe containg meter readings and removes all rows that do not have the 
    meter_id specified
    
    """
    return df[df['meter_id'] == str(m_id)]

def filter_month(df, months):
    
    
    """Takes in a series of comma-separated numbers representing months (i.e. January = 1) and filters the dataframe 
    based on the numbers provided.
    
    """
    
    return df[df.index.month.isin([int(month) for month in months.split(',')])]

def filter_year(df, years):
    
    
    """Takes in a series of comma-separated numbers representing years (i.e. 2014, 2015) and filters the dataframe 
    based on the numbers provided.
    """
    
    return df[df.index.year.isin([int(year) for year in years.split(',')])]


if __name__ == "__main__":
    main()
