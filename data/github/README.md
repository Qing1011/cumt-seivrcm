# Disparities

The repository contains auxiliary data and code relevant to the modeling
effort for the COVID-19 Scenario Modeling Hub Research Disprities rounds

For any questions or issues please feel free to open an issue on the 
GitHub.

## [Contact Matrix](./contact_matrix)

We produced synthetic daily contact matrices by race/ethnicity in 
the household, school, community, workplace setting using methodology 
described in 
[Mistry et al. 2021](https://www.nature.com/articles/s41467-020-20544-y) and 
[Aleta et al. 2022](https://www.pnas.org/doi/10.1073/pnas.2112182119).

For more information, please consult the associated [README.md](./contact_matrix/README.md)


## [Population data](./population_data)

The folder contains state population structure by age and race/ethnicity.

- [population_data.csv](./population_data/population_data.csv): contains
state state population stucture by age and race/ethnicity separately from 
the [United States Census, 2020](https://www.census.gov/quickfacts/fact/table/NC,CA/PST045222)


## [Serology](./serology)

The serology data was extracted from the CDC COVID Data Tracker,
[2020-2021 Nationwide COVID-19 Infection- and Vaccination-Induced Antibody Seroprevalence (Blood donations)](https://covid.cdc.gov/covid-data-tracker/#nationwide-blood-donor-seroprevalence )

The nationwide blood donor seroprevalence survey estimates the
percentage of the U.S. population ages 16 and older that have
developed antibodies against SARS-CoV-2. The dataset includes 
seroprevalence from both infection and both vaccination (combined) 
and infection for three regions in California and one region in
North Carolina by major racial/ethnic groups. 

Blood donor data represents a biased sample, so differences between 
racial/ethnic groups should be interpreted conservatively. 
Several other serological studies were conducted throughout the study period:

*California*: Cross-sectional serological studies conducted within a hospital 
network from February 4-17, 2021, indicate the risk of infection for Hispanic/Latino
is [~5x](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9068757/) that of White 
individuals aged 18-64. Another serological study found that incidence was 
[7.5x](https://academic.oup.com/ofid/article/8/8/ofab379/6329153) higher for 
Hispanic/Latino populations and 
[2.4x](https://academic.oup.com/ofid/article/8/8/ofab379/6329153) higher for
Black population compared to White populations from August-December 2020.
Notably, the latter study adjusted sampling techniques to attempt to reach 
comparable coverage by race/ethnicity.

*North Carolina:* Serological samples collected from a network of hospitals 
from 10/25/2020 - 12/26/2020 indicated that seroprevalence was 
[1.8x](https://journals.asm.org/doi/full/10.1128/msphere.00841-21) higher among 
Black individuals and 
[3.9x](https://journals.asm.org/doi/full/10.1128/msphere.00841-21) higher among 
Hispanic/Latino individuals compared to White populations.

## [Target data](./target-data)

This folder contains the Phase 1 and Phase 2 calibration targets for California
and North Carolina, including incident cases and deaths by race/ethnicity. It
also contains the supporting overall-case and source files documented in its
[README](./target-data/README.md).

## [Target death data](./target-data-death)

This folder contains the corresponding Phase 1 and Phase 2 case-and-death target
files used in the disparities modeling work. See its
[README](./target-data-death/README.md) for the date ranges, demographic groups,
and source description.

## [Vaccination](./vaccination)

This folder contains weekly vaccination data by key demographics for 
California and North Carolina. We provide the number of individuals 
receiving at least 1 dose (`"partial_vax"`) and fully vaccinated 
(`"full_vax"`) by age ('demographic_category' = 'age') and by 
race/ethnicity ('demographic_category' = 'race_ethnicity'). Age is 
broken down into '0-17', '18-49', '50-64', '65+', and 'unknown'
and race/ethnicity is broken down into 'asian','white','black',
'latino', 'other', and 'unknown', as denoted in 'demographic_value'.

Source data: 

- [California Department of Public Health COVID-19 Vaccine Progress Dashboard](https://data.ca.gov/dataset/covid-19-vaccine-progress-dashboard-data)
- [North Carolina Department of Health and Human Services COVID-19 Dashboard Data - Data Behind the Dashboards](https://covid19.ncdhhs.gov/dashboard/data-behind-dashboards)

For more detailed information on vaccine efficacy and vaccine rollout
schedule assumptions, please consult the Scenario Description associated with
the disparities SMH round, available on the 
[COVID-19 Scenario Modeling Hub - Research GitHub repository](https://github.com/midas-network/covid19-smh-research)



