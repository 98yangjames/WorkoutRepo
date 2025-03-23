import os
import json
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv

LOCAL = True
dotenv_path = '.env'

def get_data_from_google():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = {}
    if LOCAL:
        # Load credentials
        creds = Credentials.from_service_account_file("offline.json", scopes=scopes)
        print(creds)
    else:
        try:
            google_credentials = json.loads(os.getenv('MY_JSON'))
            creds = Credentials.from_service_account_info(google_credentials, scopes=scopes)
        except TypeError as e:
            print("Error: ", e)
    
    client = gspread.authorize(creds)
    sheet_id = "1qLDf_YFvXjH0rcMwyCwNdo47191hA9gEMEj8VWOj7_U"
    sheet = client.open_by_key(sheet_id)
    df = pd.DataFrame(sheet.sheet1.get_all_values())
    df.columns = df.iloc[0]
    df = df.drop(0)
    return df

def connect_to_sql():

    load_dotenv(dotenv_path)
    conn = pymysql.connect(
        host=os.environ.get("host"),
        user=os.environ.get("user"),
        password=os.environ.get("password"),
        database=os.environ.get("database"),
        port=int(os.environ.get("port"))
    )
    cursor = conn.cursor()
    return cursor

def query_print(query):
    cursor = connect_to_sql()
    cursor.execute(query)
    for c in cursor.fetchall():
        print(c)
    cursor.close()

def query_df(query):
    cursor = connect_to_sql()
    cursor.execute(query)
    column_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    # for c in rows:
    #     print(c)

    df = pd.DataFrame(rows, columns = column_names)
    cursor.close()
    return df

def create_sqlalchemy_engine():
    connection_string = f"mysql+pymysql://{os.environ.get('user')}:{os.environ.get('password')}@{os.environ.get('host')}:{os.environ.get('port')}/{os.environ.get('database')}"
    engine = create_engine(connection_string)
    return engine
'''
MYSQL Database has the following column datatypes:
    Date: date
    Activity: varchar(100)
    Distance: float
    Type: varchar(45)
    Duration: decimal(10,2)
'''
def updateDB():
    df = get_data_from_google()
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Activity'] = df['Activity'].astype(str)
    df['Distance'] = df['Distance'].replace('', np.nan)
    df['Distance'] = df['Distance'].astype(float)
    df['Type'] = df['Type'].astype(str)
    df['Duration'] = df['Duration'].astype(float).round(2)
    print(df.dtypes)
    # print(df)

    existing_df = query_df("SELECT * FROM Workouts")

    additional_rows = len(df) - len(existing_df)

    inserting_df = df[len(existing_df): len(existing_df) + additional_rows]
    # Create the SQLAlchemy engine
    engine = create_sqlalchemy_engine()
    db = 'Workouts'
    rows_inserted = inserting_df[['Date', 'Activity', 'Distance', 'Type', 'Duration']].to_sql(db, con=engine, if_exists='append', index=False)
    print(f"Inserted {rows_inserted} rows into the database: " + db)

updateDB()
