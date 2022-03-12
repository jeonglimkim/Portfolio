import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf


#Part 3 - Preparing Data
acs_data = pd.read_csv('./usa_00001.csv')
acs_data['EDUCD'].unique()

crosswalk = pd.read_csv('PPHA_30545_MP01-Crosswalk.csv')
crosswalk.head()

#create a continuous measure of education called educdc
crosswalk = pd.read_csv('PPHA_30545_MP01-Crosswalk.csv')
acs_data = acs_data.merge(crosswalk, left_on = 'EDUCD', right_on = 'educd')
acs_data.head()

acs_data = acs_data.drop(['educd'], axis = 1) 
acs_data = acs_data.rename(columns = {'educdc':'EDUCDC'}) #formatting
acs_data.head()

#create dummy variables
acs_data['EDUCD'].unique() #999 not in data 
acs_data['hsdip'] = np.where((acs_data['EDUCD'] > 61) & (acs_data['EDUCD'] < 101), 1, 0)  #high-school diploma
acs_data['coldip'] = np.where((acs_data['EDUCD'] > 100), 1, 0) #college degree

acs_data['white'] = np.where(acs_data['RACE'] == 1, 1, 0) #white
acs_data['black'] = np.where(acs_data['RACE'] == 2, 1, 0) #black

acs_data['hispanic'] = np.where(acs_data['HISPAN'] == 0, 0, 1) #hispanic

acs_data['married'] = np.where((acs_data['MARST'] == 1) | (acs_data['MARST'] == 2), 1, 0) #married

acs_data['female'] = np.where(acs_data['SEX'] == 2, 1, 0) #female

acs_data['vet'] = np.where(acs_data['VETSTAT'] == 2, 1, 0) #veteran

#interaction term
acs_data['EDUCDC*hsdip'] = acs_data['EDUCDC'] * acs_data['hsdip']
acs_data['EDUCDC*coldip'] = acs_data['EDUCDC'] * acs_data['coldip']

#create variables
acs_data['AGE_squared'] = acs_data['AGE'] ** 2

acs_data= acs_data[acs_data['INCWAGE'] != 0]
acs_data['INCWAGE_log'] = np.log(acs_data['INCWAGE'])


#Part 4 - Data Analysis
#1.compute descriptive(summary)statistics 
acs_data.columns
acs_data['YEAR'].describe()
acs_data['INCWAGE'].describe()
acs_data['INCWAGE_log'].describe()
acs_data['EDUCDC'].describe()
acs_data['female'].describe()
acs_data['AGE'].describe()
acs_data['AGE_squared'].describe()
acs_data['white'].describe()
acs_data['black'].describe()
acs_data['hispanic'].describe()
acs_data['married'].describe()
acs_data['NCHILD'].describe()
acs_data['vet'].describe()
acs_data['hsdip'].describe()
acs_data['coldip'].describe()
acs_data['EDUCDC*hsdip'].describe()
acs_data['EDUCDC*coldip'].describe()


#2.scatter plot ln (incwage) and education
plt.scatter(acs_data['EDUCDC'], acs_data['INCWAGE_log'], alpha=0.2, s=25)
sns.regplot(x="EDUCDC", y="INCWAGE_log", data=acs_data, line_kws={"color": "red"})
plt.title('Scatterplot for EDUCDC and INCWAGE_log')
plt.xlabel('Education')
plt.ylabel('Natural Log of Income Wage')


#3.new model
result = smf.ols('INCWAGE_log ~ EDUCDC + female + AGE + AGE_squared + white + black + hispanic + married + NCHILD + vet', data = acs_data).fit()
print(result.summary())


#3e # Does the model predict that men or women will have higher wages, all else equal?
acs_data['EDUCDC'].value_counts()
acs_data['AGE'].value_counts()

d = {'EDUCDC':[12], 'female':[0], 'AGE': [48], 'AGE_squared':[25**2], 'white':[1], 'black':[0], 'hispanic':[0], 'married':[0], 'NCHILD':[0], 'vet':[0]}
df = pd.DataFrame(data=d)
print(df)
predictions1 = result.get_prediction(df)
predictions1.summary_frame(alpha=0.05) #when male


d2 = {'EDUCDC':[12], 'female':[1], 'AGE': [48], 'AGE_squared':[25**2], 'white':[1], 'black':[0], 'hispanic':[0], 'married':[0], 'NCHILD':[0], 'vet':[0]}
df2 = pd.DataFrame(data=d2)
print(df2)
predictions2 = result.get_prediction(df2)
predictions2.summary_frame(alpha=0.05) #when female


#4. Graph ln(incwage) and education
acs_data['diploma'] = np.where(acs_data['hsdip'] == 0, 'no high school diploma', 'high school diploma')
acs_data['diploma'] = np.where(acs_data['coldip'] == 1, 'college diploma', acs_data['diploma'])
acs_data['diploma'].unique()


sns.lmplot(x="EDUCDC", 
           y="INCWAGE_log", 
           hue="diploma",
           ci=None,
           data=acs_data,
           height=10)
plt.title('Education vs Log Income Wage Based on the Receiving of Diploma')
plt.xlabel('Education')
plt.ylabel("Natural Log of Income Wage")


#5. Determine whether a college degree is a strong predictor of wages
q5result = smf.ols('INCWAGE_log ~ EDUCDC + hsdip + coldip + female + AGE + AGE_squared + white + black + hispanic + married + NCHILD + vet', data = acs_data).fit()
print(q5result.summary())

#6a
print(q5result.summary())

#6b
d3 = {'EDUCDC':[12], 'AGE': [22], 'hsdip':[1], 'coldip':[0], 'female':[1], 'AGE_squared':[22**2], 'white':[0], 'black':[0], 'hispanic':[0], 'married':[0], 'NCHILD':[0], 'vet':[0]}
df3 = pd.DataFrame(data=d3)
print(df3)
predictions3 = q5result.get_prediction(df3)
predictions3.summary_frame(alpha=0.05) #with high school degree


d4 = {'EDUCDC':[16], 'AGE': [22], 'hsdip':[0], 'coldip':[1], 'female':[1], 'AGE_squared':[22**2], 'white':[0], 'black':[0], 'hispanic':[0], 'married':[0], 'NCHILD':[0], 'vet':[0]}
df4 = pd.DataFrame(data=d4)
print(df4)
predictions4 = q5result.get_prediction(df4)
predictions4.summary_frame(alpha=0.05) #with college degree



