import pandas as pd
import numpy as np

CURRENT_YEAR = pd.to_datetime('now').year

def get_table_data(df):
    df['Duration'] = df['Duration'].astype(int)
    # Replace empty strings with NaN
    df['Distance'] = df['Distance'].replace('', np.nan)
    df['Distance'] = df['Distance'].astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['Pace'] = df['Duration'] / df['Distance']
    

    # List of activities and their filters
    activities = [
        {"name": "Total Workouts", "filter": lambda df: df},
        {"name": "Running", "filter": lambda df: df[df['Activity'] == 'Running']},
        {"name": "Lifting", "filter": lambda df: df[df['Activity'] == 'Lifting']},
        {"name": "Basketball", "filter": lambda df: df[df['Activity'] == 'Basketball']},
        {"name": "Pickleball", "filter": lambda df: df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Pickleball')]},
        {"name": "Hiking", "filter": lambda df: df[df['Activity'] == 'Hiking']},
        {"name": "Tennis", "filter": lambda df: df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Tennis')]}
    ]

    table_data = []
    for activity in activities:
        filtered_df = activity["filter"](df)
        current_year_df = filtered_df[filtered_df['Date'].dt.year == CURRENT_YEAR]
        table_data.append({
            "activity": activity["name"],
            "hours": f"{round(filtered_df['Duration'].sum() / 60, 1)} Hours",
            "average": f"{round(filtered_df['Duration'].mean(), 1) if not filtered_df.empty else 0} Minutes",
            "occurances": str(len(filtered_df)),
            "current_occurances": str(len(current_year_df))
        })
    return table_data

def get_predicted_table_data(df):
    activities = [
        {"name": "Total Workouts", "filter": lambda df: df},
        {"name": "Running", "filter": lambda df: df[df['Activity'] == 'Running']},
        # Add other activities
    ]

    prediction_factor = 1.1  # Placeholder prediction logic
    table_data = []
    for activity in activities:
        filtered_df = activity["filter"](df)
        predicted_hours = round(filtered_df['Duration'].sum() * prediction_factor / 60, 1)
        predicted_average = round(filtered_df['Duration'].mean() * prediction_factor, 1) if not filtered_df.empty else 0
        predicted_occurances = int(len(filtered_df) * prediction_factor)
        current_year_df = filtered_df[filtered_df['Date'].dt.year == CURRENT_YEAR]

        table_data.append({
            "activity": activity["name"],
            "hours": f"{predicted_hours} Hours",
            "average": f"{predicted_average} Minutes",
            "current_occurances": str(len(current_year_df)),
            "total_times": str(predicted_occurances)
        })
    return table_data
