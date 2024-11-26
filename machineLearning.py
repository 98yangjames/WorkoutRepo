import pandas as pd
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import calendar
from datetime import datetime
import json
from dotenv import load_dotenv
import os


# Load .env file
load_dotenv()

def get_data_from_google():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    google_credentials = json.loads(os.getenv('MY_JSON'))

    creds = Credentials.from_service_account_info(google_credentials, scopes=scopes)
    #creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1qLDf_YFvXjH0rcMwyCwNdo47191hA9gEMEj8VWOj7_U"
    sheet = client.open_by_key(sheet_id)
    df = pd.DataFrame(sheet.sheet1.get_all_values())
    df.columns = df.iloc[0]
    df = df.drop(0)
    return df

def generate_linear_regression():
    df = get_data_from_google()
    running_df = df[df['Activity'] == 'Running'] 
    model = LinearRegression()
    running_df['ordinal'] = range(1, len(running_df) + 1)
    model.fit(running_df[['ordinal']], running_df[['Distance']])
    days_in_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
    arr = []
    for i in range(1, 365):
        arr.append([i])
    predicted_value = model.predict(arr)
    return round(predicted_value.sum())

def generate_heatmap():
    df = get_data_from_google()

    le = LabelEncoder()
    df['Duration'] = df['Duration'].astype(int)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Activity'] = df['Activity'].astype(str)
    df['Type'] = df['Type'].astype(str)
    
    df['ActivityEncoded'] = le.fit_transform(df['Activity'])
    df['DateEncoded'] = le.fit_transform(df['Date'])
    df['TypeEncoded'] = le.fit_transform(df['Type'])

    correlation_matrix = df[['Duration', 'DateEncoded', 'Month', 'ActivityEncoded', 'TypeEncoded']].corr()
    correlation_matrix = correlation_matrix.rename(columns={'Unnamed: 0' : 'Column'})
    
    correlation_matrix.to_csv('correlation_matrix.csv')
    # # Create the heatmap
    heatmap_fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu_r', 
                    title='Correlation Heatmap across Activities')
    
    return heatmap_fig
