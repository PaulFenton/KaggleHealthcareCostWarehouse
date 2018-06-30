# Repo for Kaggle SPARCS Healthcare database ETL & Data Warehouse Creation

## Overview

The Statewide Planning and Research Cooperative System (SPARCS) Inpatient De-identified File contains discharge level detail on patient characteristics, diagnoses, treatments, services, and charges. This github repo contains the python ETL code required to prepare and populate a star-schema from this dataset in a SQL Server database.

The original source data can be found on Kaggle:

https://health.data.ny.gov/Health/Hospital-Inpatient-Discharges-SPARCS-De-Identified/82xm-y6g8

## ETL Script Description

Two main driver scripts are used to control the flow:
* <b>main.py</b> - this file controls the main source transformation, dimension creation, fact table encoding, and populating the star schema on the database
* <b>secondary_load.py</b> - this file performs some manual changes to demonstrate how the warehouse should be updated to handle a Slowly Changing Dimension (Type II) change.

## Prerequisites for development ##

* Python 3 (64-bit)
* Microsoft SQL Server 2016 (for local db development)
* Get the source data from Kaggle and put it at ./source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv

## Database configuration ##

The following environment variables must be set to configure python's database connections securely. Here is how to do it on windows:

```console
set SERVER=<your computer name>\SQLEXPRESS
set DB_NAME=<your database name>
set DB_USER=<your user name>
set DB_PASSWORD=<your password>
```
If you are using a local database as in this example, the 'DB_USER' and 'DB_PASSWORD' will not be used, and replaced by windows authentication on a trusted connection.
