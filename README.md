# Austin Real Estate Analysis

Austin’s real estate market is undeniably on the rise.  The growing economy and been a highlight of the cities allure, along with being named the best place to live in the US on 3 consecutive years: 2017, 2018, and 2019 by U.S News & World Report.  My analysis dives into the current Austin real estate market, from a bedroom to bathroom ratio starting point.  Does the bed-to-bath ratio of homes have a statistical impact to the value of homes?   


## Table of Contents

* [General Information](#general-information)
    * [Data Gathering](#data-gathering)
    * [Hypothesis Testing](#hypothesis-testing)
    * [Methodology](#methodology)
* [Technologies](#technologies)
    * [Database](#database)
    * [Python](#python)
    * [Visualization](#visualization)
* [Setup](#setup)


## General Information
Investing in a home is a milestone many aim to achieve, whether viewed as just a starter home or potential AirBnB investment, it all begins with data.  This project began with just a simple believe to be tested: The ratio between bedrooms to bathrooms have an impact on home values. But it’s potential with further enrichment is quite limitless. 

![](images/distributions.png)

### Data Gathering:


### Hypothesis Testing:

###### Step 1: Set up the hypothesis
The null hypothesis is that the ratio between bedrooms to bathrooms has no statistically significant difference to the mean value of homes.

Alternative hypothesis is that there is a significant difference to the mean value

>**Ho : μ = 0**

>**Ho : μ != 0**

###### Step 2: Select test statistic
To test this hypothesis the z-test was chosen.
The significance level was set at: 0.05

A z-test is a statistical test used to determine whether two population means are different when the variances are known and the sample size is large.

<p align="center">
  <img src="images/z-statistic.png">
</p>

###### Step 3: Set up decision rule

<p align="center">
  <img src="images/decisionrule.png">
</p>
###### Step 4: Compute the test statistic

![](images/z-score.png)

###### Step 5: Conclusion

Sample information:
-------------------------------
Adjusted equal sample-size: 1,424 <br> 
Adjusted unequal sample-size: 2,894


### Methodology:

Data used in the study included square footage, number of beds, baths, and value for all single and multi-family homes, condo, and townhomes with active listings in the Austin housing market from December 2019 to January 2020, inside the city limits.  This data was used to calculate averages and test for significance between equal ratio vs unequal ratio homes. All figures shown in the article represent the mean value for each data point unless otherwise specified. The IQR (interquartile range) method of outlier detection was implemented as part of the data cleansing process.

## Technologies
<div class="row">
  <div class="column">
    <img src="images/python.jpg" alt="Snow" width="80" height="60">
  </div>
  <div class="column">
    <img src="images/jupyter.png" alt="Forest" width="80" height="60">
  </div>
  <div class="column">
    <img src="images/mongodb.jpeg" alt="Mountains" width="80" height="60">
  </div>
</div>
Python:{libraries} pandas, scipy, matplotlib, pymongo, sklearn, folium
Mongodb
Tableau
Docker

## Setup