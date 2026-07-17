import json
import os
import sys

def append_translations(file_path, new_entries):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    # Avoid duplicates by key
    existing_keys = {item['key'] for item in data}
    for entry in new_entries:
        if entry['key'] not in existing_keys:
            data.append(entry)
        else:
            # Update existing if needed
            for i, item in enumerate(data):
                if item['key'] == entry['key']:
                    data[i] = entry
                    break

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python append_translations.py <target_json> <new_entries_json_file>")
        sys.exit(1)
    
    target_path = sys.argv[1]
    new_entries_file = sys.argv[2]
    try:
        with open(new_entries_file, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        append_translations(target_path, entries)
        print(f"Successfully appended {len(entries)} entries from {new_entries_file}.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
