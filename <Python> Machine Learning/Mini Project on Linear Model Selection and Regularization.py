import os
os.environ['R_HOME'] = "/Library/Frameworks/R.framework/Resources"

from r_wrapper import diftrans
from r_wrapper import base
from r_wrapper import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# [3.2] Understand the Data
Beijing_sample = base.get("Beijing_sample")
Tianjin_sample = base.get("Tianjin_sample")

# [3.3] Clean Data of Beijing and Tianjin Car Sales
# keep 2010 and 2011 data only
Beijing = Beijing_sample[(Beijing_sample['year']>= 2010) & (Beijing_sample['year'] < 2012)]

# collect unique MSRP values
uniqueMSRP = pd.DataFrame(Beijing.MSRP.unique()).rename(columns={0:'MSRP'})

# aggregate sales at each price for 2010 (pre-lottery)
Beijing10_sales = Beijing[(Beijing['year'] == 2010)].groupby('MSRP').aggregate({'sales':[sum]})
Beijing10_sales = Beijing10_sales.unstack().reset_index().rename_axis(None, axis=1)
Beijing10_sales = Beijing10_sales.drop(columns=['level_0', 'level_1']).rename(columns={0:'count'})

# merge the MSRP and sales
Beijing_pre = uniqueMSRP.merge(Beijing10_sales, how='left', on = "MSRP")
Beijing_pre[['count']] = Beijing_pre[['count']].fillna(value=0) 
Beijing_pre = Beijing_pre.sort_values('MSRP') 
Beijing_pre.head() # preview data

# Exercise 3.1 
# a) Clean data of Beijing car sales in 2011, and store the data frame in a variable called Beijing_post.
Beijing11_sales = Beijing[(Beijing['year'] == 2011)].groupby('MSRP').aggregate({'sales':[sum]})
Beijing11_sales = Beijing11_sales.unstack().reset_index().rename_axis(None, axis=1)
Beijing11_sales = Beijing11_sales.drop(columns=['level_0', 'level_1']).rename(columns={0:'count'})

Beijing_post = uniqueMSRP.merge(Beijing11_sales, how='left', on = "MSRP")
Beijing_post[['count']] = Beijing_post[['count']].fillna(value=0) 
Beijing_post = Beijing_post.sort_values('MSRP') 
Beijing_post.head() # preview data

# b) Clean data of Tianjin car sales in 2010 as a variable called Tianjin_pre.
Tianjin = Tianjin_sample[(Tianjin_sample['year']>= 2010) & (Tianjin_sample['year'] < 2012)]
uniqueMSRP1 = pd.DataFrame(Tianjin.MSRP.unique()).rename(columns={0:'MSRP'})

Tianjin10_sales = Tianjin[(Tianjin['year'] == 2010)].groupby('MSRP').aggregate({'sales':[sum]})
Tianjin10_sales = Tianjin10_sales.unstack().reset_index().rename_axis(None, axis=1)
Tianjin10_sales = Tianjin10_sales.drop(columns=['level_0', 'level_1']).rename(columns={0:'count'})

Tianjin_pre = uniqueMSRP1.merge(Tianjin10_sales, how='left', on = "MSRP")
Tianjin_pre[['count']] = Tianjin_pre[['count']].fillna(value=0) 
Tianjin_pre = Tianjin_pre.sort_values('MSRP') 
Tianjin_pre.head() # preview data

# c) Clean data of Tianjin car sales in 2011 as a variable called Tianjin_post.
Tianjin11_sales = Tianjin[(Tianjin['year'] == 2011)].groupby('MSRP').aggregate({'sales':[sum]})
Tianjin11_sales = Tianjin11_sales.unstack().reset_index().rename_axis(None, axis=1)
Tianjin11_sales = Tianjin11_sales.drop(columns=['level_0', 'level_1']).rename(columns={0:'count'})

