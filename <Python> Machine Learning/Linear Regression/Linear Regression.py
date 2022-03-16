import pandas as pd
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

path = "./Boston.csv"
df = pd.read_csv(path)

#Chapter 2 Question 10

#10a
df.shape #506 rows and 14 columns
df.info()
df.describe

#10b 
sns.pairplot(df)

#10c Are any of the predictors associated with per capita crime rate? If so, explain the relationship.
sns.pairplot(df[['CRIM', 'AGE', 'DIS', 'TAX', 'PTRATIO']])


#10d Do any of the suburbs of Boston appear to have particularly high crime rates? 
#Tax rates? Pupil-teacher ratios? Comment on the range of each predictor
sns.displot(df, x='CRIM') 
sns.displot(df, x='TAX')
sns.displot(df, x='PTRATIO')

#10e
len(df[df['CHAS'] == 1]) #35

#10f
df['PTRATIO'].median() #19.05

#10g Comment on your findings. 
df['MDEV'].min()
df['MDEV'].idxmin() # Suburb index 398
print(df.iloc[398])

#10h Comment on the suburbs that average more than eight rooms per dwelling. 
len(df[df['RM']>7]) #64
len(df[df['RM']>8]) #13
sns.displot(df, x='RM') 

#Chatper 3 Question 15
#a)
CRIMZN = smf.ols('CRIM ~ ZN', df).fit()
print(CRIMZN.summary())

CRIMINDUS = smf.ols('CRIM ~ INDUS', df).fit()
print(CRIMINDUS.summary())

CRIMCHAS = smf.ols('CRIM ~ CHAS', df).fit()
print(CRIMCHAS.summary())

CRIMNOX= smf.ols('CRIM ~ NOX', df).fit()
print(CRIMNOX.summary())

CRIMRM = smf.ols('CRIM ~ RM', df).fit()
print(CRIMRM.summary())

CRIMAGE = smf.ols('CRIM ~ AGE', df).fit()
print(CRIMAGE.summary())

CRIMDIS = smf.ols('CRIM ~ DIS', df).fit()
print(CRIMDIS.summary())

CRIMRAD = smf.ols('CRIM ~ RAD', df).fit()
print(CRIMRAD.summary())

CRIMTAX = smf.ols('CRIM ~ TAX', df).fit()
print(CRIMTAX.summary())

CRIMPTRATIO = smf.ols('CRIM ~ PTRATIO', df).fit()
print(CRIMPTRATIO.summary())

CRIMB = smf.ols('CRIM ~ B', df).fit()
print(CRIMB.summary())

CRIMLSTAT = smf.ols('CRIM ~ LSTAT', df).fit()
print(CRIMLSTAT.summary())

CRIMMDEV = smf.ols('CRIM ~ MDEV', df).fit()
print(CRIMMDEV.summary())

sns.pairplot(df[['CRIM', 'CHAS']])
sns.pairplot(df[['CRIM', 'RM']])

sns.regplot(x="CHAS", y="CRIM", data=df)
sns.regplot(x="RM", y="CRIM", data=df)


#b
predictors = ' + '.join(df.columns.difference(['CRIM']))
result = smf.ols('CRIM ~ {}'.format(predictors),data = df).fit()
print(result.summary())



#10c 
result = pd.read_html(result.summary().tables[1].as_html(),header=0,index_col=0)[0]
result

#10c attempt (hard-coding)
multi_AGE = result['coef'].values[1]
multi_B = result['coef'].values[2]
multi_CHAS = result['coef'].values[3]
multi_DIS = result['coef'].values[4]
multi_INDUS = result['coef'].values[5]
multi_LSTAT = result['coef'].values[6]
multi_MDEV = result['coef'].values[7]
multi_NOX = result['coef'].values[8]
multi_PTRATIO = result['coef'].values[9]
multi_RAD = result['coef'].values[10]
multi_RM = result['coef'].values[11]
multi_TAX = result['coef'].values[12]
multi_ZN = result['coef'].values[13]

lin_ZN = pd.read_html(CRIMZN.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_ZN = lin_ZN['coef'].values[1]
lin_ZN

lin_INDUS = pd.read_html(CRIMINDUS.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_INDUS = lin_INDUS['coef'].values[1]
lin_INDUS

lin_CHAS = pd.read_html(CRIMCHAS.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_CHAS = lin_CHAS['coef'].values[1]
lin_CHAS

lin_NOX = pd.read_html(CRIMNOX.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_NOX = lin_NOX['coef'].values[1]
lin_NOX

lin_RM = pd.read_html(CRIMRM.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_RM = lin_RM['coef'].values[1]
lin_RM

lin_AGE = pd.read_html(CRIMAGE.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_AGE = lin_AGE['coef'].values[1]
lin_AGE

lin_DIS = pd.read_html(CRIMDIS.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_DIS = lin_DIS['coef'].values[1]
lin_DIS

lin_RAD = pd.read_html(CRIMRAD.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_RAD = lin_RAD['coef'].values[1]
lin_RAD

lin_TAX = pd.read_html(CRIMTAX.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_TAX = lin_TAX['coef'].values[1]
lin_TAX

lin_PTRATIO= pd.read_html(CRIMPTRATIO.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_PTRATIO = lin_PTRATIO['coef'].values[1]
lin_PTRATIO

lin_B = pd.read_html(CRIMB.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_B = lin_B['coef'].values[1]
lin_B

lin_LSTAT = pd.read_html(CRIMLSTAT.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_LSTAT= lin_LSTAT['coef'].values[1]
lin_LSTAT

lin_MDEV = pd.read_html(CRIMMDEV.summary().tables[1].as_html(),header=0,index_col=0)[0]
lin_MDEV = lin_MDEV['coef'].values[1]
lin_MDEV

lin = np.array([lin_AGE, lin_B, lin_CHAS, lin_DIS, lin_INDUS, 
                lin_LSTAT, lin_MDEV, lin_NOX, lin_PTRATIO, 
                lin_RAD, lin_RM, lin_TAX, lin_ZN])

multi = np.array([multi_AGE, multi_B, multi_CHAS, multi_DIS, multi_INDUS, 
                multi_LSTAT, multi_MDEV, multi_NOX, multi_PTRATIO, 
                multi_RAD, multi_RM, multi_TAX, multi_ZN])


plt.scatter(lin, multi)
plt.xlabel("Linear Regression Coefficients")
plt.ylabel("Multiple Regression Coefficients")
plt.show()



#10d
model_ZN = smf.ols('CRIM ~ ZN + np.power(ZN,2) + np.power(ZN, 3)'.format(predictors), data = df).fit()
print(model_ZN.summary())

model_NOX = smf.ols('CRIM ~ NOX + np.power(NOX,2) + np.power(NOX, 3)'.format(predictors), data = df).fit()
print(model_NOX.summary())

model_DIS = smf.ols('CRIM ~ DIS + np.power(DIS,2) + np.power(DIS, 3)'.format(predictors), data = df).fit()
print(model_DIS.summary())

model_RAD = smf.ols('CRIM ~ RAD + np.power(RAD,2) + np.power(RAD, 3)'.format(predictors), data = df).fit()
print(model_RAD.summary())

model_MDEV = smf.ols('CRIM ~ MDEV + np.power(MDEV,2) + np.power(MDEV, 3)'.format(predictors), data = df).fit()
print(model_MDEV.summary())

    


