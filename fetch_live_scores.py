import os
import json
import requests

# Secure API Token Handling
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "145b9cfa09674828ae129543762dd921")
URL = "https://api.football-data.org/v4/competitions/WC/matches"
HEADERS = {"X-Auth-Token": API_KEY}

def sync_world_cup_data():
    try:
        print("Connecting to football-data.org live match vectors...")
        response = requests.get(URL, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ API Connection Failed! Status code: {response.status_code}")
            return

        data = response.json()
        raw_matches = data.get("matches", [])
        processed_fixtures = []

        print(f"Parsing {len(raw_matches)} matches into template-ready native structures...")

        for match in raw_matches:
            # Reconstruct the exact object architecture bracket.html expects
            reconstructed_match = {
                "status": match.get("status"),              # Keeps 'TIMED', 'IN_PLAY', 'FINISHED'
                "stage": match.get("stage"),                # Keeps 'GROUP_STAGE', etc.
                "group": match.get("group"),                # Keeps 'GROUP_A', 'GROUP_B', etc.
                "homeTeam": {
                    "name": match.get("homeTeam", {}).get("name", "TBD")
                },
                "awayTeam": {
                    "name": match.get("awayTeam", {}).get("name", "TBD")
                },
                "score": {
                    "fullTime": {
                        "home": match.get("score", {}).get("fullTime", {}).get("home"),
                        "away": match.get("score", {}).get("fullTime", {}).get("away")
                    }
                }
            }
            processed_fixtures.append(reconstructed_match)

        # Output the structural core required by loadCachedWorldCupData()
        compiled_output = {"matches": processed_fixtures}

        with open("worldcup.json", "w", encoding="utf-8") as data_file:
            json.dump(compiled_output, data_file, indent=2, ensure_ascii=False)

        print("🏆 Sync complete! worldcup.json structure realigned perfectly.")

    except Exception as error:
        print(f"💥 Critical script execution fault: {error}")

if __name__ == "__main__":
    sync_world_cup_data()