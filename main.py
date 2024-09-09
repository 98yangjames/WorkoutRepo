import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from dash import dash_table
from machineLearning import generate_heatmap

# Load your data
df = pd.read_csv('James_Workouts - Workouts.csv')
df['Duration'] = df['Duration'].astype(int)
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

corr_df = pd.read_csv('correlation_matrix.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Store(id='current-tab', data={'tab': 'Scatter Plot'}),  # Store for keeping track of the current tab
    
    html.H1("James' Workout Endeavors"),
    
    dcc.Tabs(
        id='tabs', 
        value='Scatter Plot', 
        children=[
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
                            ),
                            style={'flex': '1', 'padding': '10px'}
                        )
                    ], style={'display': 'flex', 'justify-content': 'space-between'})
                ])
            ]),

            dcc.Tab(label='Analysis', value='Analysis', children=[
                html.Div([
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
        fig = px.scatter(df, x=xaxis_column, y=yaxis_column, trendline='rolling', color='Activity', trendline_options=dict(window=5), hover_data=['Date'])

    elif xaxis_column == 'Month' and yaxis_column == 'Duration':
        fig = px.bar(df, x=xaxis_column, y=yaxis_column, color='Activity', hover_data=['Activity', 'Date'])

    else:
        fig = px.scatter(df, x=xaxis_column, y=yaxis_column, hover_data=['Date'])
    
    return fig, table_columns, table_data_1, table_columns, table_data_2

# # Callback to store the current tab value in the dcc.Store component
# @app.callback(
#     Output('current-tab', 'data'),
#     [Input('tabs', 'value')]
# )
# def store_current_tab(tab):
#     return {'tab': tab}

# # Callback to restore the tab value from the dcc.Store component
# @app.callback(
#     Output('tabs', 'value'),
#     [Input('current-tab', 'data')],
#     [State('tabs', 'value')]  # To avoid the circular dependency
# )
# def restore_current_tab(data, current_tab):
#     if data is None:
#         return current_tab
#     return data.get('tab', current_tab)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
