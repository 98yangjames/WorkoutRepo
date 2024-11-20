import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash import dash_table
from machineLearning import generate_heatmap, generate_linear_regression
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def convert_pace(pace_float):
    minutes = int(pace_float)  # Get the integer part as minutes
    seconds = int((pace_float - minutes) * 60) 

def get_data_from_google():
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1qLDf_YFvXjH0rcMwyCwNdo47191hA9gEMEj8VWOj7_U"
    sheet = client.open_by_key(sheet_id)
    df = pd.DataFrame(sheet.sheet1.get_all_values())
    df.columns = df.iloc[0]
    df = df.drop(0)
    return df



# Load your data
df = get_data_from_google()

df['Duration'] = df['Duration'].astype(int)
# Replace empty strings with NaN
df['Distance'] = df['Distance'].replace('', np.nan)
df['Distance'] = df['Distance'].astype(float)
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month
df['Pace'] = df['Duration'] / df['Distance']
# Get the current year
current_year = datetime.now().year
corr_df = pd.read_csv('correlation_matrix.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Store(id='current-tab', data={'tab': 'Scatter Plot'}),  # Store for keeping track of the current tab
    html.H1("James' Workout Endeavors", style = {"textAlign": "center"}),
    html.Img(
    src="/assets/IMG_8157.png",
    style={
        "height": "1000px",  # Adjust height
        "width": "auto",   # Keep aspect ratio
        #"float" : "left",
        "display": "block",
        "margin": "0 auto",  # Center the image
    },
    ),
    html.Br(),
    dcc.Tabs(
        id='tabs', 
        value='Overview', 
        children=[
            dcc.Tab(label = 'Overview', value = 'Overview', children = [
            html.B("*Current denotes this year"),
            dash_table.DataTable(
            id='workout-summary-table',
            columns=[
                {"name": "Activity", "id": "activity"},
                {"name": "Hours", "id": "hours"},
                {"name": "Average", "id": "average"},
                {"name": "Total Times (Lifetime)", "id": "occurances"},
                {"name": "Total Times (Current)", "id" : "current_occurances"}
            ],
            data = [
                {
                    "activity": "Total Workouts",
                    "hours": str(round(df['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df)),
                    "current_occurances": str(len(df[df['Date'].dt.year == current_year]))
                },
                {
                    "activity": "Running",
                    "hours": str(round(df[df['Activity'] == 'Running']['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df[df['Activity'] == 'Running']['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df[df['Activity'] == 'Running'])),
                    "current_occurances": str(len(df[(df['Activity'] == 'Running') & (df['Date'].dt.year == current_year)]))
                },
                {
                    "activity": "Lifting",
                    "hours": str(round(df[df['Activity'] == 'Lifting']['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df[df['Activity'] == 'Lifting']['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df[df['Activity'] == 'Lifting'])),
                    "current_occurances": str(len(df[(df['Activity'] == 'Lifting') & (df['Date'].dt.year == current_year)]))
                },
                {
                    "activity": "Basketball",
                    "hours": str(round(df[df['Activity'] == 'Basketball']['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df[df['Activity'] == 'Basketball']['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df[df['Activity'] == 'Basketball'])),
                    "current_occurances": str(len(df[(df['Activity'] == 'Basketball') & (df['Date'].dt.year == current_year)]))
                },
                {
                    "activity": "Pickleball",
                    "hours": str(round(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Pickleball')]['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Pickleball')]['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Pickleball')])),
                    "current_occurances": str(len(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Pickleball') & (df['Date'].dt.year == current_year)]))
                },
                {
                    "activity": "Hiking",
                    "hours": str(round(df[(df['Activity'] == 'Hiking')]['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df[(df['Activity'] == 'Hiking')]['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df[(df['Activity'] == 'Hiking')])),
                    "current_occurances": str(len(df[(df['Activity'] == 'Hiking') & (df['Date'].dt.year == current_year)]))
                },
                {
                    "activity": "Tennis",
                    "hours": str(round(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Tennis')]['Duration'].sum() / 60, 3)) + " Hours",
                    "average": str(round(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Tennis')]['Duration'].mean(), 3)) + " Minutes",
                    "occurances": str(len(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Tennis')])),
                    "current_occurances": str(len(df[(df['Activity'] == 'Outdoor') & (df['Type'] == 'Tennis') & (df['Date'].dt.year == current_year)]))
                },
            ],


            style_table={'width': '50%', 'margin': 'auto'},
            style_cell={'textAlign': 'center'},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'lightgrey'},
            style_data_conditional=[
                {'if': {'column_id': 'activity'}, 'textAlign': 'left'}
            ]
            ),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': year, 'value': year} for year in df['Date'].dt.year.unique()],
                value='All',  # Default value is "All"
                clearable=False,
                style={
                    'width': '50%',
                    'margin': '20px auto',  # Center and add margin around the dropdown
                    'padding': '10px',
                    'font-size': '18px',  # Larger font size for readability
                    'border-radius': '8px',  # Rounded edges
                    'border': '1px solid lightgrey',  # Subtle border
                    'background-color': '#f9f9f9',  # Light background to match the page
                    'text-align': 'center'
                }
            ),
            # Plotly graph
            dcc.Graph(id='yearly-plot'),
            dcc.Graph(id = 'yearly-pie')

            ]),
            dcc.Tab(label='Scatter Plot', value='Scatter Plot', children=[
                html.Div([
                    html.Div([
                        html.B('Select an X-axis and Y-Axis!'),
                        dcc.Dropdown(
                            id='xaxis-column',
                            options=[{'label': col, 'value': col} for col in df.columns],
                            value='Date',
                            style={'width': '200px'}
                        ),
                        
                        dcc.Dropdown(
                            id='yaxis-column',
                            options=[{'label': col, 'value': col} for col in df.columns],
                            value='Duration',
                            style={'width': '200px', 'margin-left': '10px'}
                        )
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),
                    dcc.Graph(id='scatter-plot'),

                    html.Div([
                        html.Div(
                            dash_table.DataTable(
                                id='selected-columns-table-1',
                                style_table={'width': '100%', 'margin': 'auto'},
                                style_cell={'textAlign': 'center'},
                                style_cell_conditional=[
                                    {'if': {'column_id': 'x'}, 'width': '20%'},
                                    {'if': {'column_id': 'y'}, 'width': 'auto'}
                                ],
                                sort_action = 'native',
                            ),
                            style={'flex': '1', 'padding': '10px'}
                        ),
                        html.Div(
                            dash_table.DataTable(
                                id='selected-columns-table-2',
                                style_table={'width': '100%', 'margin': 'auto'},
                                style_cell={'textAlign': 'center'},
                                style_cell_conditional=[
                                    {'if': {'column_id': 'x'}, 'width': '20%'},
                                    {'if': {'column_id': 'y'}, 'width': 'auto'}
                                ],
                                sort_action = 'native',
                            ),
                            style={'flex': '1', 'padding': '10px'}
                        )
                    ], style={'display': 'flex', 'justify-content': 'space-between'})
                ])
            ]),

            dcc.Tab(label='Analysis', value='Analysis', children=[
                html.Div([
                    html.H1(str(round(generate_linear_regression()/60)) + " Hours Running Predicted for next year"),
                    dcc.Graph(id='heatmap-plot', figure=generate_heatmap(), style={'width': '80%', 'height': '600px'}),
                    dash_table.DataTable(
                        id='dataframe-table',
                        columns=[{'name': i, 'id': i} for i in corr_df.columns],
                        data=corr_df.to_dict('records'),
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'center'},
                        sort_action='native',
                    ),
                ])
            ]),
        ]
    ),
])

# Callback to update graph based on selected year
@app.callback(
    Output('yearly-plot', 'figure'),
    Output('yearly-pie', 'figure'),
    Input('year-dropdown', 'value')
)
def update_graph_dropdown(selected_year):
    if selected_year == 'All':
        filtered_df = df
    else:
        # Filter DataFrame by selected year
        filtered_df = df[df['Date'].dt.year == selected_year]
    
    # Create a Plotly visualization (example: bar chart)
    fig = px.bar(filtered_df, x='Date', y='Duration', title=f'Values for the year {selected_year}', color = 'Activity')
    fig2 = px.pie(filtered_df, names = 'Activity', values = 'Duration', title = f"Distribution of Time per Workout for {selected_year}")
    return fig, fig2



# Callback to update the scatter plot and DataTables based on user input
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('selected-columns-table-1', 'columns'),
     Output('selected-columns-table-1', 'data'),
     Output('selected-columns-table-2', 'columns'),
     Output('selected-columns-table-2', 'data')],
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')]
)
def update_graph(xaxis_column, yaxis_column):
    table_data_1 = df[[xaxis_column, yaxis_column]].iloc[:len(df)//2].to_dict('records')
    table_data_2 = df[[xaxis_column, yaxis_column]].iloc[len(df)//2:].to_dict('records')

    table_columns = [
        {"name": xaxis_column, "id": xaxis_column},
        {"name": yaxis_column, "id": yaxis_column}
    ]
    
    fig = px.scatter()
    if xaxis_column == 'Date' and yaxis_column == 'Duration':
        fig = px.scatter(df, x=xaxis_column, y=yaxis_column, trendline='rolling', color='Activity', trendline_options=dict(window=5))
    
    elif xaxis_column == 'Distance' and yaxis_column == 'Duration':
        window_size = 10
        df['trendline'] = df['Duration'].rolling(window=window_size).mean()
        df['color'] = np.where(df['Duration'] < df['trendline'], 'red', 'blue')
        fig = px.scatter(df, x=xaxis_column, y=yaxis_column, trendline='rolling', color='Duration', trendline_options=dict(window=5), hover_data=['Date', 'Activity'])

    elif xaxis_column == 'Month' and yaxis_column == 'Duration':
        fig = px.bar(df, x=xaxis_column, y=yaxis_column, color='Activity', hover_data=['Activity', 'Date'])

    elif xaxis_column == 'Activity' and yaxis_column == 'Duration' or xaxis_column == 'Duration' and yaxis_column == 'Activity':
        fig = px.scatter(df, x = xaxis_column, y=yaxis_column, hover_data=['Date'])
        y_avg = df[yaxis_column].mean()
        fig.add_hline(y=y_avg, line_dash="dash", annotation_text=f"Average: {y_avg:.2f}", line_color="red")


    else:
        fig = px.scatter(df, x=xaxis_column, y=yaxis_column, hover_data=['Date'])
    
    return fig, table_columns, table_data_1, table_columns, table_data_2




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
