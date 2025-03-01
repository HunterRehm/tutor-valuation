import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import numpy as np
import json

def plot_monthly_earnings(csv_file, output_path='monthly_earnings.json'):
    # Load the CSV file
    df = pd.read_csv(csv_file, parse_dates=['Date'])
    colors = ["#003f5c", "#ffa600"]
    month_rev = {}
    year = '2024'
    
    # Calculate monthly revenue
    for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        total = 0
        for row in df.iterrows():
            date, subject, amount = list(row[1])
            date = date.split('/')
            if date[0] == month and date[2] == year:
                total += amount
        month_rev[month] = total

    # Prepare data for regression
    x = np.array([[int(i)] for i in month_rev.keys()])
    y = np.array([float(i) for i in month_rev.values()])
    model = LinearRegression()
    model.fit(x, y)
    pred_y = model.predict(x)

    # Create the data structure for Plotly
    plot_data = {
        'data': [
            {
                'type': 'bar',
                'x': list(month_rev.keys()),
                'y': y.tolist(),
                'marker': {'color': colors[0]},
                'name': 'Monthly Revenue'
            },
            {
                'type': 'scatter',
                'x': list(month_rev.keys()),
                'y': pred_y.tolist(),
                'mode': 'lines',
                'line': {'width': 3, 'color': colors[1]},
                'name': 'Trend Line'
            }
        ],
        'layout': {
            'title': 'Monthly Revenue Trend',
            'xaxis': {'title': 'Month'},
            'yaxis': {'title': 'Revenue ($)'},
            'template': 'plotly_white',
            'showlegend': True,
            'legend': {
                'yanchor': 'top',
                'y': 0.99,
                'xanchor': 'right',
                'x': 0.99
            },
            'margin': {'t': 50, 'l': 50, 'r': 50, 'b': 50}
        }
    }

    # Save as JSON
    with open(output_path, 'w') as f:
        json.dump(plot_data, f)
    
    print(f"Plot data saved to {output_path}")

    # Return the data structure if needed
    return plot_data

# Example usage
plot_monthly_earnings('revenue.csv')