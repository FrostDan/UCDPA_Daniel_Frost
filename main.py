# Import useful libraries.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Groupby function creating annoying 'Future Warning' errors. Suppress these errors.
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import dataset 1 CSV by np.loadtxt from local drive.
csv1 = np.loadtxt("Passengers.csv", delimiter=",", dtype=str)

# Convert np array into pd dataframe and name 'df1'.
df1 = pd.DataFrame(csv1, columns = ['Year','Total','Domestic','International'])

# Change 'Total' column type to float.
df1['Total'] = df1['Total'].astype(float)

# Drop 'Domestic' & 'International' columns as they are not required..
df1 = df1.drop('Domestic', axis=1)
df1 = df1.drop('International', axis=1)

# Import dataset 2 CSV by url, read url with pd.read_csv and name df2.
url2 = 'https://raw.githubusercontent.com/FrostDan/UCD_Data_Course/master/Air%20Emissions%201960-2020.csv'
data2 = pd.read_csv(url2)
df2 = pd.DataFrame(data2, columns=['LOCATION','INDICATOR','SUBJECT','MEASURE','FREQUENCY','TIME','Value','Flag Codes'])

# Location contains groups of countries such as 'G20' that are already listed as individual countries.
# This multiplies the values for those countries and creates erratic spikes.
# Remove these groups of countries.

df2 = df2[~df2.LOCATION.str.contains('EU27_2020')]
df2 = df2[~df2.LOCATION.str.contains('EU28')]
df2 = df2[~df2.LOCATION.str.contains('G20')]
df2 = df2[~df2.LOCATION.str.contains('G7M')]
df2 = df2[~df2.LOCATION.str.contains('EA19')]

# Drop unnecessary values - we only wish to keep 'MEASURE', 'TIME' and 'value'.
df2  = df2.drop(['LOCATION','INDICATOR','SUBJECT','FREQUENCY','Flag Codes'], axis=1)

# Dataset contains multiple measurements.
# Slice dataframe to isolate specific measurement - ‘MLN_TONNE’.
df2 = df2.loc[(df2['MEASURE'] == 'MLN_TONNE'), ['TIME','Value']]

# Group values by year to sum individual location values into global values.
df2 = df2.groupby('TIME')['Value'].sum().reset_index()


# Dataframe 1 starts its year value range at 1980, whereas dataframe 2 starts its year value range at 1960.
# To bring the two dataframes in-line with each other,
# Drop first 20 rows from dataframe 2 to remove year range 1960-1979.
df2 = df2.drop(df2.index[range(20)])

# Dataframe 2 ends its year range at 2021, whereas dataframe 1 ends its year range at 2020.
# To bring dataframes in-line with each other, drop last row from dataframe 2 to remove year 2021.
df2 = df2.drop(df2.index[-1]).reset_index()

# Index was unexpectedly turned into a column. Remove this unwanted column.
df2 = df2.drop('index', axis=1)


# Extract ‘Value’ column from dataframe 2 and name 'co2_Value' in order to merge it into dataframe 1.
co2_Value = df2['Value']

# Merge extracted 'co2_Value' column into dataframe 1.
df1.insert(1, 'Value', co2_Value)

# Rename columns for clarity.
# Note: 'PAX' refers to passengers in aviation.
df1.columns = ['Year', 'CO2', 'PAX']

# Divide 'CO2' column values by 1000 to convert value from millions to billions.
df1['CO2'] = df1['CO2']/1000

# Round ‘CO2’ and ‘PAX’ values to 3 decimal places for simpler analysis.
df1 = df1.round({'Year':0, 'CO2':3, 'PAX':3})

# ‘Year’ column contains unwanted '*' character on values: 2019 and 2020.
# Convert type from float to string in order to remove '*'.
df1['Year'] = df1['Year'].astype(str).str.extract('(\d+)')

# Create figure axis with plt.subplots.
fig,ax = plt.subplots()

# Create plot.
ax.plot(df1.Year, df1.CO2, color="red", marker="x")

# Set X-Axis label.
ax.set_xlabel("Year", fontsize = 14)

# Set Y-Axis label.
ax.set_ylabel("CO2 (Gt)", color="red", fontsize=14)

# Create Z-Axis (2nd Y-Axis)
ax2=ax.twinx()
ax2.plot(df1.Year, df1.PAX, df1["PAX"],color="blue",marker="x")

# Set Z-Axis label.
ax2.set_ylabel("PAX (bn)",color="blue",fontsize=14)

# Use FOR loop to rotate X-Axis labels.
for tick in ax.get_xticklabels():
    tick.set_rotation(90)

# Set graph title.
ax.set_title('Compare CO2 to Passenger over Time')

# Set both horizontal and vertical gridlines on graph.
ax.grid(True)

# Create graph.
plt.show()


