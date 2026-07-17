import subprocess
import re
import sys
import os

def get_staged_files():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', 'localisation/english'],
        stdout=subprocess.PIPE,
        text=True
    )
    return [f for f in result.stdout.splitlines() if f.endswith('.yml')]

def fix_line(line):
    # Regex for key: value (no quotes, no version number 0)
    # Group 1: indent + key + colon + space
    # Group 2: value (capture until end or #)
    # Group 3: optional comment
    
    # Ignore l_english:
    if line.strip() == 'l_english:' or line.strip().startswith('#'):
        return line
    
    # Check for key: value (unquoted)
    # Matches:   key: value text
    # Excludes:  key: "value"
    # Excludes:  key: 'value'
    # Excludes:  key: 0 "value"
    # Excludes:  key:0 "value"
    
    match = re.match(r'^(\s*[a-zA-Z0-9_\.]+:)\s+(?!0\s)(?!["\'])(.+?)\s*(#.*)?$', line)
    if match:
        prefix = match.group(1)
        value = match.group(2)
        comment = match.group(3) if match.group(3) else ""
        
        # Escape quotes in value
        value_escaped = value.replace('"', '\\"')
        
        return f'{prefix} "{value_escaped}"{comment}\n'

    # Check for key:0 value (unquoted)
    match_v0 = re.match(r'^(\s*[a-zA-Z0-9_\.]+:)\s*0\s+(?!["\'])(.+?)\s*(#.*)?$', line)
    if match_v0:
        prefix = match_v0.group(1)
        value = match_v0.group(2)
        comment = match_v0.group(3) if match_v0.group(3) else ""
         # Escape quotes in value
        value_escaped = value.replace('"', '\\"')
        
        return f'{prefix}0 "{value_escaped}"{comment}\n'

    return line

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
             with open(filepath, 'r', encoding='utf-8-sig') as f:
                lines = f.readlines()
        except:
            print(f"Failed to read {filepath}")
            return

    new_lines = []
    modified = False
    for line in lines:
        new_line = fix_line(line)
        if new_line != line:
            modified = True
            # print(f"Fixed in {filepath}:\nOld: {line.strip()}\nNew: {new_line.strip()}")
        new_lines.append(new_line)
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Fixed {filepath}")
        # Automatically stage the file again to update the staging area with the fix
        # But user said "fix in staging commit", so usually we assume we modify the files and the user will add them.
        # However, to facilitate the workflow, I'll valid the fixes. 

def main():
    files = get_staged_files()
    print(f"Scanning {len(files)} staged files...")
    for file in files:
        if os.path.exists(file):
            process_file(file)

if __name__ == '__main__':
    main()
