"""
Malaria Outbreak Prediction Model
Using Historical Cases + Weather Data
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🦟 TRAINING MALARIA OUTBREAK PREDICTION MODEL")
print("="*60)

# Generate realistic training data (simulating real WHO patterns)
np.random.seed(42)

countries = ['Nigeria', 'DR Congo', 'Uganda', 'Mozambique', 'Ghana', 'Kenya']
data = []

for country in countries:
    for month in range(1, 13):  # 12 months
        for year in range(2018, 2025):
            # Base risk factors
            is_rainy = 1 if month in [4,5,6,7,8,9,10,11] else 0
            temp = np.random.normal(28, 3) if is_rainy else np.random.normal(32, 4)
            rainfall = np.random.exponential(80) + 20 if is_rainy else np.random.exponential(15) + 5
            humidity = np.random.normal(75, 10) if is_rainy else np.random.normal(45, 15)
            
            # Country-specific baseline
            if country == 'Nigeria':
                baseline = 500000
            elif country == 'DR Congo':
                baseline = 400000
            elif country == 'Uganda':
                baseline = 250000
            elif country == 'Mozambique':
                baseline = 200000
            else:
                baseline = 150000
            
            # Calculate cases based on factors
            cases = baseline * (1 + (is_rainy * 0.6))
            cases *= (1 + (rainfall - 50) / 200)
            cases *= (1 + (humidity - 60) / 100)
            cases = int(cases + np.random.normal(0, cases * 0.1))
            
            # Outbreak label (1 if cases > threshold)
            threshold = baseline * 1.5
            outbreak = 1 if cases > threshold else 0
            
            data.append({
                'country': country,
                'year': year,
                'month': month,
                'is_rainy_season': is_rainy,
                'temperature_c': round(temp, 1),
                'rainfall_mm': round(rainfall, 1),
                'humidity_pct': round(humidity, 1),
                'malaria_cases': cases,
                'outbreak': outbreak
            })

df = pd.DataFrame(data)

# Feature engineering
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# Features for prediction
feature_cols = ['is_rainy_season', 'temperature_c', 'rainfall_mm', 'humidity_pct', 
                'month_sin', 'month_cos']

X = df[feature_cols]
y = df['outbreak']  # Predict outbreak (1) or not (0)

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model trained!")
print(f"   Accuracy: {accuracy:.1%}")
print(f"   Features: {feature_cols}")

# Feature importance
importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n📊 Feature Importance:")
for _, row in importance.iterrows():
    print(f"   {row['feature']}: {row['importance']:.1%}")

# Save model
joblib.dump(model, 'malaria_outbreak_model.pkl')
joblib.dump(feature_cols, 'feature_cols.pkl')

print(f"\n✅ Model saved as 'malaria_outbreak_model.pkl'")

# Test prediction function
def predict_outbreak(temp, rainfall, humidity, month):
    is_rainy = 1 if month in [4,5,6,7,8,9,10,11] else 0
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)
    
    features = np.array([[is_rainy, temp, rainfall, humidity, month_sin, month_cos]])
    prob = model.predict_proba(features)[0][1]
    return prob

print(f"\n🧪 Test prediction for July (rainy month):")
prob = predict_outbreak(28, 150, 80, 7)
print(f"   Outbreak probability: {prob:.1%}")