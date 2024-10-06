import matplotlib.pyplot as plt
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

    return df_hour

def calculate_tvol(df_traffvol):
    df_traffvol = df_traffvol.size()
    df_traffvol = df_traffvol.reset_index(name='Volume')
    stats_temp = {
        'Range': df_traffvol['Volume'].max() - df_traffvol['Volume'].min(),
        'Q1': df_traffvol['Volume'].quantile(0.25),
        'Q2':df_traffvol['Volume'].median(),
        'Q3': df_traffvol['Volume'].quantile(0.75),
        'IQR': df_traffvol['Volume'].quantile(0.75) - df_traffvol['Volume'].quantile(0.25)
    }
    return stats_temp

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


def calculate_measures(df_temp, group_by_column, target_column):
    """
    Calculate statistical measures for a specific column grouped by another column.

    Input:
    df (pd.DataFrame): DataFrame containing the data.
    group_by_column (str): Column name to group by (e.g., 'Lane Name').
    target_column (str): Column name for which to calculate statistics (e.g., 'Speed (mph)', 'Traffic Volume').

    Step 1: Group the values according to the desired column
    Step 2: Initialize a Dictionary
    Step 3: Append values according to the dictionary(Eg: Group Name, Range,etc,.)
    Step 4: Convert the Dictionary to Dataframe
    Step 5: Return the Dataframe to the main function
    """
    # Group by the specified column
    grouped = df_temp.groupby(group_by_column)

    # Create a dictionary to store the stats for each group
    stats_dict = {
        'Group': [],
        'Range': [],
        'Q1': [],
        'Q2': [],
        'Q3': [],
        'IQR': []
    }

    # Loop through each group and calculate the statistics
    for group, data in grouped:
        stats_dict['Group'].append(group)
        stats_dict['Range'].append(data[target_column].max() - data[target_column].min())
        stats_dict['Q1'].append(data[target_column].quantile(0.25))
        stats_dict['Q2'].append(data[target_column].median())
        stats_dict['Q3'].append(data[target_column].quantile(0.75))
        stats_dict['IQR'].append(data[target_column].quantile(0.75) - data[target_column].quantile(0.25))

    # Convert the dictionary to a DataFrame for easier handling and visualization
    stats_df = pd.DataFrame(stats_dict)

    return stats_df


def lane_traffvol_speed_stat():
        """
        Calculate the Traffic volume of each lane and the speed of the cars
        in each lane

        Input: The filtered dataframe is used.(Dataframe which has only Tuesday
                                               9 to 9:59:59 values)

            Step 1: Group by Lane Name and the number of vehicles in each Lane
            Step 2: Group by Lane Name and the Avg Speed of vehicles in each Lane
            Step 3: Pass the details in form of Data frame with 'Lane Name',
                    'Traffic Volume' and 'Avg Speed (mph)'.
            Step 4: We will be plotting the data
                    Step 4.1: We will plot considering X axis: Avg Speed(mph)
                                                       Y axis: Traffic Volume
                    Step 4.2: Define each points(i.e, NB_MID, NB_MIS,etc.)
        """
        #Number vehicles in each lanes accordingly
        grp_traffvol_lane = df_datetime.groupby('Lane Name').size()
        #Avg Speed of Vehicles according to the Lane
        grp_speed_lane = df_datetime.groupby('Lane Name')['Speed (mph)'].mean()

        # Calculating Measures for 'Speed (mph)' grouped by 'Lane Name'
        stats_speed = calculate_measures(df_datetime, 'Lane Name', 'Speed (mph)')
        print(stats_speed)

        lane_stats = pd.DataFrame({
            'Lane Name': grp_traffvol_lane.index,
            'Traffic Volume': grp_traffvol_lane,
            'Avg Speed (mph)': grp_speed_lane
        })
        print(lane_stats)
        plt.figure(figsize=(10,6))
        plt.plot(lane_stats['Avg Speed (mph)'], lane_stats['Traffic Volume'], marker = 'o',linestyle='-',color='b')
        for i, row in lane_stats.iterrows():
            plt.text(row['Avg Speed (mph)'], row['Traffic Volume'], row['Lane Name'], fontsize=9, ha='right')
        plt.title('Traffic Volume vs Avg Speed per Lane')
        plt.xlabel('Avg Speed (mph)')
        plt.ylabel('Traffic Volume')
        plt.grid(True)
        plt.show()

def traffvol_hour_stat():
    """
        Calculate the Traffic Volume on each Lanes around the hour(from 0 to 24)

        Input: We will be using the unfiltered Dataframe is used
            Step 1: Get the hour at which each car has travelled(or recorded)
            Step 2: The Number of Cars in each lane at that particular hour.
            Step 3: With the help of pivot table structure the desired plot
            Step 4: PLot the Table
                    Step 4.1: We will plot considering X axis: Hour of the Day
                                                       Y axis: Traffic Volume
    :return:
    """
    #The hour at which each vehicle was recorded
    df['Hour'] = df['Date'].dt.hour
    #Number of vehicels in each lane at that point of time(In this case Hour)
    traff_by_hour_lane = df.groupby(['Lane Name', 'Hour']).size().reset_index(name='Traffic Volume')

    #Calculating Measures for 'Traffic Volume' grouped by 'Lane Name' and 'Hour'
    stats_df = calculate_measures(traff_by_hour_lane, ['Lane Name', 'Hour'], 'Traffic Volume')
    print(stats_df)

    #Here we have used pivot , for easier plotting (Row -Hour, Column - Lane Name
    pivot_table = traff_by_hour_lane.pivot(index='Hour', columns='Lane Name', values='Traffic Volume')
    plt.figure(figsize=(10, 6))

    #Traffic volume for each lane is plotted
    for lane in pivot_table.columns:
        plt.plot(pivot_table.index, pivot_table[lane], marker='o', linestyle='-', label=lane)
    plt.title('Traffic Volume by Hour for Each Lane')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Traffic Volume')
    plt.xticks(range(24))
    plt.legend(title='Lane Name')
    plt.grid(True)
    plt.show()

#format of date is changed
df['Date'] = pd.to_datetime(df['Date'], format='ISO8601')

df_datetime = taskfilter()

#This gives the visualization for Traffic Volume in each Lane Vs Avg Speed
lane_traffvol_speed_stat()

#This gives visualization for Traffic Volume by hour for each lane
traffvol_hour_stat()

