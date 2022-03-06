import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import LinearAxis, Range1d
from bokeh.palettes import Spectral
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from statsmodels.tsa.ar_model import AutoReg

### Getting nuclear reactor location table with beautiful soup
### ref: https://towardsdatascience.com/scraping-table-data-from-websites-using-a-single-line-in-python-ba898d54e2bc
url = r'https://en.wikipedia.org/wiki/List_of_nuclear_power_stations'

def get_table(url):
    # webscrape table
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    data = []
    table = soup.find('table', {'class':'sortable wikitable'})
    table_header = table.find_all('th')
    header = [th.text.strip() for th in table_header]
    table_body = table.find('tbody')
    dic = dict(list(enumerate(header)))
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append([col.replace(u'\ufeff', '') for col in cols])
    
    # convert to df and 
    df = pd.DataFrame.from_records(data)
    df = df.rename(columns = dic)
    df = df.rename(columns={'Power station':"power plant",
                            '# units[note 1]':'unit',
                            'Net capacity[note 2](MWe)':'net capa',
                            'Country':'country',
                            'Location':'location'})
    which_country = ['United States']
    df = df[df.country.isin(which_country)]
    df[['geo','geo1','geo2']] = df.location.str.split(' / ', expand=True)
    df[['latitude','longitude']] = df.geo1.str.split(' ', expand=True)
    df = df.drop(['Refs','geo','geo1','geo2','location'], axis=1)
    df['latitude'] = df['latitude'].str[:-2].astype(float)
    df['longitude'] = df['longitude'].str[:-2].astype(float)*-1
    df['net capa'] = np.where(df['net capa'].str.endswith(']'), 
                          df['net capa'].str[:-9].str.replace(',',''), 
                          df['net capa'].str.replace(',',''))
    df['net capa'] = df['net capa'].astype(float)
    
    return df

df = get_table(url)


### Map locations of nuclear power plants
### ref: https://geopandas.org/mapping.html
### ref: https://stackoverflow.com/questions/43812911/adding-second-legend-to-scatter-plot
path = os.path.join(os.getcwd())

def get_us_map(path):
    census = gpd.read_file(os.path.join(path, 'cb_2018_us_state_500k.shp'))
    not_mainland = ['AK', 'HI', 'AS', 'GU', 'MP', 'PR', 'VI']
    us = census[~census.STUSPS.isin(not_mainland)]
    return us

us = get_us_map(path)


png_path = os.path.join(path, 'Nuclear Power Plants in the US.png')

def plot_reactors(us, df):
    crs = {'init': 'epsg:4326'}
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, crs = crs, geometry = geometry)
    fig, ax = plt.subplots(figsize=(10,10))
    us.plot(ax=ax, color='gray', edgecolor='white')

    h = [plt.plot([],[], color="gray", marker="o", 
                  markersize=i, ls="")[0] for i in (5,10,15)]
    leg= plt.legend(handles=h, labels=(1000,2000,3000),
                    loc=(0.01,0.01), title="Net Capacity (MW)",
                    fontsize = 10, title_fontsize = 10)
    ax.add_artist(leg)
    
    gdf.plot(ax=ax, markersize=df['net capa']/10,
                legend=True,
                legend_kwds={#'loc':'lower right',
                             'loc': (0.91, 0.01),
                             'title': "Units #", 
                             'fontsize': 10, 'title_fontsize': 10}, 
                cmap =   'OrRd',
                column='unit')
    ax.axis('off')
    ax.set(title='Nuclear Power Plants in the US')
   
    plt.savefig(png_path)
    print('Image saved: ', png_path)
    plt.show()
    
plot_reactors(us, df)


### Load and merge df for plot
def load_elec_data(path):
    df = pd.read_csv(os.path.join(path, 'Net electricity generation.csv'))
    df = df.drop([0,1,2,3,4,5])
    df = df.drop(columns=['Series Key.1', 'Series Key.2',
                          'Series Key.3','Series Key.4'])
    df = df.rename(columns={'Series Key':'Year',
                            'ELEC.GEN.COW-US-99.M':'Coal',
                            'ELEC.GEN.NG-US-99.M':'Natural Gas',
                            'ELEC.GEN.NUC-US-99.M':'Nuclear',
                            'ELEC.GEN.HYC-US-99.M':'Conventional Hydroelectric',
                            'ELEC.GEN.WND-US-99.M':'Wind'})
    return df

df_elec = load_elec_data(path)

def load_climate_data(path):
    df = pd.read_csv(os.path.join(path, 'Climate.csv'), skiprows=4)
    df.columns = ['Year', 'Temperature', 'Departure from Mean']
    df['Year'] = df['Year'].astype(str)
    return df

df_clim = load_climate_data(path)


def merge_df(df1, df2):
    df = pd.merge(df1, df2, on='Year')
    df["year"] = df["Year"].str.slice(0,4)
    df["month"] = df["Year"].str.slice(4,6)
    df['Date']= pd.to_datetime(['{}-{}-01'.format(y, m) 
                               for y, m in zip(df.year, df.month)])
    df = df.drop(['Year','year','month'], axis=1)
    df = df.sort_values(by='Date',ascending=True)

    return df

df_merged = merge_df(df_elec, df_clim)
#df_merged['Date'] = df_merged['Date'].dt.date

