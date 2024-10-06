import pandas as pd
import numpy as np

df = pd.read_csv('rawpvr_2018-02-01_28d_1083 TueFri.csv')

def datainfo():
    print(df.head())
    # Analyse the Data type and change accordingly
    print("\nData Types:" )
    print(df.dtypes)
    """As a part of data preprocessing we are finding the Null values which 
           will be further processed."""
    print("\nNull Value: ")
    print(df.isnull().sum())
    print("\nDuplicates:")
    print(df.duplicated().sum())

def taskfilter():
    #filter just the tuesday
    df_tues = df[((df['Date'].dt.dayofweek +1 ) == 2)]
    #filter just the hour = 9
    df_hour = df_tues[(df_tues['Date'].dt.hour ==9)]
    #filter the direction to north and finally get (tuesday & 9 & north)
    df_south = df_hour[(df_hour['Direction Name'] == 'South')]
    #we can even do it as df_north[((df['Date'].dt.dayofweek +1 ) == 2)
    #               &(df['Date'].dt.hour ==9) & (df['Direction Name'] == 'North')]
    return df_south

def calculate_measure(df_temp):
    for lane,group in df_temp:
        stats ={
            'Range': df_temp['Speed (mph)'].max() - df_temp['Speed (mph)'].min(),
            'Q1': df_temp['Speed (mph)'].quantile(0.25),
            'Q2': df_temp['Speed (mph)'].median(),
            'Q3': df_temp['Speed (mph)'].quantile(0.75),
            'IQR': df_temp['Speed (mph)'].quantile(0.75) - df_temp['Speed (mph)'].quantile(0.25)
        }
    return stats

#datainfo()

#format of date is changed
df['Date'] = pd.to_datetime(df['Date'], format='ISO8601')

# Fill missing values in the 'Speed (mph)' column with the median speed
df['Speed (mph)'] = df['Speed (mph)'].fillna(df['Speed (mph)'].median())

#get the filtered data which has north, hour =9, day = tuesday
filter_south = taskfilter()

#group according to individual north lanes
group_south_lanes = filter_south.groupby('Lane Name')

df_stats = pd.DataFrame(calculate_measure(group_south_lanes))
print(df_stats)