Tianjin_post = uniqueMSRP1.merge(Tianjin11_sales, how='left', on = "MSRP")
Tianjin_post[['count']] = Tianjin_post[['count']].fillna(value=0) 
Tianjin_post = Tianjin_post.sort_values('MSRP') 
Tianjin_post.head() # preview data

# [3.4] Visualize Beijing Car Sales
df2 = Beijing_pre.pop('count')
Beijing_distribution_pre = pd.DataFrame(Beijing_pre.values.repeat(df2, axis=0), columns=Beijing_pre.columns)

df3 = Beijing_post.pop('count')
Beijing_distribution_post = pd.DataFrame(Beijing_post.values.repeat(df3, axis=0), columns=Beijing_post.columns)

fig, ax = plt.subplots()
for a in [Beijing_distribution_pre, Beijing_distribution_post]:
    sns.distplot(a/1000, ax=ax, kde=False, norm_hist=True)
plt.xlabel("MSRP(1000RMB)", size=14)
plt.ylabel("Density", size=14)
plt.title("Pre-lottery (blue) vs. Post-lottery (brown)\n Sales Distributions of Beijing Cars", size=18)
plt.legend(loc='upper right')

# Excercise 3.2
# a) Overlay the histograms that describe the 2010 and 2011 distribution of Tianjin car sales. Be sure to normalize the histograms so the area of the bars in each histogram sum to 1.
df4 = Tianjin_pre.pop('count')
Tianjin_distribution_pre = pd.DataFrame(Tianjin_pre.values.repeat(df4, axis=0), columns=Tianjin_pre.columns)

df5 = Tianjin_post.pop('count')
Tianjin_distribution_post = pd.DataFrame(Tianjin_post.values.repeat(df5, axis=0), columns=Tianjin_post.columns)

fig, ax = plt.subplots()
for a in [Tianjin_distribution_pre, Tianjin_distribution_post]:
    sns.distplot(a/1000, ax=ax, kde=False, norm_hist=True)
plt.xlabel("MSRP(1000RMB)", size=14)
plt.ylabel("Density", size=14)
plt.title("Pre-lottery (blue) vs. Post-lottery (brown)\n Sales Distributions of Tianjin Cars", size=18)
plt.legend(loc='upper right')

# [3.5] Compute Before-and-After Estimator
base.set_seed(1) # for reproducibility
n_observations = 100000
placebo_demonstration = pd.DataFrame({'sample1': np.random.normal(0, 1, n_observations), 'sample2': np.random.normal(0, 1, n_observations)})
placebo_demonstration.head()

fig, ax = plt.subplots()
ax = sns.distplot(placebo_demonstration['sample1'], ax=ax, kde=False, norm_hist=True)
ax = sns.distplot(placebo_demonstration['sample2'], ax=ax, kde=False, norm_hist=True)
plt.xlabel("Support", size=12)
plt.ylabel("Density", size=14)
plt.title("Two Samples from Standard Normal Distribution", size=18)

# set the seed for reproducibility set.seed(1)
# We will use the `rmultinom` function to construct our placebo.
# Imagine the same number of cars as in 2010. (see `size` argument)
# For each MSRP value, we will decide how many of these imaginary cars will
# be sold at this price. The number of of these imaginary cars to be sold at
# the particular MSRP value will be proportional to the actual number of cars
# sold in the pre-lottery distribution. (see `prob` argument) # We only want one placebo distribution. (see `n` argument) placebo_1 <- data.frame(MSRP = Beijing_pre[‘MSRP’],
base.set_seed(1)
Beijing_pre = uniqueMSRP.merge(Beijing10_sales, how='left', on = "MSRP")
Beijing_pre[['count']] = Beijing_pre[['count']].fillna(value=0)
Beijing_pre = Beijing_pre.sort_values('MSRP')
count =  stats.rmultinom(n = 1, size = sum(Beijing_pre['count']), prob = Beijing_pre['count'])
count2 = count[:,0]
d = {'MSRP': Beijing_pre['MSRP'], 'count' : count2}
placebo_1 = pd.DataFrame(data=d)
print(placebo_1)
print(placebo_1.dtypes)


