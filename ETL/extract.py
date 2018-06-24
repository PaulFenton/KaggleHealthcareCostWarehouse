import pandas as pd
def read_source_file():
    print('reading source file..')
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

    print('done!')
    return df

def extract_dim_facility(df):

    df = df.groupby(['Facility Id']).agg({
        'Health Service Area': 'first',
        'Hospital County': 'first',
        'Operating Certificate Number': 'first',
        'Facility Name': 'first'
    }).reset_index()
    return df