import pandas as pd

def load_dim_facility(df, engine):
    df.to_sql("dim_Facility", engine)
    return