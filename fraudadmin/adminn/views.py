
from django.shortcuts import render
import pandas as pd
from sqlalchemy import create_engine

# Database connection details
db_user = 'postgres'
db_password = 'azbycx567'
db_host = 'localhost'
db_port = '5432'
db_name = 'frauddetection'
table_name = 'transactions'

# CSV file path
csv_file_path = 'C:/Users/HomePC/CS2024/RTFS/balanced_data.csv'

# Create a connection to the database
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Push the DataFrame to the database
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f"Data successfully pushed to the table '{table_name}' in the database '{db_name}'.")
