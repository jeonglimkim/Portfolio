import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import random



#Chatper 4 Question 11
auto_data = pd.read_csv('./Data-Auto.csv')

#a median
auto_data['mpg01'] = auto_data.mpg > auto_data.mpg.median()
auto_data['mpg01'] = np.where(auto_data['mpg01'] == False, 0,1 )


#b boxplot, scatterplot
for col in auto_data.iloc[:, 2:8].columns:
    sns.boxplot(auto_data['mpg01'], auto_data[col])
    plt.title(col)
    plt.xlabel(col)
    plt.ylabel('mpg01')
    plt.show()

for col in auto_data.iloc[:, 2:8].columns:
    sns.scatterplot(auto_data[col],auto_data['mpg01'])
    plt.title(col)
    plt.xlabel(col)
    plt.ylabel('mpg01')
    plt.show()
    
    
#c split data
X = auto_data[['horsepower', 'acceleration', 'weight']]
y = auto_data['mpg01']
y = auto_data['mpg01'].astype('category').cat.codes
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


#d lda 
lda_model = LinearDiscriminantAnalysis()
lda_result = lda_model.fit(X_train, y_train)
y_pred11d = lda_model.predict(X_test)
accuracy_score(y_test, y_pred11d)
1-accuracy_score(y_test, y_pred11d)

#e qda 
qda_model = QuadraticDiscriminantAnalysis()
qda_result = qda_model.fit(X_train, y_train)
y_pred11e = qda_model.predict(X_test)
accuracy_score(y_test, y_pred11e)
1-accuracy_score(y_test, y_pred11e)

#f logistic
logit_model = LogisticRegression()
logit_result = logit_model.fit(X_train, y_train)
y_pred11f = logit_model.predict(X_test)
accuracy_score(y_test, y_pred11f)
1-accuracy_score(y_test, y_pred11f)



#Chatper 5 Question 5
random.seed()
default_data = pd.read_csv('./Data-Default.csv')

#a logistic regression 
default_data['default01'] = np.where(default_data['default'] == "No", 0, 1)
logit_model = LogisticRegression()
X = default_data[['income', 'balance']]
Y = default_data['default01']
result = logit_model.fit(X, Y)
result.coef_

#b validation. test error
X = default_data[['income', 'balance']]
y = default_data['default01']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

logit_result = logit_model.fit(X_train, y_train)
y_pred5b = logit_model.predict(X_test)
accuracy_score(y_test, y_pred5b)
1-accuracy_score(y_test, y_pred5b)

#c
X = default_data[['income', 'balance']]
y = default_data['default01']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

logit_result = logit_model.fit(X_train, y_train)
y_pred5c1 = logit_model.predict(X_test)
1-accuracy_score(y_test, y_pred5c1)


X = default_data[['income', 'balance']]
y = default_data['default01']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

logit_result = logit_model.fit(X_train, y_train)
y_pred5c2 = logit_model.predict(X_test)
1-accuracy_score(y_test, y_pred5c2)


X = default_data[['income', 'balance']]
y = default_data['default01']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.75, random_state=42)

logit_result = logit_model.fit(X_train, y_train)
y_pred5c3 = logit_model.predict(X_test)
1-accuracy_score(y_test, y_pred5c3)

#d student as dummy variable
default_data['student0'] = np.where(default_data['student'] == "No", 0, 1)
logit_model = LogisticRegression()
X = default_data[['income', 'balance', 'student0']]
Y = default_data['default01']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

logit_result = logit_model.fit(X_train, y_train)
y_pred5d = logit_model.predict(X_test)
1-accuracy_score(y_test, y_pred5d)













