"""
Professional Data Fetching Script
WHO AFRO Malaria Data - Real-time download
Author: Nathan Aniakwa
Purpose: Fetch real malaria surveillance data for African countries
"""

import requests
import pandas as pd
import os
from datetime import datetime
import json

print("="*70)
print("🌍 WHO AFRO MALARIA DATA FETCHER")
print("="*70)
print(f"🕐 Fetch started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Create data directory
os.makedirs("data", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

# WHO AFRO API endpoints (real data sources)
datasets = {
    "malaria_cases": {
        "url": "https://data.afro.who.int/api/3/action/datastore_search",
        "resource_id": "2928887b-2021-4bcf-927f-7fb1cb542fb2",
        "description": "Confirmed malaria cases by country"
    },
    "suspected_cases": {
        "url": "https://data.afro.who.int/api/3/action/datastore_search",
        "resource_id": "7d6cb833-8520-4a94-a256-5fb939267fab",
        "description": "Number of suspected malaria cases"
    },
    "mortality_rate": {
        "url": "https://data.afro.who.int/api/3/action/package_show",
        "id": "estimated-malaria-mortality-rate-per-100-000-population",
        "description": "Malaria mortality rate per 100,000"
    }
}

def fetch_dataset(name, config):
    """Fetch dataset from WHO AFRO API"""
    print(f"📥 Fetching: {config['description']}...")
    
    try:
        if name == "mortality_rate":
            response = requests.get(config["url"], params={"id": config["id"]})
            return {"status": "metadata", "data": response.json()}
        else:
            params = {
                "resource_id": config["resource_id"],
                "limit": 5000
            }
            response = requests.get(config["url"], params=params)
            data = response.json()
            
            if "result" in data and "records" in data["result"]:
                df = pd.DataFrame(data["result"]["records"])
                filename = f"data/{name}.csv"
                df.to_csv(filename, index=False)
                print(f"   ✅ Saved {len(df)} records to {filename}")
                return {"status": "success", "data": df, "filename": filename}
            else:
                print(f"   ⚠️ No records found")
                return {"status": "empty", "data": None}
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {"status": "error", "error": str(e)}

# Fetch all datasets
results = {}
for name, config in datasets.items():
    results[name] = fetch_dataset(name, config)

print()
print("="*70)
print("📊 DATA FETCHING COMPLETE")
print("="*70)

# Create a summary report
summary = {
    "fetch_date": datetime.now().isoformat(),
    "datasets": {}
}

for name, result in results.items():
    if result["status"] == "success":
        summary["datasets"][name] = {
            "status": "success",
            "records": len(result["data"]),
            "file": result["filename"]
        }
    else:
        summary["datasets"][name] = {"status": result["status"]}

# Save summary
with open("data/fetch_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n📁 Files saved in /data/ folder:")
for f in os.listdir("data"):
    print(f"   📄 {f}")

print(f"\n✅ Fetch completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")