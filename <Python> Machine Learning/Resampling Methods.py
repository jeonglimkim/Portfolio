import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score

import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('/Users/Jenny/Desktop/Machine Learning/Problem Set/Problem Set 3')

#Chapter 5 Question 6
#a)
default = pd.read_csv('./Data-Default.csv', index_col=0)
default.head()
default.shape

encoding_dict = {'Yes':1, 'No':0}
default['default'] = default['default'].map(encoding_dict)
default.head()

X = default[['balance', 'income']]
X = sm.add_constant(X)
y = default['default']
results = sm.Logit(y, X).fit()
print(results.summary())

#b)
#Bootstrapping
np.random.seed(1)
def get_indices(data, num_samples):
    positive_data = data[data['default'] == 1]
    negative_data = data[data['default'] == 0]
    
    positive_indices = np.random.choice(positive_data.index, int(num_samples/4), replace = True)
    negative_indices = np.random.choice(negative_data.index, int(30*num_samples/4), replace = True)
    total = np.concatenate([positive_indices, negative_indices])
    np.random.shuffle(total)
    return total

def boot_fn(data, index):
    X = data[['balance', 'income']].loc[index]
    y = data['default'].loc[index]
    
    lr = LogisticRegression()
    lr.fit(X, y)
    intercept = lr.intercept_
    coef_balance = lr.coef_[0][0]
    coef_income = lr.coef_[0][1]
    return[intercept, coef_balance, coef_income]

intercept, coef_balance, coef_income = boot_fn(default, get_indices(default, 10))
print('Intercept is {}, the coeff of balance is {} , the coeff for income is {} '.format(intercept,coef_balance,coef_income))

#c)
np.random.seed(1)
def boot(data,func,R):
    intercept = []
    coeff_balance = []
    coeff_income = []
    for i in range(R):
        
        [inter,balance,income] = func(data,get_indices(data,100))
        intercept.append(float(inter))
        coeff_balance.append(balance)
        coeff_income.append(income)
        
    intercept_statistics = {'estimated_value':np.mean(intercept),'std_error':np.std(intercept)}   
    balance_statistics = {'estimated_value':np.mean(coeff_balance),'std_error':np.std(coeff_balance)}
    income_statistics = {'estimated_value':np.mean(coeff_income),'std_error':np.std(coeff_income)}
    return {'intercept':intercept_statistics,'balance_statistices':balance_statistics,'income_statistics':income_statistics}

results = boot(default,boot_fn,1000)
print('Balance - ',results['balance_statistices'])
print('Income - ', results['income_statistics'])


# Chapter 5 Question 8
#a) 
#Generating a simulated data set
np.random.seed(1)
y = np.random.normal(size = 100)
X = np.random.normal(size = 100)
y = X - 2 * (X ** 2) + np.random.normal(size = 100)

#n=100, p=2

#b) 
sns.scatterplot(X, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot')

#c)
np.random.seed(1)
for i in range(1, 5):
    poly = PolynomialFeatures(i, include_bias=False)
    predictors = poly.fit_transform(X.reshape(-1, 1))
    
    lr = LinearRegression()
    error = -1 * cross_val_score(lr, predictors, y, cv = len(X), scoring = 'neg_mean_squared_error').mean()
    print(f'For model {i}, error is {error}'.format(i, error))


#d)
np.random.seed(2)
for i in range(1, 5):
    poly = PolynomialFeatures(i, include_bias=False)
    predictors = poly.fit_transform(X.reshape(-1, 1))
    
    lr = LinearRegression()
    error = -1 * cross_val_score(lr, predictors, y, cv = len(X), scoring = 'neg_mean_squared_error').mean()
    print(f'For model {i}, error is {error}')


#f)
for i in range(1,5):
    poly = PolynomialFeatures(i)
    predictors = poly.fit_transform(X.reshape(-1,1))

    results = sm.OLS(y,predictors).fit()
    print(results.summary())

#Chatper 6 Question 11
#a) 
boston = pd.read_csv('./Boston.csv', index_col=0)
boston = boston.reset_index()
boston.columns

predictors = boston.drop('CRIM',axis = 1)
y = boston['CRIM']
predictors.head()

results_dict = {}

#best subset
hand_selected_features = ['NOX','DIS','RAD','LSTAT']

lin_reg = LinearRegression()
error = cross_val_score(lin_reg,predictors, y, cv = 5, scoring = 'neg_mean_squared_error')
print('Error for best subset selection is ',-np.mean(error))
results_dict['Best_subset'] = -np.mean(error)





#forward stepwise

from sklearn.datasets import load_boston

boston = load_boston()
data = pd.DataFrame(boston.data,columns = boston.feature_names)
X = data.drop('CRIM',axis = 1)
y = data['CRIM']

lin_reg = LinearRegression()

P = len(X.columns)
used_pred = []
M = []
M_scores = []

for K in range(P):
    best_score = -1000
    best_pred = None
        
    # Inner loop
    for var in X.columns:
            
        # Skips if predictor already used
        if var not in used_pred:
            predictors = used_pred[:]   
            predictors.append(var)
            
            score = np.mean(cross_val_score(lin_reg, X[predictors], y, cv = 5, scoring = 'neg_mean_squared_error'))
            if score > best_score:
                best_score = score
                best_pred = var
    
    # Updates the list of used predictors and list of Mk models
    used_pred.append(best_pred)
    M.append(used_pred)
    M_scores.append(best_score)                             
    
best_M = M_scores.index(max(M_scores))
print('Predictors that make the best model are: ', M[best_M])


#backward stepwise