# Exercise 3.3
# b) Use rmultinom to sample observations from Beijing_pre. Store the resulting data frame in placebo_2. Be careful to draw the correct number of observations.
base.set_seed(1)
Beijing_post = uniqueMSRP.merge(Beijing11_sales, how='left', on = "MSRP")
Beijing_post[['count']] = Beijing_post[['count']].fillna(value=0)
Beijing_post = Beijing_post.sort_values('MSRP')
count3 =  stats.rmultinom(n = 1, size = sum(Beijing_post['count']), prob = Beijing_pre['count'])
count4 = count3[:,0]
d = {'MSRP': Beijing_pre['MSRP'], 'count' : count4}
placebo_2 = pd.DataFrame(data=d)
print(placebo_2)
print(placebo_2.dtypes)


#c) Compare placebo_1 and placebo_2. Do they appear to be drawn from the same distribution?
fig, ax = plt.subplots()
for a in [placebo_1, placebo_2]:
    sns.distplot(a/1000, ax=ax, kde=False, norm_hist=True)
plt.xlabel("MSRP(1000RMB)", size=14)
plt.ylabel("Density", size=14)
plt.title("Placebo_1 (blue) vs. Placebo_2 (brown) Distribution", size=18)
plt.legend(loc='upper right')

placebo_at_0 = diftrans.diftrans(pre_main = placebo_1, post_main = placebo_2, bandwidth_seq = 0)
placebo_at_0


# Exercise 3.4
# a) Compute the transport cost between the two placebo distributions for different values of 𝑑 from 0 to 100,000.
transcost_placebo = diftrans.diftrans(pre_main = placebo_1, post_main = placebo_2, bandwidth_seq = np.arange(0, 100000, step = 1000))
transcost_placebo

#b) For the same values of 𝑑, compute the transport cost between the observed distributions for 2010 and 2011 Beijing car sales.
transcost = diftrans.diftrans(pre_main = Beijing_pre, post_main = Beijing_post, bandwidth_seq = np.arange(0, 100000, step = 1000))
transcost

#c) Plot the placebo costs and the empirical costs obtained in the previous two steps with the bandwidth as the x-axis
fig, ax = plt.subplots()
ax = plt.plot('bandwidth', 'main', data=transcost_placebo, label='Placebo')
ax = plt.plot('bandwidth', 'main', data=transcost, label='Empirical')
plt.legend()
plt.xlabel("Bandwidth", size=12)
plt.ylabel("Trasnport Cost", size=14)
plt.title("Placebo and Empricial Transport Cost", size=18)

#d) For which values of 𝑑 is the placebo cost less than 0.05%?
transcost_placebo.loc[transcost_placebo['main'] <= 0.0005]
#25000

#e) For the smallest value of 𝑑 found in the previous step, what is the empirical transport cost?
transcost.loc[transcost['bandwidth'] == 25000]
#0.100769


# [3.6] Compute Differences-in-Transports Estimator
Tianjin_pre = uniqueMSRP1.merge(Tianjin10_sales, how='left', on = "MSRP")
Tianjin_pre[['count']] = Tianjin_pre[['count']].fillna(value=0)
Tianjin_pre = Tianjin_pre.sort_values('MSRP')

Tianjin_post = uniqueMSRP1.merge(Tianjin11_sales, how='left', on = "MSRP")
Tianjin_post[['count']] = Tianjin_post[['count']].fillna(value=0)
Tianjin_post = Tianjin_post.sort_values('MSRP')

dit_at_0 = diftrans.diftrans(pre_main = Beijing_pre, post_main = Beijing_post, pre_control = Tianjin_pre, post_control = Tianjin_post, bandwidth_seq = 0, conservative = True)
dit_at_0

