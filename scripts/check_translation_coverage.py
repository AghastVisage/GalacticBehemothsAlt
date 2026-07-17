#!/usr/bin/env python3
import os
import re
import json
import argparse
import subprocess


def get_keys_and_values_from_file(file_path):
    """
    Extracts localization keys and their values from a YAML file.
    Assumes standard Paradox localization format:
     key: "value"
     key:0 "value"
    Returns a dictionary {key: value}
    """
    data = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Check for key: "value" or key:0 "value" pattern
                if ':' in line:
                    parts = line.split(':', 1)
                    key_part = parts[0].strip()
                    value_part = parts[1].strip()
                    
                    # Basic validation
                    if key_part and not key_part.startswith('l_') and not key_part.startswith(' '):
                         # Extract value content - remove quotes if present
                         # Paradox files usually have quotes, but sometimes might not or might have comments after
                         # Simple extraction: take everything after first quote and before last quote
                         value = value_part
                         ignore_index_match = re.search(r'^\d+\s+"', value)
                         if ignore_index_match:
                             value = value[ignore_index_match.end()-1:]
                         elif value.startswith('"'):
                             pass # Normal case
                         elif re.match(r'^\d+\s+', value):
                             # Case like: key:0 "value"
                             match = re.search(r'^\d+\s+(.*)', value)
                             if match:
                                 value = match.group(1)

                         if value.startswith('"') and value.endswith('"'):
                             value = value[1:-1]
                         
                         data[key_part] = value
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return data

def get_changed_keys(commit_hash, cn_dir):
    """
    Returns a set of keys that have changed in the Chinese directory since the given commit.
    Ignores whitespace changes.
    """
    changed_keys = set()
    try:
        # Get list of changed files
        cmd = ["git", "diff", "--name-only", commit_hash, "HEAD", cn_dir]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        changed_files = [f for f in result.stdout.splitlines() if f.strip()]
        
        for file_path in changed_files:
            if not file_path.endswith('.yml'):
                continue
            
            # Get changes for this file, ignoring whitespace
            # -U0 avoids context lines, making parsing easier
            cmd_diff = ["git", "diff", "-w", "-U0", commit_hash, "HEAD", file_path]
            diff_result = subprocess.run(cmd_diff, capture_output=True, text=True)
            
            if diff_result.returncode != 0:
                print(f"Warning: Could not diff file {file_path}")
                continue

            for line in diff_result.stdout.splitlines():
                if line.startswith('+') and not line.startswith('+++'):
                    # This is an added/modified line
                    content = line[1:].strip()
                    if ':' in content and not content.startswith('#'):
                        parts = content.split(':', 1)
                        key = parts[0].strip()
                        # Basic validity check (matches logic in extracting keys)
                        if key and not key.startswith('l_'):
                            changed_keys.add(key)
                            
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
    except Exception as e:
        print(f"Error processing git changes: {e}")
        
    return changed_keys


def main():
    parser = argparse.ArgumentParser(description="Check translation coverage.")
    parser.add_argument("-o", "--output", help="Output file path for missing translations in JSON format.")
    parser.add_argument("-c", "--commit", help="Git commit hash to compare against for finding outdated translations.")
    args = parser.parse_args()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loc_dir = os.path.join(repo_root, "localisation")
    cn_dir = os.path.join(loc_dir, "simp_chinese")
    en_dir = os.path.join(loc_dir, "english")

    if not os.path.exists(cn_dir):
        print(f"Error: Chinese localization directory not found at {cn_dir}")
        return

    # Map Chinese keys to (file_path, original_text)
    cn_keys_map = {} # key -> {'file': file_path, 'original': text}
    
    # Map English keys
    en_keys = set()

    # Get changed keys if commit hash is provided
    changed_keys = set()
    if args.commit:
        print(f"Calculating changes since commit {args.commit}...")
        changed_keys = get_changed_keys(args.commit, cn_dir)
        print(f"Found {len(changed_keys)} changed/new keys.")


    print(f"Scanning Chinese files in {cn_dir}...")
    for root, dirs, files in os.walk(cn_dir):
        for file in files:
            if file.endswith(".yml"):
                file_path = os.path.join(root, file)
                file_data = get_keys_and_values_from_file(file_path)
                rel_path = os.path.relpath(file_path, cn_dir)
                for key, value in file_data.items():
                    cn_keys_map[key] = {'file': rel_path, 'original': value}

    print(f"Scanning English files in {en_dir}...")
    if os.path.exists(en_dir):
        for root, dirs, files in os.walk(en_dir):
            for file in files:
                if file.endswith(".yml"):
                    file_path = os.path.join(root, file)
                    # We only care about keys existence here
                    en_keys.update(get_keys_and_values_from_file(file_path).keys())
    else:
        print(f"Warning: English localization directory not found at {en_dir}")

    total_cn_keys = len(cn_keys_map)

    missing_items = []
    
    # Track statistics
    stats = {
        'missing': 0,
        'outdated': 0,
        'empty': 0
    }

    for key, info in cn_keys_map.items():
        original_text = info['original']
        # Check if original text is empty or just whitespace
        if not original_text or original_text.strip() == "":
            print(f"Warning: Key '{key}' in {info['file']} has empty original text.")
            missing_items.append({
                "file": info['file'],
                "key": key,
                "original": original_text,
                "status": "empty"
            })
            stats['empty'] += 1
            continue

        if key not in en_keys:
            missing_items.append({
                "file": info['file'],
                "key": key,
                "original": info['original'],
                "status": "missing"
            })
            stats['missing'] += 1
        elif key in changed_keys:
            missing_items.append({
                "file": info['file'],
                "key": key,
                "original": info['original'],
                "status": "outdated"
            })
            stats['outdated'] += 1

    total_eligible_keys = total_cn_keys - stats['empty']
    coverage = 0
    if total_eligible_keys > 0:
        coverage = (total_eligible_keys - stats['missing']) / total_eligible_keys * 100
    total_issues = len(missing_items)

    print("\n" + "="*50)
    print("Translation Coverage Report")
    print("="*50)
    print(f"Total Chinese Keys: {total_cn_keys}")
    print(f"Keys with Empty Original: {stats['empty']} (excluded from coverage)")
    print(f"Total Eligible for Translation: {total_eligible_keys}")
    print(f"Total English Keys: {len(en_keys)}")
    print(f"Missing Translations: {stats['missing']}")
    if args.commit:
        print(f"Outdated Translations: {stats['outdated']}")
    print(f"Coverage (ignoring outdated/empty): {coverage:.2f}%")
    print("="*50)

    if total_issues > 0:
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(missing_items, f, ensure_ascii=False, indent=4)
                print(f"\nReport written to {args.output}")
            except Exception as e:
                print(f"\nError writing to output file: {e}")
        else:
            # Group by file and status
            items_by_file = {}
            for item in missing_items:
                fpath = item['file']
                if fpath not in items_by_file:
                    items_by_file[fpath] = []
                items_by_file[fpath].append(item)
            
            print("\nIssues found (grouped by source file):")
            for file in sorted(items_by_file.keys()):
                print(f"\n{file}:")
                for item in sorted(items_by_file[file], key=lambda x: x['key']):
                    status_tag = f"[{item['status'].upper()}]"
                    print(f"  - {status_tag} {item['key']}")

if __name__ == "__main__":
    main()
