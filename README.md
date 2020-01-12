# Austin Real Estate Analysis

Austin’s real estate market is undeniably on the rise.  The growing economy and been a highlight of the cities allure, along with being named the best place to live in the US on 3 consecutive years: 2017, 2018, and 2019 by U.S News & World Report.  My analysis dives into the current Austin real estate market, from a bedroom to bathroom ratio starting point.  Does the bed-to-bath ratio of homes have a statistical impact to the value of homes?   

## Table of Contents

* [General Information](#general-information)
    * [Data Gathering](#data-gathering)
    * [Data Information](#data-information)
    * [Hypothesis Testing](#hypothesis-testing)
* [Technologies](#technologies)
    * [Database](#database)
    * [Python](#python)
    * [Visualization](#visualization)
* [Future Improvements](#future-improvements)


## General Information
Investing in a home is a milestone many aim to achieve, whether viewed as just a starter home or potential AirBnB investment, it all begins with data.  This project began with just a simple believe to be tested: The ratio between bedrooms to bathrooms have an impact on home values. But it’s potential with further enrichment is quite limitless. 

![](images/distributions.png)

### Data Gathering:
<p align="center">
  <img src="images/realtylogos.png">
</p>

Data used for this analysis was gathered from Zillow, Realtor, and Realty Austin websites.  The data gathering techniques where separated into three phases, which are located under the ```src``` folder.  Two ```csv``` files, the results of the webscraping, are stored in the ```data``` directory.

1)   Scraping:  Three scrappers were used to gather current listing information from each site, code can be found under ```scrapper``` folder.  
2)  Transform:  It was transformed into a clean pandas dataframe through custom functions, located on the ```data_transformer``` folder.
3)  Cleansing:  Functions on the ```data_cleansing``` folder utilized the transform functions to clean the data and store clean data back to mongodb.   

### Data Information:
Data used in the study included square footage, number of beds, baths, and value for all single and multi-family homes, condo, and townhomes with active listings in the Austin housing market from December 2019 to January 2020, inside the city limits. This data was used to calculate averages and test for significance between equal ratio vs unequal ratio homes. All figures shown in the article represent the mean value for each data point unless otherwise specified. 

### Hypothesis Testing:

###### Step 1: Set up the hypothesis
The null hypothesis is that the ratio between bedrooms to bathrooms has no statistically significant difference to the mean value of homes.

Alternative hypothesis is that there is a significant difference to the mean value.

>**H0: μ = μ 0**

>**H1: μ ≠ μ 0**

###### Step 2: Select test statistic
To test this hypothesis the z-test was chosen.
The significance level was set at: 0.05

A z-test is a statistical test used to determine whether two population means are different when the variances are known and the sample size is large.

<p align="center">
  <img src="images/z-statistic.png">
</p>

###### Step 3: Set up decision rule
Reject the null hypothesis if test-statistic > 1.96 or if test-statistic < -1.96.
<p align="center" style="width:10%" >
  <img src="images/normdist.png">
</p>

###### Step 4: Compute the test statistic
This will be a two-tailed test

![](images/z-score.png)

###### Step 5: Conclusion
Given the results of our test we conclude that we must reject the null-hypothesis.  There is enough evidence to say that ratios between homes do have an effect on home values.
The z-score of 3.386 > 1.96 with a p-value of 0.001 well below our 0.05 significance level. 


### Sample Information:
Detailed Information on the analysis process is on ```real_estate_analysis.ipynb``` file, under the ```notebooks``` folder.

The IQR (interquartile range) method of outlier detection was implemented as part of the data cleansing process.

<table style="width:120%" align="center">
  <tr>
    <td>Original Total sample-size: 4,880</td>
    <td>Adjested Total sample-size: 4,318</td>
  </tr>
  <tr>
    <td>Original Equal sample-size: 1,605</td>
    <td>Adjested Equal sample-size: 1,424</td>
  </tr>
  <tr>
    <td>Original Unequal sample-size: 3,275</td>
    <td>Adjested Unequal sample-size: 2,894</td>
  </tr>
</table>
<p align="center">
  <img src="images/Original Sample.png" width="400">
  <img src="images/Adjusted Sample.png" width="400">
  <img src="images/count_tables.png">
  <img src="images/map.png">
</p>

## Technologies
<p align="center">
  <img src="images/logos.png">
</p>

Data Gathering: Beautiful Soup, Selenium<br>
Data Storage: Mongodb<br>
Data Analysis: Python 3, Numpy, Pandas, Scikit-Learn, Scipy<br>
Data Visualization: Tableau, Folium, Matplotlib, Seaborn

## Future Improvements