# Exercise 3.5
#a) Compute the (3) for different values of 𝑑 from 0 to 50,000. Unlike before, we go up to 50,000 because we are using the conservative bandwidth of 2𝑑 for the Beijing transport cost.
dit = diftrans.diftrans(pre_main = Beijing_pre, post_main = Beijing_post, pre_control = Tianjin_pre, post_control = Tianjin_post, bandwidth_seq = np.arange(0, 50000, step = 1000), conservative = True)
dit 

#b) Using what you learned from Exercise 3.3, construct a placebo distribution that is sampled from Beijing_pre whose size is the number of Beijing cars in 2010. Call this distribution placebo_Beijing_1.
base.set_seed(1)
count =  stats.rmultinom(n = 1, size = sum(Beijing_pre['count']), prob = Beijing_pre['count'])
count2 = count[:,0]
d = {'MSRP': Beijing_pre['MSRP'], 'count' : count2}
placebo_Beijing_1 = pd.DataFrame(data=d)
print(placebo_Beijing_1)
print(placebo_Beijing_1.dtypes)

#c) Construct another placebo distribution called placebo_Beijing_2 that is also sampled from Beijing_pre but is of size is the number of Beijing cars in 2011.
base.set_seed(1)
count3 =  stats.rmultinom(n = 1, size = sum(Beijing_post['count']), prob = Beijing_pre['count'])
count4 = count3[:,0]
d = {'MSRP': Beijing_pre['MSRP'], 'count' : count4}
placebo_Beijing_2 = pd.DataFrame(data=d)
print(placebo_Beijing_2)
print(placebo_Beijing_2.dtypes)

#d) Construct a placebo distribution called placebo_Tianjin_1 that is sampled from Tianjin_pre and whose size is the number of Tianjin cars in 2010.
base.set_seed(1)
count =  stats.rmultinom(n = 1, size = sum(Tianjin_pre['count']), prob = Tianjin_pre['count'])
count2 = count[:,0]
d = {'MSRP': Tianjin_pre['MSRP'], 'count' : count2}
placebo_Tianjin_1 = pd.DataFrame(data=d)
print(placebo_Tianjin_1)
print(placebo_Tianjin_1.dtypes)

#e) Construct a placebo distribution called placebo_Tianjin_2 that is sampled from Tianjin_pre and whose size is the number of Tianjin cars in 2011.
base.set_seed(1)
count3 =  stats.rmultinom(n = 1, size = sum(Tianjin_post['count']), prob = Tianjin_pre['count'])
count4 = count3[:,0]
d = {'MSRP': Tianjin_pre['MSRP'], 'count' : count4}
placebo_Tianjin_2 = pd.DataFrame(data=d)
print(placebo_Tianjin_2)
print(placebo_Tianjin_2.dtypes)

#f) Using the four placebo distributions, compute the placebo counterpart of (3) for the same values of 𝑑 that you used in part a
dit1 = diftrans.diftrans(pre_main = placebo_Beijing_1, post_main = placebo_Beijing_2, pre_control = placebo_Tianjin_1, post_control = placebo_Tianjin_2, bandwidth_seq = np.arange(0, 50000, step = 1000), conservative = True)
dit1

#g) Create a plot of the absolute value of the placebo differences-in-transports estimator on the y-axis and the bandwidth on the x-axis.
dit1['Absolute diff2d'] = np.absolute(dit1['diff2d'])

fig, ax = plt.subplots()
ax = plt.plot('bandwidth', 'Absolute diff2d', data=dit1, label='Difference 2d in the Beijing and Tianjin')
plt.legend()
plt.xlabel("Bandwidth", size=12)
plt.ylabel("Trasnport Cost", size=14)
plt.title("Absolute Value of the Placebo differences-in-transports", size=18)

#h) For which values of 𝑑 does the absolute value of the placebo differences-in-transports estimator stay below 0.05%?
d2 = dit1.loc[dit1['Absolute diff2d'] <= 0.0005] #7000
d2

#i) Among all the values of 𝑑 that you found in the previous step, which one yielded the largest value of (3) from part a?
dit.loc[dit['diff2d'].idxmax()] #7000
