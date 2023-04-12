import psycopg2
import pandas as pd

HOST = "localhost"
USER = "postgres"
PASSWORD = "847468"
DATABASE = "glycoenzdb"
FILE = "data/GlycoEnzOntoDB.xlsx"
TABLE_NAME = "GlycoDB"


# Connect to the database
conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)
cursor = conn.cursor()

# Read the excel file
df = pd.read_excel(FILE)

# Replace NaN values with NULL
df = df.where((pd.notnull(df)), 'NULL')

# Drop the table
drop_table_query = f"DROP TABLE IF EXISTS {TABLE_NAME};";
cursor.execute(drop_table_query)

# Create the table
create_table_query = f"CREATE TABLE {TABLE_NAME} ({','.join([f'{column} TEXT' for column in df.columns])});"
cursor.execute(create_table_query)

# Iterate over the rows of the dataframe and insert into the database
for index, row in df.iterrows():
    values = [row[column] for column in df.columns]
    query = f"INSERT INTO {TABLE_NAME} ({','.join(df.columns)}) VALUES {tuple(values)}"
    cursor.execute(query)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()