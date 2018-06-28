import pandas as pd
import numpy as np

def clean_source(df):

    # drop unneeded colums
    drop = ['Age Group', 'Zip Code - 3 digits', 'Gender', 'Race', 'Ethnicity', 'Patient Disposition',\
            'Type of Admission', 'Discharge Year', 'APR MDC Code', 'APR MDC Description', 'APR Severity of Illness Code', 'APR DRG Description', \
            'APR Severity of Illness Description', 'APR Medical Surgical Description', 'Payment Typology 1', 'Payment Typology 2', 'Payment Typology 3', 'Abortion Edit Indicator', 'Emergency Department Indicator']
    df = df.drop(drop, axis=1)

    #df['Facility Id'] = df['Facility Id'].fillna(0).astype('int64')
    df['Operating Certificate Number'] = df['Operating Certificate Number'].fillna(4000).astype('int64') # use certificate # 4000 to indicate identifying information was redacted for abortion procedure

    # deal with nulls in Facility Id
    df['Facility Id'] = df['Facility Id'].fillna(4000).astype('int64') # use facility code 4000 to indicate identifying information was redacted for abortion procedure

    # deal with '120 +' in length of stay
    df['Length of Stay'] = df['Length of Stay'].replace('120 +', 120).astype('float64')

    # get rid of the $ sign in costs and parse as float
    df['Total Charges'] = df['Total Charges'].replace('[\$,]', '', regex=True).astype(float)
    df['Total Costs'] = df['Total Costs'].replace('[\$,]', '', regex=True).astype(float)

    # calculate profit in transformation to simplify reporting
    df['Total Profit'] = df['Total Charges'] - df['Total Costs']

    return df

def transform_dim_facility(df, startdate):

    # extract the facility dimension from the main DF
    dim = df.groupby(['Facility Id']).agg({
        'Health Service Area': 'first',
        'Hospital County': 'first',
        'Operating Certificate Number': 'first',
        'Facility Name': 'first'
    }).reset_index()

    # add the new SCD tracking columns
    dim['Active Flag'] = 1
    dim['Effective Start Date'] = startdate
    dim['Effective End Date'] = np.nan

    return dim

def transform_dim_diagnosis(df, startdate):

    # extract the diagnosis dimension from the main DF
    dim = df.groupby(['CCS Diagnosis Code']).agg({
        'CCS Diagnosis Description': 'first'
    }).reset_index()

    # add the new SCD tracking columns
    dim['Active Flag'] = 1
    dim['Effective Start Date'] = startdate
    dim['Effective End Date'] = np.nan

    return dim

def transform_dim_procedure(df, startdate):

    # extract the procedure dimension from the main DF
    dim = df.groupby(['CCS Procedure Code']).agg({
        'CCS Procedure Description': 'first'
    }).reset_index()

    # add the new SCD tracking columns
    dim['Active Flag'] = 1
    dim['Effective Start Date'] = startdate
    dim['Effective End Date'] = np.nan

    return dim

def transform_dim_provider(df, startdate):

    licenses = np.append(df['Attending Provider License Number'].unique(),
              df['Operating Provider License Number'].unique())

    licenses = np.append(licenses, df['Other Provider License Number'].unique())

    dim = pd.DataFrame(pd.Series(licenses).unique(), columns=['Provider License Number']).dropna()

    # now what we have got rid of the nulls, convert to int
    dim['Provider License Number'] = dim['Provider License Number'].astype(str).astype(np.int64)

    # add the new SCD tracking columns
    dim['Active Flag'] = 1
    dim['Effective Start Date'] = startdate
    dim['Effective End Date'] = np.nan
    print(dim.head(5))
    return dim

def transform_dim_patients_refine(df, startdate):
    # extract the petients refine dimension from the main DF
    dim = df.groupby(['APR DRG Code']).agg({
        'APR Risk of Mortality': 'first'
    }).reset_index()

    return dim

def transform_dim_patients(df, startdate):
    dim = df[['Age Group', 'Zip Code - 3 digits', 'Gender', 'Race', 'Ethnicity', 'Patient Disposition']].drop_duplicates()
    return dim