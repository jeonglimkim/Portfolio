# Nuclear Power Generation in the U.S.

#### Jeong Lim Kim and Jayoung Kang \| PPHA 30536: Data and Programming for Public Policy II

## ***Project Overview***

This project is aimed at understanding the current status and trend of nuclear share of electricity net generation in the United States. Electricity generation by nuclear power plant is a contested topic around the globe. Growing concerns on air pollution and nuclear safety have led policy makers to implement a nuclear power phase-out. Thus, in order to predict the future trend of nuclear generation in the U.S., we have examined the historical trend and current status of nuclear generation. We have employed the following approaches in programming our final project:

*a. Understanding current status of nuclearpower plants*

We first mapped the location of the current operating nuclear power plants through web-scraping the table that contains the location of operating nuclear power plants in the United States byusing **BeautifulSoup** and plotting it onto the U.S. map through **geopandas**.

*b. Understanding the historical trend of electricity power generation in the U.S.*

In order to understand the historical trend of electricity power generation in the U.S., we have developed a stacked bar graph that displays monthly net electricity generation from five energy sources -- coal, natural gas, nuclear, conventional hydroelectric, and wind. To analyze if climate change has any correlation with net electricity generation, we merged the data on national average temperature from year 2001 to 2020 with the net electricity generation data and visually display the relationship between two elements. Through **bokeh**, we have provided a hover tool to inspect the data. The legends are also interactive, allowing the audience to click on specific data he wishes to focus on visually.

*c. Predicting future nuclear power generation*

In order to fit a model to predict nuclear power generation, we conducted two types of regression. The first regression was a linear regression, using the monthly energy generated from other sources (coal, natural gas, hydroelectricity, wind) as well as the monthly average climate in the U.S. as the x-variables. We used the climate data because we hypothesized that energy production in general would be linked to climate levels. However, since our data was a time-series data, we also ran an autocorrelation with twelve lags in order to account seasonality. In order to run the autocorrelation, we utilized the **statsmodels** package. For both models, we split the data in the training and testing data by the date, so that data from 2001 to 2015 were used as training data and data from 2016 to 2020 was used as testing data.

## ***Data Usage*** 

In order to conduct the final project, the data we utilized consist of the following:

a)  Wikipedia page with location data of operating nuclear power plants in the U.S.

    <https://en.wikipedia.org/wiki/List_of_nuclear_power_stations>

b)  Cartographic boundary files from the U.S. Census Bureau

    <https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html>

c)  U.S. Energy Information Administration

    <https://www.eia.gov/beta/states/data/dashboard/electricity>

d)  National Climatic Data Center

    <https://www.ncdc.noaa.gov/cag/national/time-series>
