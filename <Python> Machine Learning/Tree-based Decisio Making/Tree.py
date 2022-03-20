import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import seaborn as sns




#Chapter 6 Question 9
college = pd.read_csv('./Data-College.csv', index_col = 0)
college.shape
college.columns

college = pd.get_dummies(college, columns=['Private'])

#a) Split the data set into a training set and a test set.
X = college.copy()
y = X.pop('Apps')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42)


#b) Fit a linear model using least squares on the training set, and report the test error obtained.
reg = LinearRegression().fit(X_train, y_train)
y_pred = reg.predict(X_test)
mean_squared_error(y_test, y_pred) #test MSE


#e) Fit a PCR model on the training set, with M chosen by cross-validation. 
#Report the test error obtained, along with the value of M selected by cross-validation.
#source: https://www.statology.org/principal-components-regression-in-python/
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale 
from sklearn.model_selection import RepeatedKFold
from sklearn import model_selection

#scale predictor variables
pca = PCA()
X_reduced = pca.fit_transform(scale(X))

#define cross validation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

regr = LinearRegression()
mse = []

# Calculate MSE with only the intercept
score = -1*model_selection.cross_val_score(regr,
           np.ones((len(X_reduced),1)), y, cv=cv,
           scoring='neg_mean_squared_error').mean()    
mse.append(score)

# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 6):
    score = -1*model_selection.cross_val_score(regr,
               X_reduced[:,:i], y, cv=cv, scoring='neg_mean_squared_error').mean()
    mse.append(score)


#split the dataset into training (70%) and testing (30%) sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0) 

#scale the training and testing data
X_reduced_train = pca.fit_transform(scale(X_train))
X_reduced_test = pca.transform(scale(X_test))[:,:1]

#train PCR model on training data 
regr = LinearRegression()
regr.fit(X_reduced_train[:,:1], y_train)

#calculate RMSE
pred = regr.predict(X_reduced_test)
np.sqrt(mean_squared_error(y_test, pred))

# Plot cross-validation results    
plt.plot(mse)
plt.xlabel('Number of Principal Components')
plt.ylabel('MSE')
plt.title('hp')



#f) Fit a PLS model on the training set, with M chosen by cross- validation. 
#Report the test error obtained, along with the value of M selected by cross-validation.
#source: https://www.statology.org/partial-least-squares-in-python/
#define cross-validation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

mse = []
n = len(X)

# Calculate MSE with only the intercept
score = -1*model_selection.cross_val_score(PLSRegression(n_components=1),
           np.ones((n,1)), y, cv=cv, scoring='neg_mean_squared_error').mean()    
mse.append(score)

# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 6):
    pls = PLSRegression(n_components=i)
    score = -1*model_selection.cross_val_score(pls, scale(X), y, cv=cv,
               scoring='neg_mean_squared_error').mean()
    mse.append(score)

#split the dataset into training (70%) and testing (30%) sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0) 

#calculate RMSE
pls = PLSRegression(n_components=2)
pls.fit(scale(X_train), y_train)

np.sqrt(mean_squared_error(y_test, pls.predict(scale(X_test))))

#plot test MSE vs. number of components
plt.plot(mse)
plt.xlabel('Number of PLS Components')
plt.ylabel('MSE')
plt.title('hp')






#Chapter 8 Question 9
oj = pd.read_csv('./oj.csv', index_col = 0)
oj.shape
oj.columns
oj.head

oj = pd.get_dummies(oj, columns=['Store7'])


# i) Create a training set containing a random sample of 800 observations, 
#    and a test set containing the remaining observations.
X = oj.copy()
y = X.pop('Purchase')

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 800, random_state = 1)

# ii) Fit a tree to the training data, with Purchase as the response and the other variables as predictors. 
#What is the training error rate? (Set the max_depth parameter to 3 in order to get an interpretable plot)
model_ii = DecisionTreeClassifier(max_depth =3, random_state=1) 
model_ii.fit(X_train, y_train)

y_pred_tree3 = model_ii.predict(X_test)

1 - accuracy_score(y_train, y_pred_tree3)

# iii) Create a plot of the tree. How many terminal nodes does the tree have? 
# Pick one of the terminal nodes, and interpret the information displayed.
plt.figure(figsize=(12,12))
tree.plot_tree(model_ii, fontsize=10)

# tree.plot_tree(model)
plt.show()

# iv) Predict the response on the test data, and produce a confusion matrix comparing 
# the test labels to the predicted test labels. What is the test error rate?
cm = confusion_matrix(y_test, y_pred_tree3)
print(cm)

#confusion matrix
print('\nTrue Negatives: ', cm[0][0])
print('False Negatives: ', cm[1][0])
print('True Positives: ', cm[1][1])
print('False Positives: ', cm[0][1])

#test error rate
print('\nTest error rate: ', 1 - accuracy_score(y_test, y_pred_tree3)) 

# v) Determine the optimal tree size by tuning the ccp_alpha argument in scikit-learn’s 
# DecisionTreeClassifier. You can use GridSearchCV for this purpose.
tree_size = np.arange(2,20)
print(tree_size)
parameters = {'max_depth': tree_size}
cv_tree = GridSearchCV(model_ii, parameters)
cv_tree.fit(X_train, y_train)

cv_scores = []
for mean_score in zip(cv_tree.cv_results_["mean_test_score"]):
    cv_scores.append(mean_score[0])
    
tree_size[cv_scores.index(max(cv_scores))] #3


#vi)Produce a plot with tree size on the x-axis and cross-validated classification error 
# rate on the y-axis calculated using the method in the previous question. 
# Which tree size corresponds to the lowest cross-validated classification error rate?
plt.figure(figsize=(10,8))
sns.lineplot(x=tree_size, y=cv_scores)
plt.xlabel("Tree size", fontsize= 16)
plt.ylabel("CV classification error rate")
plt.title('Tree')

tree_size[cv_scores.index(min(cv_scores))]

#vii)Produce a pruned tree corresponding to the optimal tree size obtained using cross-validation. 
#If cross-validation does not lead to selection of a pruned tree, then create a pruned tree with five terminal nodes.
model_full = DecisionTreeClassifier(random_state=1) 






