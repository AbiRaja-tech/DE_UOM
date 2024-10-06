import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('rawpvr_2018-02-01_28d_1083 TueFri.csv')

def datainfo():
    print(df.head())
    print("\nData Types:" )
    print(df.dtypes)
    print("\nNull Value: ")
    print(df.isnull().sum())
    print("\nDuplicates:")
    print(df.duplicated().sum())

def taskfiltertuesfri(i):
    """
        To filter only the data entires that satisfies the condition,
            Condition:
                1) Tuesday or Friday
                2) Between 7 and 24

        Will return the Data frame that satisfy the condition
    :param i:
    :return:
    """
    #filter based on i i=1(Tuesday) and i=-3(Friday)
    if i == 1:
        df_tues = df[((df['Date'].dt.dayofweek + 1) == 2)]
    else:
        df_tues = df[((df['Date'].dt.dayofweek + 1) == 5)]
    #filter for hours between 7 AM and midnight
    df_hour = df_tues[(df_tues['Date'].dt.hour >= 7) & (df_tues['Date'].dt.hour < 24)]
    return df_hour

def gen_hour_traff(df_hour_traff):
    """Calculate the Traffic volume of each hour

       Get the filtered data and run a group by followed by the size to get
       the number of vehicles in an hour(Traffic Volume)
    """
    stats = df_hour_traff.groupby(df_hour_traff['Date'].dt.hour).size()
    return stats

#format of date is changed
df['Date'] = pd.to_datetime(df['Date'], format='ISO8601')

filter_tues = taskfiltertuesfri(1)
filter_fri = taskfiltertuesfri(2)

Hour_Vol_Tues = gen_hour_traff(filter_tues)
Hour_Vol_Fri = gen_hour_traff(filter_fri)

# Plotting the results
plt.figure(figsize=(10, 6))

# Plot Tuesday's traffic volume
plt.plot(Hour_Vol_Tues.index, Hour_Vol_Tues.values, marker='o', linestyle='-', color='b', label='Tuesday')

# Plot Friday's traffic volume
plt.plot(Hour_Vol_Fri.index, Hour_Vol_Fri.values, marker='o', linestyle='-', color='r', label='Friday')

# Add titles and labels
plt.title('Traffic Volume by Hour on Tuesday and Friday')
plt.xlabel('Hour of the Day')
plt.ylabel('Traffic Volume')
plt.xticks(range(7, 24))  # Set x-ticks to show hours from 7 to 23
plt.legend(title='Day')
plt.grid(True)

# Display the plot
plt.show()

print("\n\nAverage Traffic Volume Per Hour:")
print(f"Tuesday: {sum(Hour_Vol_Tues.values) / len(Hour_Vol_Tues):.2f}")
print(f"Friday: {sum(Hour_Vol_Fri.values) / len(Hour_Vol_Fri):.2f}")