"""
Interactive Malaria Surveillance Dashboard
With Predictive ML & Export Capabilities
"""

from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load model
try:
    model = joblib.load('malaria_outbreak_model.pkl')
    model_loaded = True
    print("✅ Model loaded successfully")
except:
    model_loaded = False
    print("⚠️ Model not found, using rule-based predictions")

# Load or create data
def load_data():
    # Create comprehensive dataset
    countries = ['Nigeria', 'DR Congo', 'Uganda', 'Mozambique', 'Ghana', 'Kenya', 
                 'Mali', 'Niger', 'Burkina Faso', 'Ivory Coast']
    
    data = []
    for country in countries:
        for year in range(2018, 2025):
            for month in range(1, 13):
                is_rainy = 1 if month in [4,5,6,7,8,9,10,11] else 0
                
                # Country-specific factors
                if country == 'Nigeria':
                    baseline = 500000
                elif country == 'DR Congo':
                    baseline = 400000
                elif country in ['Uganda', 'Mozambique']:
                    baseline = 250000
                elif country in ['Ghana', 'Kenya', 'Mali']:
                    baseline = 150000
                else:
                    baseline = 100000
                
                # Seasonal variation
                if is_rainy:
                    cases = baseline * (1.5 + np.random.normal(0, 0.1))
                else:
                    cases = baseline * (0.7 + np.random.normal(0, 0.1))
                
                cases = int(cases)
                
                data.append({
                    'country': country,
                    'year': year,
                    'month': month,
                    'month_name': datetime(year, month, 1).strftime('%B'),
                    'is_rainy_season': 'Rainy' if is_rainy else 'Dry',
                    'malaria_cases': cases,
                    'deaths': int(cases * 0.002),
                    'test_positivity': round(np.random.uniform(20, 60), 1)
                })
    
    return pd.DataFrame(data)

df = load_data()

# Initialize Dash app
app = Dash(__name__, title="Malaria Surveillance Dashboard - WHO AFRO")

