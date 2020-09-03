
import pandas as pd
import numpy as np

"""Script to estimate monthly electricity usage costs for each household (meter_id), for 
meter readings contained in 'meter_readings.csv'.

The output of the script is a printed table showing the estimated costs.

This script requires `pandas` and 'numpy' to be installed within the Python
environment you are running this script in.

"""

def main():

    #read csv file
    data = pd.read_csv('ee_coding_challenge_dataset.csv')
    df = pd.DataFrame(data)

    #create DatTimeIndex
    df['DateTime'] = pd.to_datetime(df['DateTime'], dayfirst = True)
    df.set_index(pd.DatetimeIndex(df['DateTime']), inplace = True) 
    df.drop(columns = ['DateTime'], inplace = True)

    # clean data by removing consumption reading errors
    df = df[(df['consumption']>0) & (df['consumption']<3) & (df['consumption']!=0)]

    # Add 'Month' and 'Year' columns
    df['Month'] = df.index.month
    df['Year'] = df.index.strftime("%Y")

    grouped_df = pd.DataFrame(df.groupby(['meter_id', 'Month', 'Year'])[['consumption']].sum())
    grouped_df.reset_index(inplace = True)

    # Estimate usage cost with flat rate
    grouped_df['Electricity cost (£) on current flat rate tariff'] = grouped_df['consumption']*0.15
    
    # Convert month number to name
    grouped_df['Month'] = grouped_df['Month'].apply(month_name)

    # Drop consumption column
    grouped_df.drop(columns = ['consumption'], inplace = True)

    # Print desired table showing estimated usage costs based on flat rate
    print(grouped_df)

def month_name(num):
    
    """Converts month number to name. 
    This allows the use of vectorized operations when combined with .apply() function"""
    
    month_dict = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'\
                  , 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    
    return month_dict[num]

if __name__ == "__main__":
    main()
