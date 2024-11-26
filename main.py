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
from dotenv import load_dotenv
import os
import json

def convert_pace(pace_float):
    minutes = int(pace_float)  # Get the integer part as minutes
    seconds = int((pace_float - minutes) * 60) 


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
# Load your data
try:
    df = get_data_from_google()
except ValueError as e:
    print("Couldn't get API Data, loading cached data")
    print('Error here: ', e)
    df = pd.read_csv('James_Workouts - Workouts.csv')

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

def get_table_data():

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

    # Generate data for the table
    table_data = []
    for activity in activities:
        filtered_df = activity["filter"](df)
        current_year_df = filtered_df[filtered_df['Date'].dt.year == current_year]
        table_data.append({
            "activity": activity["name"],
            "hours": f"{round(filtered_df['Duration'].sum() / 60, 3)} Hours",
            "average": f"{round(filtered_df['Duration'].mean(), 3) if not filtered_df.empty else 0} Minutes",
            "occurances": str(len(filtered_df)),
            "current_occurances": str(len(current_year_df))
        })
    return table_data
# List of image file paths or URLs
image_folder = "assets"
image_list = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# Define the layout of the app
app.layout = html.Div([
    dcc.Store(id='current-tab', data={'tab': 'Scatter Plot'}),  # Store for keeping track of the current tab
    html.H1("James' Workout Endeavors", style = {"textAlign": "center"}),
    html.Div([
        html.Button("◀", id="prev-button", n_clicks=0, style={"fontSize": "24px"}),
        html.Img(id="slideshow-image", style={"width": "auto", "height": "1000px", "margin": "0 10px"}),
        html.Button("▶", id="next-button", n_clicks=0, style={"fontSize": "24px"})
    ], style={"display": "flex", "alignItems": "center", "justifyContent": "center", "gap": "10px"}),

    dcc.Store(id="current-image-index", data=0),  # Track the current image index
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
                    {"name": "Total Times (Current)", "id": "current_occurances"},
                    
                ],
                data=get_table_data()
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


## Callbacks
@app.callback(
    Output("slideshow-image", "src"),
    Output("current-image-index", "data"),
    Input("prev-button", "n_clicks"),
    Input("next-button", "n_clicks"),
    State("current-image-index", "data")
)
def update_slideshow(prev_clicks, next_clicks, current_index):
    # Calculate new index based on which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return image_list[current_index], current_index
    
    trigger = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if trigger == "prev-button":
        new_index = (current_index - 1) % len(image_list)  # Wrap around to the last image
    elif trigger == "next-button":
        new_index = (current_index + 1) % len(image_list)  # Wrap around to the first image
    else:
        new_index = current_index
    
    return image_list[new_index], new_index

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
