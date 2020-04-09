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
The [Committee to Protect Journalists](https://cpj.org/) (CPJ) maintains a worldwide [database](https://cpj.org/data/) of press workers killed since 1992, and information/circumstances surrounding each death.

The [US Press Freedom Tracker](https://pressfreedomtracker.us/) maintains a [database](https://pressfreedomtracker.us/data/) of press freedom violations/attacks on the press in the US.

## Description of Raw Data

### Journalist Deaths since 1992
This data set has x rows and x columns. The majority of the columns are categorical in nature. 

### Journalists Imprisoned since 1992
This data set has x rows and x columns. The majority of the columns are categorical in nature. 


## Data Cleaning and Manipulation

- Drop any columns that contain all NaN values
- Drop columns not useful for analysis.
- Use only confirmed motive in analysis?
- Some rows in 'coverage' column contain multiple categories; separate these?


# Analysis/Results

## There doesn't appear to be a consistent trend in the number of journalists killed over time. We see a spike in the early 1990's (why?Bosnian war?), and then another general increase from ~2003-2018.
![](images/TotalDeathsvsYear.png)

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






