import pandas as pd

# # For making dictionary to make it simple

def make_filtered_data(path, istrain=True):
#     path = "./GDP.csv"
    state_desc_dict = {}
    
    data = pd.read_csv(path,skiprows= 4)
    data= data.drop(['GeoFips','LineCode'], axis = 1)
    data = data.rename(columns = {"GeoName":"State"})
    not_state_list = ['New England', 'Mideast', 'Great Lakes', 'Plains', 'Southeast', 'Southwest', 'Rocky Mountain', 'Far West']
    data_filtered = data[data.State != 'United States *']
    for not_state in not_state_list:
        data_filtered = data_filtered[data_filtered.State != not_state]
    data_filtered = data_filtered[:-7]
    
    for state in (sorted(set(data_filtered.State))):
        data_state = data_filtered[data_filtered.State == state]
    
        desc_dict = {}
        for desc in (sorted(set(data_state.Description))):
            if not 'Addenda' in desc:
                data_desc = data_state[data_state.Description == desc]
                try: 
                    desc_dict[desc] = float(data_desc['2008'].item()) if istrain else float(data_desc['2012'].item())
                except:
                    desc_dict[desc] = 0.0 # 0 if ('L'), ('D')

        state_desc_dict[state] = desc_dict
    
    return state_desc_dict

gdppath = "./GDP.csv"
wagepath = "./Wages and Salaries.csv"

gdp_filtered = make_filtered_data(gdppath)
wage_filtered = make_filtered_data(wagepath) # 2008 for train

gdp_filtered_test = make_filtered_data(gdppath, False)
wage_filtered_test = make_filtered_data(wagepath, False) # 2012 for test


# For making label

electionpath = "./1976-2016-president.csv"
election = pd.read_csv(electionpath)
election = election.drop(['state_po', 'state_fips', 'state_cen', 'state_ic', 'office', 'writein', 'version', 'notes'], axis = 1)
election_filtered = election[election['year'].isin(['2008', '2012'])]

election_2008 = election_filtered[election_filtered.year == 2008]
election_2012 = election_filtered[election_filtered.year == 2012]

def make_label_for_state(election_year):
    state_candidate_dict = {}
    for state in (sorted(set(election_year.state))):
        election_state = election_year[election_year.state == state]
        state_candidate_dict[state] = election_state.candidate.iloc[0]

    candidate_idx_dict = {}
    for idx, candidate in enumerate(set(state_candidate_dict.values())):
        candidate_idx_dict[candidate] = idx
    
    for key in state_candidate_dict.keys(): # change the name of candidate to idx
        for can_key in candidate_idx_dict.keys():
            if state_candidate_dict[key] == can_key:
                state_candidate_dict[key] = candidate_idx_dict[can_key]
                
    return candidate_idx_dict, state_candidate_dict

idx_train, label_train = make_label_for_state(election_2008)
idx_test, label_test = make_label_for_state(election_2012)

print(idx_train)
print(label_train)

print(idx_test)
print(label_test)

# transfrom dict to feature by using correlation coefficient

import numpy as np
import math

label_list = []
for state in label_train.keys():
    label_list.append(label_train[state])
    
label_list_test = []
for state in label_test.keys():
    label_list_test.append(label_test[state])

    
def get_top_5_desc(data_filtered, istrain= True):
    correlation = []
    for desc in list(data_filtered.values())[0].keys():
        score_list_per_desc = []
        
        if istrain:
            for state in label_train.keys():
                score_list_per_desc.append(data_filtered[state][desc])
        else:
            for state in label_test.keys():
                score_list_per_desc.append(data_filtered[state][desc])
        
            
        r = np.corrcoef(score_list_per_desc, label_list)
        
        if math.isnan(r[0,1]):
            correlation.append(0)
        else:
            correlation.append(abs((r[0,1])))
        


    top_5_idx = np.argsort(correlation)[-5:]
    top_5_desc = [list(list(data_filtered.values())[0].keys())[idx] for idx in top_5_idx]
    top_5_values = [correlation[i] for i in top_5_idx]
    print(top_5_values)
    print(top_5_desc)
    
    feature = []
    for desc in top_5_desc:
        feature_per_desc = []
        if istrain:
            for state in label_train.keys():
                feature_per_desc.append(data_filtered[state][desc])
        else:
            for state in label_test.keys():
                feature_per_desc.append(data_filtered[state][desc])
            
        feature.append(np.array(feature_per_desc))
    feature = np.array(feature).T
    feature = (feature - np.amin(feature))/(np.amax(feature) - np.amin(feature)) # normalize data
    
    return feature # (51,5)

label_array = np.array(label_list)
gdp_desc=get_top_5_desc(gdp_filtered) #(51,5)
wage_desc=get_top_5_desc(wage_filtered) # 51,5
concated_feature = np.hstack((gdp_desc,wage_desc)) # (51,10)

label_array_test = np.array(label_list_test)
gdp_desc_test=get_top_5_desc(gdp_filtered_test, False)
wage_desc_test=get_top_5_desc(wage_filtered_test, False)
concated_feature_test = np.hstack((gdp_desc_test,wage_desc_test))

print(label_array.shape)
print(concated_feature.shape)

print(label_array_test.shape)
print(concated_feature_test.shape)


from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB



models = [('Dec Tree', DecisionTreeClassifier()), 
          ('Lin Disc', LinearDiscriminantAnalysis()), 
          ('SVC', SVC(gamma='auto'))]

results = []

# 5-fold cross-validation
for name, model in models:
    kf = StratifiedKFold(n_splits=5)
    res = cross_val_score(model, concated_feature, label_array, cv=kf, scoring='accuracy')
    res_mean = round(res.mean(), 4)
    res_std  = round(res.std(), 4)
    results.append((name, res_mean, res_std))

print(results)


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

np.random.seed(603)
model = DecisionTreeClassifier()
model.fit(concated_feature, label_array) # training
predict = model.predict(concated_feature_test) # inference
accuracy_score(label_array_test, predict)




