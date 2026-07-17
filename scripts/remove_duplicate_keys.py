import os
import re
import argparse

def remove_duplicate_keys(file_path, dry_run=False):
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a file.")
        return

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    seen_keys = set()
    new_lines = []
    removed_keys = []

    # Regex to match Paradox localization keys:   key:0 "value" or   key: "value"
    # It looks for lines starting with whitespace, followed by a key name, then : or :[0-9]
    key_pattern = re.compile(r'^(\s+)([a-zA-Z0-9_\.\-]+):[0-9]?\s+.*')

    for line in lines:
        match = key_pattern.match(line)
        if match:
            key = match.group(2)
            if key in seen_keys:
                removed_keys.append((key, line.strip()))
                continue
            else:
                seen_keys.add(key)
                new_lines.append(line)
        else:
            new_lines.append(line)

    if removed_keys:
        print(f"Processing {file_path}:")
        for key, content in removed_keys:
            print(f"  Removed duplicate key: '{key}' -> {content}")
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                f.writelines(new_lines)
            print(f"  Updated {file_path} (removed {len(removed_keys)} duplicates).")
    else:
        if not dry_run:
            # Check if file needs rewriting anyway (e.g. encoding issues, though utf-8-sig should be safe)
            pass

def main():
    parser = argparse.ArgumentParser(description="Find and remove duplicate keys in Stellaris YAML localization files.")
    parser.add_argument("path", help="Path to a file or directory to process.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be removed without modifying files.")
    args = parser.parse_args()

    target_path = args.path
    if os.path.isfile(target_path):
        remove_duplicate_keys(target_path, args.dry_run)
    elif os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.endswith(".yml"):
                    file_path = os.path.join(root, file)
                    remove_duplicate_keys(file_path, args.dry_run)
    else:
        print(f"Error: {target_path} not found.")

if __name__ == "__main__":
    main()
