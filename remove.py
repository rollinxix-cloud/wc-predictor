import json
import os

FILE_NAME = "participants.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        print(f"❌ Error: {FILE_NAME} not found!")
        return None
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("❌ Error: JSON file is corrupted or empty.")
        return None

def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print("✅ participants.json updated successfully!")

def remove_participant():
    data = load_data()
    if data is None:
        return

    if not data:
        print("📂 The ledger is currently empty. Nothing to remove!")
        return

    # Display current participants quickly for reference
    print("\n--- Current Active Ledger ---")
    for p in data:
        print(f"🎫 Ticket #{p.get('ticket')}: {p.get('name')} ({p.get('pick1')} vs {p.get('pick2')})")
    print("-----------------------------\n")

    ticket_to_remove = input("Enter the Ticket Number to remove (e.g., 01): ").strip()

    # Find the target entry
    target = None
    for item in data:
        if str(item.get("ticket")).zfill(2) == ticket_to_remove.zfill(2):
            target = item
            break

    if target:
        print(f"\n⚠️ Found Entry: {target['name']} (Ticket #{target['ticket']})")
        confirm = input(f"Are you sure you want to permanently delete this entry? (y/n): ").lower()
        
        if confirm == 'y':
            data.remove(target)
            save_data(data)
            print("🚀 Done! Don't forget to commit and push your changes to GitHub.")
        else:
            print("❌ Operation cancelled.")
    else:
        print(f"❓ No entry found matching Ticket #{ticket_to_remove}")

if __name__ == "__main__":
    remove_participant()