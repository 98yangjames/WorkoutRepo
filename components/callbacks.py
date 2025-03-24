from dash.dependencies import Input, Output
from helpers.utils import get_table_data, get_predicted_table_data
import plotly.express as px
import numpy as np

def register_callbacks(app, df):
    @app.callback(
        Output('yearly-plot', 'figure'),
        Output('yearly-pie', 'figure'),
        Output('yearly-scatter', 'figure'),
        Input('year-dropdown', 'value')
    )
    def update_graph_dropdown(selected_year):
        if selected_year == 'All':
            filtered_df = df
        else:
            filtered_df = df[df['Date'].dt.year == selected_year]

        fig = px.bar(filtered_df, x='Date', y='Duration', title=f'Values for the year {selected_year}', color='Activity')
        fig.update_layout(autosize=True)
        fig2 = px.pie(filtered_df, names='Activity', values='Duration', title=f"Distribution of Time per Workout for {selected_year}")
        fig3 = px.scatter(filtered_df, x = 'Date', y= 'Duration', title = f'Values for the year {selected_year}', color='Duration', trendline='ols')

        return fig, fig2, fig3

    # Callback to update the scatter plot and DataTables based on user input
    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value')]
    )
    def update_graph(xaxis_column, yaxis_column):

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
            fig = px.scatter(df, x = 'Activity', y='Duration', hover_data=['Date'], color = 'Duration')
            y_avg = df['Duration'].mean()
            fig.add_hline(y=y_avg, line_dash="dash", annotation_text=f"Average: {y_avg:.2f}", line_color="red")

        elif xaxis_column not in df.columns or yaxis_column not in df.columns:
            return px.scatter(title="Select an X and Y Axis Value")
        else:
            fig = px.scatter(df, x=xaxis_column, y=yaxis_column, title=f'{xaxis_column} vs {yaxis_column}')
        
        fig.update_layout(
        autosize=True,  # Allow the graph to resize dynamically
        )
        return fig
    
    @app.callback(
    Output('xaxis-column', 'options'),
    Output('yaxis-column', 'options'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value')
    )
    def update_dropdown_options(selected_x, selected_y):
        x_options = [{'label': col, 'value': col} for col in df.columns if col != selected_y]
        y_options = [{'label': col, 'value': col} for col in df.columns if col != selected_x]
        return x_options, y_options