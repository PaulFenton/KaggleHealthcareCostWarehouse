# Repo for the healthcare cost Data Warehouse codebase

## Prerequisites for development ##

* Python 3 (64-bit)
* Microsoft SQL Server 2016 (for local db development)

The source data file is not versioned, get it from Kaggle or the Google shared drive and put it in a folder called "source_data"
The path should be ./source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv

## Database configuration ##

The following environment variables must be set to configure python's database connections securely. Here is how to do it on windows:

```console
set SERVER=<your computer name>\SQLEXPRESS
set DB_USER=<your user name>
set DB_PASSWORD=<your password>
```
