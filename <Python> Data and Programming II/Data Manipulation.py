# 1. The two datasets included in the assignment repo are downloaded directly from the BEA.  The file
# labeled "total" has the total employment per state for the years 2000 and 2017.  The file labeled
# "by industry" has employment per industry in each of 10 industries per state for the same years.
#
# Load and merge the data into a panel dataframe, with the columns: "state", "year", and one for each
# of the 10 industries.  Every state-year combination should uniquely identify a row.  No more and no
# less than 12 columns should remain.  Do any necessary cleaning for the data to be easily usable.
#
# The values should be given as the share of the total employment in that place and time, e.g. if
# total employment in a place and time was 100, and the employment in one industry was 10, then the
# value shown for that state-year industry should be 0.1.
#
# Output this dataframe to a csv document named "data.csv" and sync it to your homework repo with
# your code.

import pandas as pd

#By Industry Employment_Reshaping
path1 = "./SAEMP25N by industry.csv"
industry = pd.read_csv(path1,
                       skiprows = 4,
                       na_values=['(T)', '(D)'])

industry
industry.columns
industry.dtypes
industry.head()
industry.tail()

industry = industry.drop(['GeoFips','LineCode'], axis = 1)
industry.drop(industry.tail(5).index,inplace=True)
industry = industry.dropna(subset=['2000','2017'], how="all")
industry = industry.rename(columns = {"GeoName":"State"})


#Total Industry Employment_Reshaping
path2 = "./SAEMP25N total.csv"

total = pd.read_csv(path2,
                    skiprows = 4)

total
total.head()
total.tail()

total = total.drop(['GeoFips'], axis=1)
total = total.dropna()
total = total.rename(columns = {"GeoName":"State"})


#Calculate the share of the total employment
new = industry.merge(total, on="State")
new["2000"] = new["2000_x"]/new["2000_y"]
new["2017"] = new["2017_x"]/new["2017_y"]
new = new.drop(['2000_x','2017_x','2000_y','2017_y'],axis=1)
new

employment = new.pivot_table(index= "State",
                             columns = "Description"
                             )

Year2000 = employment["2000"]
Year2017 = employment["2017"]
Year2000['Year'] = '2000'
Year2017['Year'] = '2017'

employment = pd.concat([Year2000,Year2017])
employment.groupby(['State', 'Year']).sum()

employment = employment.reset_index()

employment.columns
employment.columns = employment.columns.str.strip()

employment


#Export it to csv file
employment.to_csv('./data.csv')


# 2. Using the dataset you created, answer the following questions:
#
# a. Find the states with the top five share of manufacturing employment in the year 2000, then show
# how their share of employment in manufacturing changed between 2000 and 2017.  Use a basic plot to
# display the information.
#
# b. Show which five states have the highest concentration of employment in a single industry in each
# of 2000 and 2017, and what those industries are.


import seaborn as sns

# a. 
path3 = "./data.csv"

data = pd.read_csv(path3,
                   index_col=0)

manu = data.sort_values('Manufacturing', ascending = False).groupby(['Year']).head(5)
manu_states = manu.iloc[0:5, 0].tolist()

manu = data[data.State.isin(manu_states)]

graph = sns.lineplot(x='Year', 
                     y='Manufacturing',
                     hue="State",
                     data=manu, 
                     ci=None)

# b. 
data_reshaped = data.melt(id_vars=['State', 'Year'], var_name='Industry', value_name='Share of Employment')

data_reshaped = pd.pivot_table(data_reshaped, index=['State', 'Industry'], columns='Year', values='Share of Employment')

data_reshaped = data_reshaped.reset_index()

def top5(df, col):
    output = df.nlargest(5, col)
    print(output[['State','Industry']])

top5(data_reshaped, 2000)
top5(data_reshaped, 2017)
