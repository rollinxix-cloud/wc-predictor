import json
import os

print("=== P.E.S MATCHES PLAYER ENTRY ===")
name = input("👉 Enter Participant Name: ").strip()
pick1 = input("👉 Enter Finalist 1: ").strip()
pick2 = input("👉 Enter Finalist 2: ").strip()

if not name or not pick1 or not pick2:
    print("❌ Error: Fields cannot be blank.")
    exit()

file_name = "participants.json"
try:
    with open(file_name, "r") as f:
        data = json.load(f)
except Exception:
    data = []

ticket_num = str(len(data) + 1).zfill(3)

new_entry = {
    "ticket": ticket_num,
    "name": name,
    "pick1": pick1,
    "pick2": pick2,
    "status": "Verified"
}
data.append(new_entry)

with open(file_name, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n✅ Saved {name} locally (Ticket #{ticket_num})!")

print("🚀 Pushing updates to live GitHub Pages dashboard...")
os.system("git add participants.json")
os.system(f'git commit -m "Added entry for {name}"')
os.system("git push origin main")
print("\n✨ Process finished.")