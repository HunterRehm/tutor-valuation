import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_valuation(revenue_data):
    """
    Calculate business valuation based on:
    1. Current annual revenue
    2. Growth trajectory (monthly slope * 12)
    3. Conservative revenue multiple (1.1x) applied to:
       - Current annual revenue
       - Plus one year of projected growth
    """
    # Calculate current revenue metrics
    monthly_revenue = np.array(revenue_data['data'][0]['y'])
    annual_revenue = monthly_revenue.sum()
    avg_monthly_revenue = monthly_revenue.mean()
    
    # Calculate growth trend
    X = np.array(range(len(monthly_revenue))).reshape(-1, 1)
    y = monthly_revenue.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    
    # Extract growth metrics
    monthly_growth = model.coef_[0][0]  # Slope represents $/month growth
    projected_annual_growth = monthly_growth * 12  # Project growth for next 12 months
    
    # Valuation components
    base_value = annual_revenue  # Current annual revenue
    growth_value = projected_annual_growth  # Projected 12-month growth
    revenue_multiple = 1.1  # Conservative multiple for small tutoring business
    
    # Final valuation calculation
    revenue_based_value = (base_value + growth_value) * revenue_multiple
    
    # Prepare metrics for display
    valuation_metrics = {
        'Business Value': f"${revenue_based_value:,.2f}",
        'Base Annual Revenue': f"${base_value:,.2f}",
        'Projected Annual Growth': f"${growth_value:,.2f}",
        'Monthly Growth Rate': f"${monthly_growth:,.2f}/month",
        'Revenue Multiple': f"{revenue_multiple}x",
        'Monthly Revenue (Avg)': f"${avg_monthly_revenue:,.2f}"
    }
    
    # Include calculation explanation
    valuation_explanation = {
        'method': 'Revenue-based valuation with growth projection',
        'formula': '(Annual Revenue + 12-month Growth) × Multiple',
        'components': {
            'annual_revenue': base_value,
            'growth_projection': growth_value,
            'multiple': revenue_multiple,
            'reasoning': """
                1. Uses current annual revenue as base value
                2. Adds one year of projected growth based on current trend
                3. Applies 1.1x multiple (conservative for education business)
                4. Growth projection uses linear regression of monthly revenue
            """
        }
    }
    
    return valuation_metrics, valuation_explanation 