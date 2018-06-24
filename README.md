# Repo for the healthcare cost Data Warehouse codebase

## Prerequisites for development ##

* Python 3 (64-bit)
* Microsoft SQL Server 2016 (for local db development)
* Get the source data from Kaggle and put it at ./source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv

## Database configuration ##

The following environment variables must be set to configure python's database connections securely. Here is how to do it on windows:

```console
set SERVER=<your computer name>\SQLEXPRESS
set DB_USER=<your user name>
set DB_PASSWORD=<your password>
```
