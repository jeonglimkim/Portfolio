# To answer these questions, you will use the two csv documents included in your repo.  In nst-est2019-alldata.csv:
# SUMLEV is the level of aggregation, where 10 is the whole US, 20 is a US region, and 40 is a US state.
# REGION is the fips code for the US region
# STATE is the fips code for the US state
# The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2019/nst-est2019-alldata.pdf


# Question 1: Load the population estimates file into a dataframe. Specify an absolute path using the Python os library
# so that anyone who clones your homework repo into the default location on their computer, which is THEIR current
# working directory, Documents, GitHub, your-repo-name, (e.g. c:\users\jeff\documents\github\your-rep) can open it without
# changing anything.  Then show code doing some basic exploration of the dataframe.


import os
import pandas as pd

# os.getcwd()
# os.listdir()
# os.chdir("/Users/Jenny/Desktop/Github/homework-4-jeonglimkim/nst-est2019-alldata.csv")

path = "/Users/Jenny/Desktop/Github/homework-4-jeonglimkim"
popest = pd.read_csv(os.path.join(path, 'nst-est2019-alldata.csv'))
popest

popest.head()
popest.tail()
popest['STATE']
popest['SUMLEV']


# Question 2: Your data only includes fips codes for states.  Use the us library to crosswalk fips codes to state
# abbreviations.  Keep only the state abbreviations in your data.

import us

fipscode = us.states.mapping('fips', 'abbr')
fipscode

del fipscode[None] 

fipscode = {int(k):v for k,v in fipscode.items()}
fipscode

popest = popest.replace({"STATE":fipscode})
popest


# Question 3: Subset the data so that only observations for individual US states remain, and only state names and data
# for the population estimates in 2010-2019 remain.

onlystates = popest.loc[popest['SUMLEV'] == 40]
onlystates = onlystates.iloc[:, 2:15]
onlystates = onlystates.drop(['CENSUS2010POP','ESTIMATESBASE2010'],axis=1)
onlystates


# Question 4: Reshape the data from wide to long, making sure you reset the index to the default values if any of your
# data is located in the index.

reshape = pd.wide_to_long(onlystates, stubnames = "POPESTIMATE", i = "STATE", j = "Year").reset_index()
reshape

# Question 5: Open the state-visits.csv file, and fill in the VISITED column with a dummy variable for whether you've visited
# a state or not.  If you haven't been to many states, then filling in a random selection of them is fine too; this isn't
# actually a travel log!  Save your changes.  Then load the file as a dataframe in Python, and merge the visited column
# into your population dataframe, only keeping values that appear in both dataframes.  Are any observations dropped from this?
# Show code where you investigate your merge, and display any observations that weren't in both dataframes.

path = "/Users/Jenny/Desktop/Github/homework-4-jeonglimkim"
visits = pd.read_csv(os.path.join(path,"state-visits.csv"))
visits = pd.DataFrame(visits)
visits

reshape1 = reshape.merge(visits, on = "STATE", how = 'inner')
len(reshape) #520
len(reshape1) #510
#My observation did drop. 

# Question 6: Using groupby, calculate the rate of change from year to year for the population of all US states.

group1 = reshape1.set_index(['STATE', 'Year']).POPESTIMATE
group2 = group1.groupby('STATE').pct_change()
group2


# Question 7: Continuing to use groupby, sum the 2019 populations of all the states you have not been to, and compare it to
# the states you been to.   Have you visited the home state of the majority of Americans?

only2019 = reshape1.loc[reshape1['Year'] == 2019]
group3 = only2019.set_index(['STATE','Year'])
group4 = group3.groupby(['VISITED'])["POPESTIMATE"].sum()
group4

#Not visited = 129489266
#Visited = 198750257
#I have visited the home state of the majority of Americans.






