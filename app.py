from dash import Dash, html, dcc
import json
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
from valuation_analysis import calculate_valuation
import os

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# This needs to be named 'application' for Render
application = app.server
server = application  # Keep this for backwards compatibility

# Load and calculate
try:
    with open('monthly_earnings.json', 'r') as f:
        revenue_figure = json.load(f)
except FileNotFoundError:
    # Generate the revenue figure if it doesn't exist
    from valuation import plot_monthly_earnings
    revenue_figure = plot_monthly_earnings('revenue.csv', 'monthly_earnings.json')

# Get valuation metrics and explanation
valuation_metrics, valuation_explanation = calculate_valuation(revenue_figure)
business_value = valuation_metrics.pop('Business Value')
other_metrics = valuation_metrics

# Extract revenue data for other stats
monthly_revenue = np.array(revenue_figure['data'][0]['y'])
revenue_stats = {
    'Revenue Growth': f"{((monthly_revenue[-1] - monthly_revenue[0]) / monthly_revenue[0] * 100):,.1f}%",
    'Highest Month': f"${monthly_revenue.max():,.2f}",
    'Lowest Month': f"${monthly_revenue.min():,.2f}"
}

# Create the layout
app.layout = html.Div([
    # Header
    html.H1('Business Valuation Dashboard', style={'textAlign': 'center', 'margin': '20px'}),
    
    # Valuation Section
    html.Div([
        html.H2('Business Valuation Analysis', 
                style={'textAlign': 'center', 'margin': '20px', 'color': '#003f5c'}),
        
        # Business Value (Featured)
        html.Div([
            html.H3('Estimated Business Value', 
                   style={'textAlign': 'center', 'color': '#2f4b7c', 'marginBottom': '10px'}),
            html.P(business_value, 
                  style={
                      'fontSize': '48px',
                      'fontWeight': 'bold',
                      'textAlign': 'center',
                      'color': '#003f5c',
                      'margin': '20px'
                  }),
            # Calculation Method
            html.Div([
                html.H4('Calculation Method', 
                       style={'color': '#2f4b7c', 'marginTop': '20px'}),
                html.P(f"Formula: {valuation_explanation['formula']}", 
                      style={'fontSize': '16px', 'margin': '10px'}),
                html.Div([
                    html.P(line.strip(), style={'margin': '5px'}) 
                    for line in valuation_explanation['components']['reasoning'].split('\n') 
                    if line.strip()
                ], style={'marginLeft': '20px'})
            ], style={'textAlign': 'left', 'marginTop': '20px'})
        ], style={
            'backgroundColor': 'white',
            'padding': '30px',
            'margin': '20px auto',
            'borderRadius': '10px',
            'boxShadow': '0 6px 12px 0 rgba(0,0,0,0.2)',
            'maxWidth': '800px',
            'border': '2px solid #003f5c'
        }),
        
        # Supporting Metrics
        html.Div([
            html.Div([
                html.Div([
                    html.H4(key, style={'margin': '10px', 'color': '#2f4b7c'}),
                    html.P(value, style={
                        'fontSize': '24px',
                        'fontWeight': 'bold',
                        'margin': '10px',
                        'color': 'black'
                    })
                ], style={
                    'backgroundColor': 'white',
                    'border': '1px solid #dee2e6',
                    'borderRadius': '5px',
                    'padding': '15px',
                    'margin': '10px',
                    'textAlign': 'center',
                    'flex': '1'
                }) for key, value in other_metrics.items()
            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-around',
                'margin': '20px'
            })
        ])
    ], style={
        'backgroundColor': '#f8f9fa',
        'padding': '20px',
        'margin': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
    }),

    # Revenue Section
    html.Div([
        html.H2('Revenue Details', style={'textAlign': 'center', 'margin': '20px'}),
        dcc.Graph(
            id='monthly-revenue-graph',
            figure=revenue_figure,
            config={
                'scrollZoom': False,
                'doubleClick': False,
                'showTips': False,
                'displayModeBar': False,
                'dragMode': False,
                'staticPlot': True,
                'responsive': True
            }
        ),
        
        # Additional revenue metrics
        html.Div([
            html.Div([
                html.Div([
                    html.H4(key, style={'margin': '10px'}),
                    html.P(value, style={'fontSize': '24px', 'fontWeight': 'bold', 'margin': '10px'})
                ], style={
                    'backgroundColor': 'white',
                    'border': '1px solid #dee2e6',
                    'borderRadius': '5px',
                    'padding': '15px',
                    'margin': '10px',
                    'textAlign': 'center',
                    'flex': '1'
                }) for key, value in revenue_stats.items()
            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'justifyContent': 'space-around',
                'margin': '20px'
            })
        ])
    ], style={
        'backgroundColor': 'white',
        'padding': '20px',
        'margin': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.2)'
    })

], style={'padding': '20px', 'backgroundColor': '#f8f9fa'})

# Add port configuration for Render
port = int(os.getenv('PORT', 8080))

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port) 