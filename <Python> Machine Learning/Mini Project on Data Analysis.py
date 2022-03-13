import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
import matplotlib.pyplot as plt


#3 Data Analysis
#1.

vardesc = pd.read_excel('./Variable Description.xlsx')
vardesc = vardesc.drop([0,1])
vardesc.drop(['Description', 'Source'], axis=1, inplace=True)
vardesc = vardesc.pivot(index='Count', columns='Variable', values='Count' )

data = pd.read_csv("Covid002.csv", encoding = "ISO-8859-1")
data.shape

#source: https://stackoverflow.com/questions/26152556/drop-columns-that-arent-common-between-two-dataframes
common_cols = list(set(vardesc.columns).intersection(data.columns))
df = data[common_cols]
df['county'] = data['county']
df['state'] = data['state'] 
df['deathspc'] = data['deathspc']

#2. 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df.describe()

#3. 
df = df.dropna()
df.shape

#4. 
X = df.copy()
X = pd.get_dummies(X, columns = ['state'])
X.shape
X.head()

#5. 
y = X.pop('deathspc')
X.drop(['county', 'state_Wyoming'], axis=1, inplace=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#6. 
reg = LinearRegression().fit(X_train, y_train)
reg.coef_
print(reg.score(X_train, y_train)) #training Rsquared 0.41285556413534596
print(reg.score(X_test, y_test)) #test Rsquared 0.3798403097116271

y_pred = reg.predict(X_test)
mean_squared_error(y_test, y_pred) #test MSE 1235.1067855657857
y_pred = reg.predict(X_train)
mean_squared_error(y_train, y_pred) #training MSE 1706.2682688744092


#7.
#Ridge
ridge = Ridge(normalize = True)
alpha_param = (10**np.linspace(start=-2, stop=2, num=100))

def vector_values(grid_search, trials):
    mean_vec = np.zeros(trials)
    std_vec = np.zeros(trials)
    i = 0
    final = grid_search.cv_results_
    
    for mean_score, std_score in zip(final["mean_test_score"], final["std_test_score"]):
        mean_vec[i] = -mean_score
        std_vec[i] = std_score
        i = i+1

    return mean_vec, std_vec

param_grid = [{'alpha': alpha_param }]
grid_search_ridge = GridSearchCV(ridge, param_grid, cv = 10, scoring = 'neg_mean_squared_error')
grid_search_ridge.fit(X_train, y_train)

mean_vec, std_vec = vector_values(grid_search_ridge, 100)

plt.figure(figsize=(12,10))
plt.title('Ridge Regression', fontsize= 20)
plt.plot(np.log(alpha_param), mean_vec)
plt.errorbar(np.log(alpha_param), mean_vec, yerr = std_vec)
plt.ylabel("MSE", fontsize= 20)
plt.xlabel("log(Alpha)", fontsize= 20)
plt.show()

# Find the optimal MSE score
print(min(mean_vec)) #1929.5610821469459

# Optimal alpha
ridgealpha = alpha_param[np.where(mean_vec == min(mean_vec))][0] #0.21544346900318845
ridgealpha

ridge2 = linear_model.Ridge(alpha=ridgealpha, normalize=True)
ridge2.fit(X_train, y_train) 

#Lasso
lasso = Lasso(normalize = True)

grid_search_lasso = GridSearchCV(lasso, param_grid, cv = 10, scoring = 'neg_mean_squared_error')
grid_search_lasso.fit(X_train, y_train)

mean_vec, std_vec = vector_values(grid_search_lasso, 100)

plt.figure(figsize=(12,10))
plt.title('Lasso Regression', fontsize= 20)
plt.plot(np.log(alpha_param), mean_vec)
plt.errorbar(np.log(alpha_param), mean_vec, yerr = std_vec)
plt.ylabel("MSE", fontsize= 20)
plt.xlabel("log(Alpha)", fontsize= 20)
plt.show()


# Find the optimal MSE score
print(min(mean_vec)) #1961.2445474737956

# Optimal alpha
lassoalpha = alpha_param[np.where(mean_vec == min(mean_vec))][0] #0.01
lassoalpha
lasso2 = linear_model.Lasso(alpha=lassoalpha, normalize=True) 

#8.
#Ridge
ridge2 = linear_model.Ridge(alpha=ridgealpha, normalize=True)
ridge2.fit(X_train, y_train) 
print(ridge2.score(X_train, y_train)) #training Rsquared 0.39178400924305734
print(ridge2.score(X_test, y_test)) #test Rsquared 0.3840209888232874
y_pred2 = ridge2.predict(X_test)
mean_squared_error(y_test, y_pred2) #test MSE 1226.780566980563
y_pred2 = ridge2.predict(X_train)
mean_squared_error(y_train, y_pred2) #training MSE 1767.5031598013927


#Lasso
lasso2 = linear_model.Lasso(alpha=lassoalpha, normalize=True) 
lasso2.fit(X_train, y_train)
print(lasso2.score(X_train, y_train)) #training Rsquared 0.39503455799219
print(lasso2.score(X_test, y_test)) #test Rsquared 0.3946107517390012
y_pred2 = lasso2.predict(X_test)
mean_squared_error(y_test, y_pred2) #test MSE  1205.6900507158748
y_pred2 = lasso2.predict(X_train)
mean_squared_error(y_train, y_pred2) #training MSE 1758.0569182153563



