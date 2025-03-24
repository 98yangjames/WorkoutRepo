from dash import dash_table
from dash import dcc, html
from helpers.utils import get_table_data

def create_layout(df):
    return html.Div([
        dcc.Store(id='current-tab', data={'tab': 'Scatter Plot'}),  # Store for keeping track of the current tab
        html.H1("James' Workout Endeavors", style={"textAlign": "center"}),
        html.Br(),
        dcc.Tabs(
            id='tabs', 
            value='Overview', 
            children=[
                dcc.Tab(label='Overview', value='Overview', children=[
                    html.Div([
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
                            style_table={'width': '100%', 'overflowX': 'auto'},
                            style_cell={'textAlign': 'center', 'padding': '10px'},
                            style_cell_conditional=[
                                {'if': {'column_id': 'activity'}, 'width': '30%'},
                                {'if': {'column_id': 'hours'}, 'width': '15%'},
                                {'if': {'column_id': 'average'}, 'width': '15%'},
                                {'if': {'column_id': 'occurances'}, 'width': '20%'},
                                {'if': {'column_id': 'current_occurances'}, 'width': '20%'}
                            ],
                        ),
                        html.Br(),

                        # Year Selection Section (Styled)
                        html.Div([
                            html.Label("📅 Select Year:", style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#2c3e50', 'marginRight': '10px'}),
                            dcc.RadioItems(
                                id='year-dropdown',
                                options=[{'label': 'All', 'value': 'All'}] + [{'label': year, 'value': year} for year in df['Date'].dt.year.unique()],
                                value=2025,  # Default value
                                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
                            ),
                        ], style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '10px', 'box-shadow': '2px 2px 10px #ccc', 'marginBottom': '20px'}),

                        # Graphs Section (Styled)
                        html.Div([
                            dcc.Graph(id='yearly-plot'),
                            dcc.Graph(id='yearly-pie'),
                            dcc.Graph(id='yearly-scatter'),
                        ], style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '10px', 'box-shadow': '2px 2px 10px #ccc'})
                    ], style={'padding': '20px'})
                ]),

                dcc.Tab(label='Scatter Plot', value='Scatter Plot', children=[
                    html.Div([
                        # X-Axis Selection
                        html.Div([
                            html.Label("Select X-Axis:", style={'fontSize': '16px', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.Dropdown(
                                id='xaxis-column',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value='Date',
                                style={'width': '250px'}
                            ),
                        ], style={'display': 'flex', 'align-items': 'center', 'marginBottom': '10px'}),

                        # Y-Axis Selection
                        html.Div([
                            html.Label("Select Y-Axis:", style={'fontSize': '16px', 'fontWeight': 'bold', 'marginRight': '10px'}),
                            dcc.Dropdown(
                                id='yaxis-column',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value='Duration',
                                style={'width': '250px'}
                            ),
                        ], style={'display': 'flex', 'align-items': 'center', 'marginBottom': '20px'}),

                        # Scatter Plot (Styled)
                        html.Div([
                            dcc.Graph(id='scatter-plot')
                        ], style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '10px', 'box-shadow': '2px 2px 10px #ccc'})
                    ], style={'padding': '20px'})
                ]),
            
                # About Tab
                dcc.Tab(label='About', value='About', children=[
                    html.Div([
                        html.H2("About Me", style={'textAlign': 'center', 'color': '#2c3e50'}),
                        html.Br(),

                        # Profile Image Placeholder
                        html.Div([
                            html.Img(
                                src="https://via.placeholder.com/150",  # Replace with your actual image URL
                                style={
                                    'width': '150px',
                                    'height': '150px',
                                    'border-radius': '50%',
                                    'object-fit': 'cover',
                                    'box-shadow': '2px 2px 10px rgba(0, 0, 0, 0.2)',
                                    'marginBottom': '20px'
                                }
                            )
                        ], style={'textAlign': 'center'}),

                        # Description Section
                        html.Div([
                            html.P("Hi, I'm James! This is a short paragraph about me and my fitness journey.", 
                                   style={'textAlign': 'justify', 'lineHeight': '1.6'}),
                            html.P("I started tracking my workouts to stay motivated and improve my performance.", 
                                   style={'textAlign': 'justify', 'lineHeight': '1.6'}),
                            html.P("Feel free to explore my stats and progress in the other tabs.", 
                                   style={'textAlign': 'justify', 'lineHeight': '1.6'}),
                        ], style={'maxWidth': '600px', 'margin': 'auto'}),

                        html.Br(),

                        # Contact or Links Section
                        html.Div([
                            html.P("📧 Contact: james@example.com", style={'textAlign': 'center', 'fontWeight': 'bold'}),
                            html.P("🔗 Follow me on [GitHub](https://github.com) | [LinkedIn](https://linkedin.com)", 
                                   style={'textAlign': 'center', 'fontWeight': 'bold'})
                        ], style={'marginTop': '20px'})
                    ], style={
                        'padding': '30px', 
                        'border': '1px solid #ddd', 
                        'border-radius': '10px', 
                        'box-shadow': '2px 2px 10px #ccc',
                        'textAlign': 'center',
                        'maxWidth': '800px',
                        'margin': 'auto'
                    })
                ])
            ]
        ),
    ])
