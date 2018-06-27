import pandas as pd

def load_dim(dim, table_name, engine):
    dim.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=100)
    return