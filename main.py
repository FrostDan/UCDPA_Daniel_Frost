# IMPORT USEFUL LIBRARIES.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# GROUPBY FUNCTION CREATING ANNOYING 'FUTURE WARNING' ERRORS. SUPPRESS THESE ERRORS.
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# IMPORT DATASET 1 CSV BY NP.LOADTXT FROM LOCAL DRIVE.
csv1 = np.loadtxt("Passengers.csv", delimiter=",", dtype=str)
# CONVERT NP ARRAY INTO PD DATAFRAME
df1 = pd.DataFrame(csv1, columns = ['Year','Total','Domestic','International'])

# CHANGE TOTAL COLUMN TYPE TO FLOAT
df1['Total'] = df1['Total'].astype(float)

print(df1)

# DROP DOMESTIC AND INTERNATIONAL VALUES AS WE ARE INTERESTED IN TOTAL VALUES.
df1 = df1.drop('Domestic', axis=1)
df1 = df1.drop('International', axis=1)

# IMPORT DATASET 2 CSV BY URL AND SET AS DATAFRAME2 (DF2).
url2 = 'https://raw.githubusercontent.com/FrostDan/UCD_Data_Course/master/Air%20Emissions%201960-2020.csv'
data2 = pd.read_csv(url2)
df2 = pd.DataFrame(data2, columns=['LOCATION','INDICATOR','SUBJECT','MEASURE','FREQUENCY','TIME','Value','Flag Codes'])

# LOCATION CONTAINS GROUPS OF COUNTRIES SUCH AS 'G20' THAT ARE ALREADY LISTED AS INDIVIDUAL COUNTRIES.
# THIS DOUBLES THE VALUES FOR THOSE COUNTRIES AND CREATES ERRATIC SPIKES.
# REMOVE THESE GROUPS OF COUNTRIES.

df2 = df2[~df2.LOCATION.str.contains('EU27_2020')]
df2 = df2[~df2.LOCATION.str.contains('EU28')]
df2 = df2[~df2.LOCATION.str.contains('G20')]
df2 = df2[~df2.LOCATION.str.contains('G7M')]
df2 = df2[~df2.LOCATION.str.contains('EA19')]

# DROP UNNECESSARY VALUES - WE ONLY WISH TO KEEP MEASUREMENT, TIME AND VALUE.
df2  = df2.drop(['LOCATION','INDICATOR','SUBJECT','FREQUENCY','Flag Codes'], axis=1)

# DATASET CONTAINS MULTIPLE MEASUREMENTS. SLICE DATAFRAME TO ISOLATE SPECIFIC MEASUREMENT - MILLIONS OF TONNES.
df2 = df2.loc[(df2['MEASURE'] == 'MLN_TONNE'), ['TIME','Value']]

# GROUP VALUES BY YEAR TO SUM CONVERT INDIVIDUAL LOCATION VALUES INTO GLOBAL VALUES.
df2 = df2.groupby('TIME')['Value'].sum().reset_index()


# DATAFRAME 1 STARTS ITS YEAR VALUE AT 1980, WHEREAS DATAFRAME 2 STARTS ITS YEAR VALUE AT 1960.
# TO BRING DATASFRAMES INLINE WITH EACH OTHER, DROP ROWS 20 ROWS FROM DATAFRAME 2 TO REMOVE YEARS 1960-1979.
df2 = df2.drop(df2.index[range(20)])

# DATAFRAME 2 ENDS ITS YEAR VALUE WITH 2021, WHEREAS DATAFRAME 1 ENDS ITS YEAR VALUE AT 2020.
# TO BRING DATAFRAMES INLINE WITH EACH OTHER, DROP LAST ROW FROM DATAFRAME 2 TO REMOVE YEAR 2021.
df2 = df2.drop(df2.index[-1]).reset_index()

# INDEX WAS UNEXPECTEDLY TURNED INTO A COLUMN. REMOVE THIS UNWANTED COLUMN.
df2 = df2.drop('index', axis=1)


# EXTRACT VALUE COLUMN FROM DATAFRAME 2 IN ORDER TO MERGE IT INTO DATAFRAME 1
co2_Value = df2['Value']

# MERGE EXTRACTED COLUMN INTO DATAFRAME 1
df1.insert(1, 'Value', co2_Value)

# RENAME COLUMNS FOR CLARITY - 'PAX' REFERS TO PASSENGERS IN AVIATION.
df1.columns = ['Year', 'CO2', 'PAX']

# DIVIDE CO2 COLUMN VALUES BY 1000 TO CONVERT VALUE FROM MILLIONS TO BILLIONS
df1['CO2'] = df1['CO2']/1000

# ROUND CO2 AND FLIGHT VALUES TO 3 DECIMAL PLACES FOR SIMPLER ANALYSIS.
df1 = df1.round({'Year':0, 'CO2':3, 'PAX':3})

# YEAR COLUMN CONTAINS UNWANTED '*' CHARACTER ON YEARS 2019 AND 2020.
# CONVERT TYPE FROM FLOAT TO STRING IN ORDER TO REMOVE '*'.
df1['Year'] = df1['Year'].astype(str).str.extract('(\d+)')




# CREATE FIGURE AXIS WITH SUBPLOTS
fig,ax = plt.subplots()

# CREATE PLOT
ax.plot(df1.Year, df1.CO2, color="red", marker="x")

# SET X-AXIS LABEL
ax.set_xlabel("Year", fontsize = 14)

# SET Y-AXIS LABEL
ax.set_ylabel("CO2 (Gt)", color="red", fontsize=14)

# CREATE Z-AXIS (SECOND Y-AXIS)
ax2=ax.twinx()
ax2.plot(df1.Year, df1.PAX, df1["PAX"],color="blue",marker="x")
ax2.set_ylabel("PAX (bn)",color="blue",fontsize=14)

# USE FOR LOOP TO ROTATE X-AXIS LABELS
for tick in ax.get_xticklabels():
    tick.set_rotation(90)

ax.set_title('Compare CO2 to Passenger over Time')

ax.grid(True)
plt.show()