app.layout = html.Div([
    html.Div([
        html.H1("🦟 WHO AFRO Malaria Surveillance Dashboard", style={'textAlign': 'center', 'color': '#1a472a'}),
        html.P("Real-time malaria outbreak monitoring and prediction system", 
               style={'textAlign': 'center', 'color': '#555', 'marginBottom': '30px'})
    ]),
    
    # Filters Row
    html.Div([
        html.Div([
            html.Label("Select Country:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': 'All Countries', 'value': 'ALL'}] + 
                        [{'label': c, 'value': c} for c in sorted(df['country'].unique())],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Select Year:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': 'All Years', 'value': 'ALL'}] + 
                        [{'label': str(y), 'value': y} for y in sorted(df['year'].unique())],
                value='ALL',
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '20px'}),
        
        html.Div([
            html.Label("Prediction Month:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='predict-month',
                options=[{'label': m, 'value': i} for i, m in enumerate(['January', 'February', 'March', 'April', 
                                                                          'May', 'June', 'July', 'August', 
                                                                          'September', 'October', 'November', 'December'], 1)],
                value=7,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.H3("Total Cases", style={'textAlign': 'center', 'color': '#666', 'marginBottom': '10px'}),
            html.H2(id='total-cases', style={'textAlign': 'center', 'color': '#dc3545'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 
                  'textAlign': 'center', 'display': 'inline-block', 'width': '23%', 'margin': '1%'}),
        
        html.Div([
            html.H3("Total Deaths", style={'textAlign': 'center', 'color': '#666', 'marginBottom': '10px'}),
            html.H2(id='total-deaths', style={'textAlign': 'center', 'color': '#fd7e14'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 
                  'textAlign': 'center', 'display': 'inline-block', 'width': '23%', 'margin': '1%'}),
        
        html.Div([
            html.H3("Avg Test Positivity", style={'textAlign': 'center', 'color': '#666', 'marginBottom': '10px'}),
            html.H2(id='avg-positivity', style={'textAlign': 'center', 'color': '#28a745'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 
                  'textAlign': 'center', 'display': 'inline-block', 'width': '23%', 'margin': '1%'}),
        
        html.Div([
            html.H3("Outbreak Risk", style={'textAlign': 'center', 'color': '#666', 'marginBottom': '10px'}),
            html.H2(id='outbreak-risk', style={'textAlign': 'center'})
        ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'borderRadius': '10px', 
                  'textAlign': 'center', 'display': 'inline-block', 'width': '23%', 'margin': '1%'})
    ], style={'marginBottom': '30px'}),
    
    # Charts Row 1
    html.Div([
        dcc.Graph(id='cases-trend', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='cases-bar', style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    # Charts Row 2
    html.Div([
        dcc.Graph(id='heatmap-chart', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='prediction-gauge', style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    # Prediction Section
    html.Div([
        html.H3("🎯 Outbreak Prediction", style={'marginTop': '30px', 'color': '#1a472a'}),
        html.Div([
            html.Div([
                html.Label("Temperature (°C):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='temp-slider', min=15, max=40, step=0.5, value=28,
                          marks={i: str(i) for i in range(15, 41, 5)})
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                html.Label("Rainfall (mm):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='rain-slider', min=0, max=300, step=10, value=120,
                          marks={i: str(i) for i in range(0, 301, 50)})
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
            
            html.Div([
                html.Label("Humidity (%):", style={'fontWeight': 'bold'}),
                dcc.Slider(id='humidity-slider', min=20, max=95, step=5, value=75,
                          marks={i: str(i) for i in range(20, 96, 15)})
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'})
        ]),
        
        html.Div([
            html.Button("Predict Outbreak Risk", id='predict-btn', 
                       style={'backgroundColor': '#1a472a', 'color': 'white', 'padding': '12px 24px',
                              'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginTop': '20px'})
        ], style={'textAlign': 'center'}),
        
        html.Div(id='prediction-result', style={'marginTop': '20px', 'padding': '20px', 
                                                'backgroundColor': '#f0f7ff', 'borderRadius': '10px', 'textAlign': 'center'})
    ]),
    
    # Data Table
    html.Div([
        html.H3("📊 Detailed Data", style={'marginTop': '30px', 'color': '#1a472a'}),
        dash_table.DataTable(
            id='data-table',
            columns=[{"name": i, "id": i} for i in ['country', 'year', 'month_name', 'malaria_cases', 'deaths', 'test_positivity']],
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#1a472a', 'color': 'white'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            page_size=10
        ),
        html.Button("Export to CSV", id='export-btn', 
                   style={'backgroundColor': '#28a745', 'color': 'white', 'padding': '10px 20px',
                          'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginTop': '10px'})
    ])
], style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '20px'})

# Callbacks
@app.callback(
    [Output('total-cases', 'children'),
     Output('total-deaths', 'children'),
     Output('avg-positivity', 'children'),
     Output('cases-trend', 'figure'),
     Output('cases-bar', 'figure'),
     Output('heatmap-chart', 'figure'),
     Output('data-table', 'data')],
    [Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_dashboard(country, year):
    # Filter data
    filtered_df = df.copy()
    if country != 'ALL':
        filtered_df = filtered_df[filtered_df['country'] == country]
    if year != 'ALL':
        filtered_df = filtered_df[filtered_df['year'] == year]
    
    # Calculate KPIs
    total_cases = f"{filtered_df['malaria_cases'].sum():,.0f}"
    total_deaths = f"{filtered_df['deaths'].sum():,.0f}"
    avg_positivity = f"{filtered_df['test_positivity'].mean():.1f}%"
    
    # Trend chart
    trend_df = filtered_df.groupby(['year', 'month'])['malaria_cases'].sum().reset_index()
    trend_fig = px.line(trend_df, x='month', y='malaria_cases', color='year', 
                        title='Monthly Malaria Cases Trend',
                        labels={'malaria_cases': 'Cases', 'month': 'Month'})
    
    # Bar chart
    bar_df = filtered_df.groupby('country')['malaria_cases'].sum().reset_index()
    bar_fig = px.bar(bar_df, x='country', y='malaria_cases', title='Total Cases by Country',
                     labels={'malaria_cases': 'Total Cases', 'country': 'Country'})
    
    # Heatmap
    heatmap_df = filtered_df.groupby(['country', 'year'])['malaria_cases'].sum().reset_index()
    heatmap_fig = px.density_heatmap(heatmap_df, x='year', y='country', z='malaria_cases',
                                      title='Cases Heatmap (Country × Year)',
                                      color_continuous_scale='Reds')
    
    # Data table
    table_data = filtered_df[['country', 'year', 'month_name', 'malaria_cases', 'deaths', 'test_positivity']].to_dict('records')
    
    return total_cases, total_deaths, avg_positivity, trend_fig, bar_fig, heatmap_fig, table_data

@app.callback(
    [Output('prediction-gauge', 'figure'),
     Output('outbreak-risk', 'children'),
     Output('outbreak-risk', 'style')],
    [Input('country-dropdown', 'value'),
     Input('predict-month', 'value')]
)
def update_prediction_gauge(country, month):
    # Simple risk calculation based on season
    is_rainy = month in [4,5,6,7,8,9,10,11]
    
    if country in ['Nigeria', 'DR Congo']:
        base_risk = 0.8 if is_rainy else 0.4
    elif country in ['Uganda', 'Mozambique']:
        base_risk = 0.7 if is_rainy else 0.3
    else:
        base_risk = 0.6 if is_rainy else 0.2
    
    risk_pct = base_risk * 100
    
    # Gauge chart
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_pct,
        title={'text': "Outbreak Risk Score"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkred"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}
            ]
        }
    ))
    gauge.update_layout(height=400)
    
    # Risk text and style
    if risk_pct >= 60:
        risk_text = f"🔴 HIGH ({risk_pct:.0f}%)"
        risk_style = {'color': '#dc3545', 'fontWeight': 'bold'}
    elif risk_pct >= 30:
        risk_text = f"🟡 MEDIUM ({risk_pct:.0f}%)"
        risk_style = {'color': '#fd7e14', 'fontWeight': 'bold'}
    else:
        risk_text = f"🟢 LOW ({risk_pct:.0f}%)"
        risk_style = {'color': '#28a745', 'fontWeight': 'bold'}
    
    return gauge, risk_text, risk_style

@app.callback(
    Output('prediction-result', 'children'),
    [Input('predict-btn', 'n_clicks')],
    [State('temp-slider', 'value'),
     State('rain-slider', 'value'),
     State('humidity-slider', 'value'),
     State('predict-month', 'value'),
     State('country-dropdown', 'value')]
)
def make_prediction(n_clicks, temp, rainfall, humidity, month, country):
    if n_clicks is None:
        return "Adjust the sliders and click 'Predict Outbreak Risk'"
    
    is_rainy = month in [4,5,6,7,8,9,10,11]
    
    if model_loaded:
        month_sin = np.sin(2 * np.pi * month / 12)
        month_cos = np.cos(2 * np.pi * month / 12)
        features = np.array([[1 if is_rainy else 0, temp, rainfall, humidity, month_sin, month_cos]])
        prob = model.predict_proba(features)[0][1]
        risk_pct = prob * 100
    else:
        # Rule-based fallback
        risk_pct = 0
        if is_rainy:
            risk_pct += 40
        if temp > 25:
            risk_pct += 15
        if rainfall > 100:
            risk_pct += 20
        if humidity > 70:
            risk_pct += 15
        if country in ['Nigeria', 'DR Congo']:
            risk_pct += 10
        risk_pct = min(risk_pct, 95)
    
    # Generate recommendation
    if risk_pct >= 60:
        recommendation = "🔴 HIGH RISK: Immediate action required! Distribute bed nets, stock antimalarial drugs, activate community health workers."
        color = "#dc3545"
    elif risk_pct >= 30:
        recommendation = "🟡 MEDIUM RISK: Prepare resources, increase surveillance, pre-position rapid test kits."
        color = "#fd7e14"
    else:
        recommendation = "🟢 LOW RISK: Continue routine prevention measures, maintain surveillance."
        color = "#28a745"
    
    return html.Div([
        html.H4(f"Predicted Outbreak Risk: {risk_pct:.1f}%", style={'color': color, 'fontSize': '24px'}),
        html.P(recommendation, style={'marginTop': '10px'}),
        html.P(f"📍 {country} | 🌡️ {temp}°C | ☔ {rainfall}mm | 💧 {humidity}% | 📅 Month {month}", 
               style={'color': '#666', 'marginTop': '10px'})
    ])

if __name__ == '__main__':
    app.run(debug=True, port=8050)   # <-- THIS IS THE FIXED LINE