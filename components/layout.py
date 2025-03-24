from dash import dash_table
from dash import dcc, html
from helpers.utils import get_table_data

def create_layout(df):
    return html.Div([
        dcc.Store(id='current-tab', data={'tab': 'Scatter Plot'}),  # Store for keeping track of the current tab
        html.H1("James' Workout Endeavors", style = {"textAlign": "center"}),
        html.Br(),
        dcc.Tabs(
            id='tabs', 
            value='Overview', 
            children=[
                dcc.Tab(label='Overview', value='Overview', children=[
                    html.P("This is my workout page. You're welcome to follow my amazing workouts :)"),
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
                        data=get_table_data(df),
                        style_table={'width': '100%', 'overflowX': 'auto'},  # Full width with horizontal scroll
                        style_cell={'textAlign': 'center', 'padding': '10px'},  # Center text and add padding
                        style_cell_conditional=[
                            {'if': {'column_id': 'activity'}, 'width': '30%'},  # Activity column gets 30% of the width
                            {'if': {'column_id': 'hours'}, 'width': '15%'},
                            {'if': {'column_id': 'average'}, 'width': '15%'},
                            {'if': {'column_id': 'occurances'}, 'width': '20%'},
                            {'if': {'column_id': 'current_occurances'}, 'width': '20%'}
                        ],
                    ),
                    html.Br(),
                    # Year Dropdown with Styling
                    html.Div([
                        html.Label("📅 Select Year:", style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#2c3e50', 'marginRight': '10px'}),
                        dcc.RadioItems(
                            id='year-dropdown',
                            options=[{'label': 'All', 'value': 'All'}] + [{'label': year, 'value': year} for year in df['Date'].dt.year.unique()],
                            value=2025,  # Default value
                            labelStyle={'display': 'inline-block', 'marginRight': '5px'}  # Inline display with spacing
                        ),
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'}),
                    dcc.Graph(id='yearly-plot'),
                    dcc.Graph(id='yearly-pie'),
                    dcc.Graph(id='yearly-scatter'),
                ]),
                dcc.Tab(label='Scatter Plot', value='Scatter Plot', children=[
                    html.Div([
                        html.Div([
                            html.Label("Select X-Axis:", style={'font-weight': 'bold', 'margin-right': '10px'}),
                            dcc.Dropdown(
                                id='xaxis-column',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value='Date',
                                style={'width': '250px'}
                            ),
                        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),

                        html.Div([
                            html.Label("Select Y-Axis:", style={'font-weight': 'bold', 'margin-right': '10px'}),
                            dcc.Dropdown(
                                id='yaxis-column',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value='Duration',
                                style={'width': '250px'}
                            ),
                        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),

                        dcc.Graph(id='scatter-plot')
                    ], style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '10px', 'box-shadow': '2px 2px 10px #ccc'})
                ]),




                # Other tabs like 'Scatter Plot', 'Weight', etc., go here.
            ]
        ),
    ])
