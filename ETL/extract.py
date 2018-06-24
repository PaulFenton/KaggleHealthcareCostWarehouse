import pandas as pd
def read_source_file():
    # specify the column types to be read from the csv
    initial_types = {
        'Health Service Area': object,
        'Hospital County': object,
        'Operating Certificate Number': object,
        'Facility Id': object,
        'Facility Name': object,
        'Age Group': object,
        'Zip Code - 3 digits': object,
        'Gender': object,
        'Race': object,
        'Ethnicity': object,
        'Length of Stay': object,
        'Type of Admission': object,
        'Patient Disposition': object,
        'Discharge Year': "int64",
        'CCS Diagnosis Code': "int64",
        'CCS Diagnosis Description': object,
        'CCS Procedure Code': "int64",
        'CCS Procedure Description': object,
        'APR DRG Code': "int64",
        'APR DRG Description': object,
        'APR MDC Code': "int64",
        'APR MDC Description': object,
        'APR Severity of Illness Code': "int64",
        'APR Severity of Illness Description': object,
        'APR Risk of Mortality': object,
        'APR Medical Surgical Description': object,
        'Payment Typology 1': object,
        'Payment Typology 2': object,
        'Payment Typology 3': object,
        'Attending Provider License Number': object,
        'Operating Provider License Number': object,
        'Other Provider License Number': object,
        'Birth Weight': "float64",
        'Abortion Edit Indicator': object,
        'Emergency Department Indicator': object,
        'Total Charges': object,
        'Total Costs': object
    }

    # 2.4 M rows in csv need to be read into a dataframe in chunks
    list = []
    for chunk in pd.read_csv("../source_data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv", dtype=initial_types, chunksize=20000, low_memory=False, error_bad_lines=False):
        list.append(chunk)
    df = pd.concat(list, axis=0)
    del list

    return df

def clean_source(df):

    # deal with nulls in Operating Certificate Number
    #df['Facility Id'] = df['Facility Id'].fillna(0).astype('int64')
    df['Operating Certificate Number'] = df['Operating Certificate Number'].fillna(4000).astype('int64') # use certificate # 4000 to indicate identifying information was redacted for abortion procedure

    # deal with nulls in Facility Id
    df['Facility Id'] = df['Facility Id'].fillna(4000).astype('int64') # use facility code 4000 to indicate identifying information was redacted for abortion procedure

    # deal with '120 +' in length of stay
    df['Length of Stay'] = df['Length of Stay'].replace('120 +', 120).astype('float64')

    # get rid of the $ sign in costs and parse as float
    df['Total Charges'] = df['Total Charges'].replace('[\$,]', '', regex=True).astype(float)
    df['Total Costs'] = df['Total Costs'].replace('[\$,]', '', regex=True).astype(float)

    # add some calculated columns to simplify reporting # todo should we do this?
    df['Total Profit'] = df['Total Charges'] - df['Total Costs']
    df['Profit Margin'] = df['Total Profit'].divide(df['Total Charges'])

    return df

def extract_dim_facility(df):
    #subset the dataframe to only useful columns
    dim_facility = df.groupby(['Facility Id'])['Total Charges'].sum()
    return