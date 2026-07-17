import subprocess
import re
import sys

def get_staged_files():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', 'localisation/english'],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout.splitlines()

def get_staged_content(filename):
    result = subprocess.run(
        ['git', 'show', f':{filename}'],
        stdout=subprocess.PIPE,
        text=True
    )
    return result.stdout

def check_quotes():
    files = get_staged_files()
    pattern_key = re.compile(r'^\s*([a-zA-Z0-9_\.]+):\d*\s*')
    pattern_valid = re.compile(r'^\s*([a-zA-Z0-9_\.]+):\d*\s*"(.*)"\s*(#.*)?$')
    
    found_issues = False
    
    for filename in files:
        if not filename.endswith('.yml'):
            continue
            
        content = get_staged_content(filename)
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # precise check for comments
            if line.strip().startswith('#') or line.strip() == 'l_english:': 
                continue

            if pattern_key.match(line):
                if not pattern_valid.match(line):
                    print(f"Potential issue in {filename}:{i+1}")
                    print(f"Line: {line}")
                    found_issues = True

    if not found_issues:
        print("No obvious quote issues found.")

if __name__ == '__main__':
    check_quotes()
