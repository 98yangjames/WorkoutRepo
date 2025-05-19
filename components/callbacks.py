from dash.dependencies import Input, Output
from helpers.utils import get_table_data, get_predicted_table_data
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
# Define a consistent color mapping for activities
ACTIVITY_COLORS = {
    "Running": "#1f77b4",
    "Lifting": "#ff7f0e",
    "Basketball": "#2ca02c",
    "Pickleball": "#d62728",
    "Hiking": "#9467bd",
    "Tennis": "#8c564b",
    "Other": "#e377c2"  # Default color for any other activity
}

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
            # Create a subplot for pie charts, one for each year, arranged horizontally
            unique_years = filtered_df['Date'].dt.year.unique()
            fig2 = make_subplots(
                rows=1, cols=len(unique_years),  # One row, multiple columns
                subplot_titles=[f"Year: {year}" for year in unique_years],
                specs=[[{'type': 'domain'}] * len(unique_years)]  # Single row, multiple columns
            )
            
            for i, year in enumerate(unique_years):
                year_df = filtered_df[filtered_df['Date'].dt.year == year]
                pie_chart = px.pie(
                    year_df,
                    names='Activity',
                    values='Duration',
                    color='Activity',
                    color_discrete_map=ACTIVITY_COLORS
                )
                pie_chart.update_traces(
                    hovertemplate="<b>%{label}</b><br>Percentage: %{percent:.2%}<extra></extra>"
                )
                fig2.add_traces(pie_chart.data, rows=1, cols=i + 1)  # Add to the correct column
            
            fig2.update_layout(
                title="Distribution of Time per Workout for All Years",
                width=400 * len(unique_years),  # Adjust width dynamically based on the number of years
                showlegend=False
            )
        else:
            filtered_df = df[df['Date'].dt.year == selected_year]
            # Single pie chart for the selected year
            fig2 = px.pie(
                filtered_df, 
                names='Activity', 
                values='Duration', 
                title=f"Distribution of Time per Workout for {selected_year}",
                color='Activity',
                color_discrete_map=ACTIVITY_COLORS
            )
            fig2.update_traces(
                hovertemplate="<b>%{label}</b><br>Percentage: %{percent:.2%}<extra></extra>"
            )

        # Bar and scatter plots remain unchanged
        fig = px.bar(
            filtered_df, 
            x='Date', 
            y='Duration', 
            title=f'Values for the year {selected_year}', 
            color='Activity',
            color_discrete_map=ACTIVITY_COLORS
        )
        fig.update_layout(autosize=True)

        fig3 = px.scatter(
            filtered_df, 
            x='Date', 
            y='Duration', 
            title=f'Values for the year {selected_year}', 
            color='Activity', 
            trendline='ols',
            color_discrete_map=ACTIVITY_COLORS
        )

        return fig, fig2, fig3
    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('xaxis-column', 'value'),
         Input('yaxis-column', 'value')]
    )
    def update_graph(xaxis_column, yaxis_column):
        fig = px.scatter()
        if xaxis_column == 'Date' and yaxis_column == 'Duration':
            fig = px.scatter(
                df, 
                x=xaxis_column, 
                y=yaxis_column, 
                trendline='rolling', 
                color='Activity', 
                trendline_options=dict(window=5),
                color_discrete_map=ACTIVITY_COLORS
            )
        elif xaxis_column == 'Distance' and yaxis_column == 'Duration':
            window_size = 10
            df['trendline'] = df['Duration'].rolling(window=window_size).mean()
            df['color'] = np.where(df['Duration'] < df['trendline'], 'red', 'blue')
            fig = px.scatter(
                df, 
                x=xaxis_column, 
                y=yaxis_column, 
                trendline='rolling', 
                color='Activity', 
                trendline_options=dict(window=5), 
                hover_data=['Date', 'Activity'],
                color_discrete_map=ACTIVITY_COLORS
            )
        elif xaxis_column == 'Month' and yaxis_column == 'Duration':
            fig = px.bar(
                df, 
                x=xaxis_column, 
                y=yaxis_column, 
                color='Activity', 
                hover_data=['Activity', 'Date'],
                color_discrete_map=ACTIVITY_COLORS
            )
        elif xaxis_column == 'Activity' and yaxis_column == 'Duration' or xaxis_column == 'Duration' and yaxis_column == 'Activity':
            fig = px.scatter(
                df, 
                x='Activity', 
                y='Duration', 
                hover_data=['Date'], 
                color='Activity',
                color_discrete_map=ACTIVITY_COLORS
            )
            y_avg = df['Duration'].mean()
            fig.add_hline(y=y_avg, line_dash="dash", annotation_text=f"Average: {y_avg:.2f}", line_color="red")
        elif xaxis_column not in df.columns or yaxis_column not in df.columns:
            return px.scatter(title="Select an X and Y Axis Value")
        else:
            fig = px.scatter(
                df, 
                x=xaxis_column, 
                y=yaxis_column, 
                title=f'{xaxis_column} vs {yaxis_column}',
                color='Activity',
                color_discrete_map=ACTIVITY_COLORS
            )
        
        fig.update_layout(
            autosize=True,  # Allow the graph to resize dynamically
        )
        return fig