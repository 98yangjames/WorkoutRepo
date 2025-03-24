import plotly.express as px

def generate_heatmap():
    # Generate heatmap logic here
    fig = px.density_heatmap(data_frame=df, x='Date', y='Activity')
    return fig
