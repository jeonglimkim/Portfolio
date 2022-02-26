import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Question 1
#Use Pandas and the os.listdir function to load the six .csv documents into dataframes.  The first
#two characters of each file name is a state, the second two (UR) refers to the unemployment rate.
#Write your code so that it will work generally with any file in this folder, with this naming
#convention.  For example, your code should work with these six files, but if a file for a seventh
#state was added, your code would automatically include it.

path = "/Users/Jenny/Desktop/Github/homework-5-jeonglimkim"
files = os.listdir(path)
files = [f for f in files if (f.endswith("UR.csv"))]

dfs = list()

for csvfile in files:
    fpath = path + '/' + csvfile
    df = pd.read_csv(fpath)
    dfs.append(df)

dfs


# Question 2
#Turn all string columns that contain dates into datetime datatypes.  This can be done in the
#loading of part 1, or after.

for df in dfs:
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
        
print (df.dtypes)


# Question 3
#Concatenate all six dataframes (making other changes as necessary) so that each row represents
#a unique state-date combination.  The resulting dataframe should have only the
#columns: state, date, unemp_rate

pd.concat(dfs)



# Question 4
#Use groupby to calculate the mean unemployment rate over this period for each of the six states,
#and print all six results.




# Question 5
#Three of the states (CA, OR, WA) are on the west coast, while the other three (MI, WI and IL)
#are in the midwest.  Create a new column named "region" that labels each row with the correct
#region.  Then group your data by the two regions and plot them on one graph.  Make the lines
#different colors and include a legend.  You can use MatPlotLib, Seaborn, the Pandas plot
#method, or a combination.  Save the single plot as a file that you commit with your code.





















