import pandas as pd
from sklearn.preprocessing import LabelEncoder
import plotly.express as px



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
