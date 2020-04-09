# Journalists-Under-Fire
An analysis of attacks on journalists and press freedom.

**IN PROGRESS**

# Overview

A free press is a vital component of deomcracy. 

Some of the questions I had in mind when conducting the analysis included:
- Are there any trends over time? Has being a journalist become more or less dangerous?
- Spatial trends; which countries are the most dangerous for journalists?
- What types of issues are most dangerous to cover?
- What specific jobs are the most dangerous?
- What are the most common sources of attacks on journalists?


# Data 

## Sources
The [Committee to Protect Journalists](https://cpj.org/) (CPJ) maintains a worldwide [database](https://cpj.org/data/) of press workers killed or imprisoned since 1992, and information/circumstances surrounding each event.


## Description of Raw Data

### Journalist Deaths since 1992
This data set has x rows and x columns. The majority of the columns are categorical in nature. 

### Journalists Imprisoned since 1992
This data set has x rows and x columns. The majority of the columns are categorical in nature. 


## Data Cleaning and Manipulation

- Drop any columns that contain all null values, or very few non-null values.
- Further narrow data by dropping columns that don't contain useful imformation for analysis.
- Use only cases w/ confirmed motive for journalist deaths.
- There were many instances, especially in the journalists imprisoned dataset, where a category value was entered in multiple different ways (capitalization, spaces etc.) and needed to be cleaned up before analysis.
- There were several categorical columns that contained rows listing multiple categories (as a single string). I had to separate these before I could aggregate/count. *insert example?*

* Show head(df) for final cleaned dataframes?


### Glimpse of final journalist deaths dataframe
|    |   year | fullName           | gender   | employedAs   | jobs           | coverage                  | mediums   | country   | localOrForeign   | charges    | lengthOfSentence
|---:|-------:|:-------------------|:---------|:-------------|:---------------|:--------------------------|:----------|:----------|:-----------------|:-----------|:-------------------|
|  0 |   2018 | Aasif Sultan       | Male     | Staff        | Print Reporter | Human Rights,Politics,War | Print     | India     | Local            | Anti-State | Sentence pending   |
|  1 |   2019 | Aasif Sultan       | Male     | Staff        | Print Reporter | Human Rights,Politics,War | Print     | India     | Local            | Anti-State | Sentence pending   |
|  2 |   1997 | Abay Hailu         | Male     | Staff        | Print Reporter | Human Rights,Politics     | Print     | Ethiopia  | Local            | nan        | 0-5 Years          |
|  3 |   1993 | Abbas Abdi         | Male     | nan          | Editor         | nan                       | Print     | Iran      | Local            | nan        | 0-5 Years          |
|  4 |   2011 | Abd al-Karim Thail | Male     | Staff        | Editor         | Politics                  | Internet  | Yemen     | Local            | No Charge  | Not Sentenced      |


### Glimpse of final journalist imprisoned dataframe
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>year</th>
      <th>fullName</th>
      <th>gender</th>
      <th>employedAs</th>
      <th>jobs</th>
      <th>coverage</th>
      <th>mediums</th>
      <th>country</th>
      <th>localOrForeign</th>
      <th>charges</th>
      <th>lengthOfSentence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018</td>
      <td>Aasif Sultan</td>
      <td>Male</td>
      <td>Staff</td>
      <td>Print Reporter</td>
      <td>Human Rights,Politics,War</td>
      <td>Print</td>
      <td>India</td>
      <td>Local</td>
      <td>Anti-State</td>
      <td>Sentence pending</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019</td>
      <td>Aasif Sultan</td>
      <td>Male</td>
      <td>Staff</td>
      <td>Print Reporter</td>
      <td>Human Rights,Politics,War</td>
      <td>Print</td>
      <td>India</td>
      <td>Local</td>
      <td>Anti-State</td>
      <td>Sentence pending</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1997</td>
      <td>Abay Hailu</td>
      <td>Male</td>
      <td>Staff</td>
      <td>Print Reporter</td>
      <td>Human Rights,Politics</td>
      <td>Print</td>
      <td>Ethiopia</td>
      <td>Local</td>
      <td>NaN</td>
      <td>0-5 Years</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1993</td>
      <td>Abbas Abdi</td>
      <td>Male</td>
      <td>NaN</td>
      <td>Editor</td>
      <td>NaN</td>
      <td>Print</td>
      <td>Iran</td>
      <td>Local</td>
      <td>NaN</td>
      <td>0-5 Years</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2011</td>
      <td>Abd al-Karim Thail</td>
      <td>Male</td>
      <td>Staff</td>
      <td>Editor</td>
      <td>Politics</td>
      <td>Internet</td>
      <td>Yemen</td>
      <td>Local</td>
      <td>No Charge</td>
      <td>Not Sentenced</td>
    </tr>
  </tbody>
</table>
</div>




# Analysis/Results

## There doesn't appear to be a consistent trend in the number of journalists killed over time. We see a spike in the early 1990's (why?Bosnian war?), and then another general increase from ~2003-2018.
![](images/TotalDeathsVsYear.png)

## Looking at the distribution by country, the top 2 are Iraq and Syria, where there have been recent wars. 
![](images/TotalDeathsByCountry.png)

## Map of total number of deaths by country, 1992-present.
![](images/DeathsByCountryMap.png)


## gif! shows counts each year
![](images/DeathByCountry.gif)


## Looking at the distribution by type of coverage, the most dangerous topics to cover are politics, war, human rights, and corruption.
![](images/TotalDeathsByCoverage.png)

![](images/TotalDeathsByJob.png)


![](images/TotalDeathsBysourcesOfFire.png)
![](images/TotalDeathsByTypeOfDeath.png)

## There does seem to be an general upward trend in the number of journalists imprisoned over time. Note the increase around 1995, similar to what we saw in the number of journalist deaths.
![](images/N_imprisonedByYear.png)

## The distribution by country is very different from that for journalist deaths. China and Turkey are significantly worse, followed by Eritrea and Iran.
![](images/N_imprisonedBycountry.png)


## Map of total imprisoned by country since 1992
![](images/ImprisonedByCountryMap.png)

## gif! shows counts each year
![](images/ImprisonedByCountry.gif)



## 
![](images/N_imprisonedBycoverage.png)

## The most common charge is by far 'Anti-State'
![](images/N_imprisonedBycharges.png)

![](images/N_imprisonedByjobs.png)
![](images/N_imprisonedBymedium.png)
![](images/N_imprisonedBylengthOfSentence.png)


# Summary
- A large number of journalists are in danger of being killed or imprisoned.
- Journalist deaths are largely related to wars.
- In contrast, journalist imprisonment appears to be largely related to political coverage and anti-state charges.
- 


# Code / Reproducing Analysis

/src folder contains all scripts needed to reproduce analysis and generate figures.

- Option in script to download new updated data?

- List of packages/versions?






