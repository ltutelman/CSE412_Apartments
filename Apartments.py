import psycopg2
import pandas as pd

conn = psycopg2.connect(
    host="tempe-apartment-db.caehuq3iuf1m.us-east-1.rds.amazonaws.com",
    database="postgres",
    port="5432",
    user="masterUser",
    password="masterPassword123!")

cur = conn.cursor()
#print('PostgreSQL database version:')
#cur.execute('SELECT version()')
#db_version = cur.fetchone()
#print(db_version)

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

apartmentInfo = create_pandas_table('SELECT * FROM public."Apartment"')
print(apartmentInfo)

cur.close()
conn.close()

