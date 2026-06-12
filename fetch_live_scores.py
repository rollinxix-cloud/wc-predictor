import os
import json
import requests
from datetime import datetime

# 1. Secure API Token Handling
# Reads from GitHub Secrets in the cloud. If local, it uses your string below.
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "145b9cfa09674828ae129543762dd921")

URL = "https://api.football-data.org/v4/competitions/WC/matches"
HEADERS = {"X-Auth-Token": API_KEY}

def sync_world_cup_data():
    try:
        print("Connecting to football-data.org live match vectors...")
        response = requests.get(URL, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ API Connection Failed! Status code: {response.status_code}")
            print(f"Response log: {response.text}")
            return

        data = response.json()
        raw_matches = data.get("matches", [])
        processed_fixtures = []

        print(f"Parsing {len(raw_matches)} tournament matches...")

        for match in raw_matches:
            # Extract country profile parameters
            home_team = match.get("homeTeam", {}).get("name", "TBD")
            away_team = match.get("awayTeam", {}).get("name", "TBD")

            # Extract full-time results structures
            score_node = match.get("score", {}).get("fullTime", {})
            home_score = score_node.get("home")
            away_score = score_node.get("away")

            # Standardize match state codes for your custom HTML status engines
            api_status = match.get("status", "").upper()
            if api_status == "FINISHED":
                status_label = "Finished"
                time_marker = "FT"
            elif api_status in ["IN_PLAY", "PAUSED", "LIVE"]:
                status_label = "Live"
                time_marker = "Live"
            else:
                status_label = "Scheduled"
                # Transform API ISO timestamps to standard clock timelines (HH:MM)
                try:
                    utc_string = match.get("utcDate", "")
                    parsed_time = datetime.strptime(utc_string, "%Y-%m-%dT%H:%M:%SZ")
                    time_marker = parsed_time.strftime("%H:%M")
                except Exception:
                    time_marker = "00:00"

            processed_fixtures.append({
                "team1": home_team,
                "score1": home_score if home_score is not None else "-",
                "team2": away_team,
                "score2": away_score if away_score is not None else "-",
                "status": status_label,
                "time": time_marker
            })

        # Encapsulate back into the structural core array required by bracket.html
        compiled_output = {"matches": processed_fixtures}

        with open("worldcup.json", "w", encoding="utf-8") as data_file:
            json.dump(compiled_output, data_file, indent=2, ensure_ascii=False)

        print("🏆 Sync complete! worldcup.json updated successfully.")

    except Exception as error:
        print(f"💥 Critical script execution runtime fault: {error}")

if __name__ == "__main__":
    sync_world_cup_data()