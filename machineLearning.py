import pandas as pd
import numpy as np
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

def load_weight_df():
    df = pd.read_csv('James_Weight.csv')
    df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y, %I:%M %p')
    df['Weight'] = df['Weight'].str.replace('lb', '').astype(float)
    df['Muscle Mass'] = df['Muscle Mass'].replace('--', np.nan)
    df['Muscle Mass'] = df['Muscle Mass'].str.replace('lb', '').astype(float)
    return df


def generate_linear_regression():
    df = pd.read_csv('James_Workouts - Workouts.csv')
    running_df = df[df['Activity'] == 'Running'] 
    model = LinearRegression()
    running_df['ordinal'] = range(1, len(running_df) + 1)
    model.fit(running_df[['ordinal']], running_df[['Duration']])
    days_in_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
    arr = []
    for i in range(1, 365):
        arr.append([i])
    predicted_value = model.predict(arr)
    return round(predicted_value.sum()/len(running_df[['ordinal']]))

def generate_weight():
    df = load_weight_df()
    fig = px.scatter(df, x='Time', y = 'Weight', color ='Muscle Mass', title='My Weight Progression')
    return fig

def generate_weight_trend():
    df = load_weight_df()
    fig = px.scatter(df, x='Time', y = 'Weight', color ='Weight', title='My Weight Trendline')
    fig.update_traces(mode='lines+markers')
    return fig

def generate_heatmap():
    df = pd.read_csv('James_Workouts - Workouts.csv')

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
