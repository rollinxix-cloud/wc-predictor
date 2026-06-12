import os
import json
import requests

API_URL = "https://api.football-data.org/v4/competitions/WC/matches"
API_TOKEN = os.environ.get("API_TOKEN")

if not API_TOKEN:
    print("❌ Error: API_TOKEN environment variable is missing.")
    exit(1)

headers = {"X-Auth-Token": API_TOKEN}

try:
    print("🛰️ Connecting to football-data.org live stadium feed...")
    response = requests.get(API_URL, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Write data safely into your repository
        with open("worldcup.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("✅ worldcup.json successfully re-compiled with latest real-time scores!")
    else:
        print(f"❌ Sync failure. API Status: {response.status_code}")
        print(response.text)
        exit(1)
        
except Exception as e:
    print(f"❌ System error encountered: {str(e)}")
    exit(1)