csv_path = os.path.join(path, 'df_merged.csv')
df_merged.to_csv(csv_path)


### Filtered df for an interactive plot
### ref: https://stackoverflow.com/questions/25199665/one-chart-with-two-different-y-axis-ranges-in-bokeh
### ref: https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html#stacked
### ref: https://stackoverflow.com/questions/55214348/include-bokeh-tooltips-in-stacked-bar-chart


df_merged_2 = df_merged.copy()
df_merged_2['Date'] = df_merged_2['Date'].dt.date
csv_path = os.path.join(path, 'df_merged_filtered.csv')
df_merged_2.to_csv(csv_path)

def interact_plot(df):
    
    output_file('stacked.html')
    months_x = list(df['Date'])
    months_x = list(map(str, months_x)) 
    resources_legend = list(df.columns[0:-3])
    num_colors= len(resources_legend)
    colors = Spectral[num_colors]

    data = {'months' : months_x}
    for i in range(num_colors):
        if ' ' in resources_legend[i]:
            origin_col = resources_legend[i]
            resources_legend[i] = origin_col.replace(' ', '_')
            data[resources_legend[i]] = list(map(float,df[origin_col])) 
        else:
            data[resources_legend[i]] = list(map(float,df[resources_legend[i]])) 


    tooltips = [
    (x,  "@" + x) for x in data.keys()]
 
    p = figure(x_range=months_x, plot_width = 10000,plot_height=500, 
               title="Monthly Net Electricity Generation by Energy Source with National Average Temperature", 
               tooltips = tooltips, toolbar_location="right", tools=["hover"])
    
    
    p.vbar_stack(resources_legend, x='months', width=0.5, color=colors, 
                 source=data,legend_label=resources_legend)
    
    
    min_temp = min(list(df['Temperature']))
    max_temp = max(list(df['Temperature']))
    range_adjust = 20
    p.extra_y_ranges = {"Temperature": Range1d(start=min_temp- range_adjust, 
                                               end=max_temp+ range_adjust)}
    
    p.line(x=months_x, y=list(df['Temperature']),y_range_name = 'Temperature', 
           color=colors[-1], line_width=2, legend='Temperature')
    
    p.title.text_font_size = '20pt'
    p.xaxis.axis_label = 'Date'
    p.xaxis.major_label_orientation = "vertical"
    p.yaxis.axis_label = 'Electricity Generation in thousand Megawatthours'
    p.add_layout(LinearAxis(y_range_name="Temperature", 
                            axis_label='Temperature'), 'right')
    
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.legend.click_policy="hide"

    
    show(p)
    
    
interact_plot(df_merged_2)


### Create train test data
def train_test(df):
    df = df.set_index(['Date'])
    X = df.drop(['Nuclear'], axis=1)
    Y = df['Nuclear'].astype(float)
    X_train = X.loc["2001-1-1":"2015-12-1"]
    Y_train = Y.loc["2001-1-1":"2015-12-1"]
    X_test = X.loc["2016-1-1":"2020-9-1"]
    Y_test = Y.loc["2016-1-1":"2020-9-1"]
    return X, Y, X_train, X_test, Y_train, Y_test

X, Y, X_train, X_test, Y_train, Y_test = train_test(df_merged)


### Run linear regression
def run_lin_reg(X_train, X_test, Y_train, Y_test):
    model = LinearRegression(fit_intercept=False)  
    results = model.fit(X_train, Y_train)
    print(results.coef_)
    predict = model.fit(X_train, Y_train).predict(X_test)
    print(r2_score(Y_test, predict))

run_lin_reg(X_train, X_test, Y_train, Y_test)


### Run autocorrelation regression
### ref: https://machinelearningmastery.com/gentle-introduction-autocorrelation-partial-autocorrelation/
### ref: https://pythondata.com/forecasting-time-series-autoregression/
def run_ac_reg(train, test):
    ar_train = train.reset_index().drop('Date', axis=1)
    ar_test = test.reset_index().drop('Date', axis=1)
    
    model = AutoReg(ar_train, lags=12, old_names=False)
    model_fitted = model.fit()
    predict_ar = model_fitted.predict(start=len(ar_train), 
                                      end=len(ar_train) + len(ar_test)-1, 
                                      dynamic=False)
    print(r2_score(ar_test, predict_ar))
    
    results = pd.concat([Y_test.reset_index(), 
                         predict_ar.reset_index().drop('index', axis=1)], 
                        axis=1)
    results = results.set_index(['Date'])
    results = results.rename(columns={0:'Prediction','Nuclear': 'Actual'})
    return results
    
results = run_ac_reg(Y_train, Y_test)

png_path2 = os.path.join(path, 'Predicted vs. Actual Results.png')


### Plot predicted outcome with actual outcome from test data for comparison
def plot_results(results):
    fig, ax = plt.subplots(figsize=(12,5))
    results.plot(ax = ax);
    ax.set_title('Predicted vs. Actual Nuclear Power Generation', 
                 fontsize='17')
    ax.set_ylabel('Nuclear Power Generation (thousand megawatthours)')
    ax.legend(bbox_to_anchor=(1.02, 1))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(png_path2)
    print('Image saved: ', png_path2)
    plt.show()

plot_results(results)

