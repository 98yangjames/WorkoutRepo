import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output
from components.layout import create_layout
from helpers.load import get_data_from_google
from helpers.utils import get_table_data, get_predicted_table_data
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Data processing
df = get_data_from_google()

# Set the layout for the app
app.layout = create_layout(df)

# Define callbacks
from components.callbacks import register_callbacks
register_callbacks(app, df)

if __name__ == '__main__':
    app.run_server(debug=True)
