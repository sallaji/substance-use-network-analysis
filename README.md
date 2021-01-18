# Substance use analysis

Detailed information about the contents of this project can be found at the main `sna_main.ipynb` jupyter notebook

## Database source

### Database provider

The National Household Survey on Drug Abuse(NSDUH), is the largest source of statistical information on the use of 
illicit drugs, alcohol, and tobacco and on mental health issues in the united states.


### Data Source

This database holds answers to questions about substance use, mental illness and treatments for these disorders among 
civilians of the united states aged 12 or older. It consists of 56,136 records on the 2019 National Survey on Drug Use 
and Health (NSDUH) public use data file (PUF) and contains 2,741 variables. Detailed information can be accessed online 
at [the Substance Abuse & Mental Health Services Administration(SAMHSA)](https://datafiles.samhsa.gov/)

## Data Collection

### Data fetching, reading and writing

Several service classes were created for handling the process of fetching, collecting and preprocessing the raw data 
required for this social network analysis project (see sna_main.ipynb as well as the source code
for further information).

### Raw Dataset

|QUESTID2|FILEDATE|MJEVER|...|IRFAMIN3|INCOME|
|:---:|:---:|:---:|:---:|:---:|:---:|
|11015143|10/08/2019|1|...|1|1|

The table above is a simplified version of the data set of which `QUESTID2` corresponds to the **Unique ID** of the 
individual observation and `FILEDATE` is the **database creation date**. The majority of the remaining variables such 
as **MJEVER** correspond to a question related to one of the substance use, demographics, mental health, and social 
environment sections included in the survey. The cell value under each header variable name corresponds to the code 
related to the option chosen in that specific question. 

The meaning of the value codes may vary depending on the question addressed. This [codebook](https://www.datafiles.samhsa.gov/sites/default/files/field-uploads-protected/studies/NSDUH-2019/NSDUH-2019-datasets/NSDUH-2019-DS0001/NSDUH-2019-DS0001-info/NSDUH-2019-DS0001-info-codebook.pdf) provides detailed information 
about the meaning of the value codes available for each addressed question. Alternatively, you can consult the 
sna_main.ipynb file in order to get a better idea of how those different meanings are built and which features have been selected for this analysis.
