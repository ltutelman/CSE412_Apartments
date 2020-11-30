import psycopg2
import pandas as pd
from config import config


params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

apartmentInfo = create_pandas_table('SELECT * FROM public."Apartment"')
print(apartmentInfo)

cur.close()
conn.close()

