import json
import os
import re
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.error import YAMLError

from ruamel.yaml.scalarstring import DoubleQuotedScalarString

# Configure YAML
yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.width = 4096  # Prevent wrapping

BASE_DIR = Path(__file__).parent.parent
SOURCE_BASE = BASE_DIR / "localisation" / "simp_chinese"
TARGET_BASE = BASE_DIR / "localisation" / "english"
TRANSLATIONS_FILE = BASE_DIR / "scripts" / "missing_translations_translated.json"

def clean_yaml_content(content):
    # Remove :0 which makes YAML invalid for ruamel
    pattern = re.compile(r"^(\s*[^#\s:][^:]*):0\s+", re.MULTILINE)
    content = pattern.sub(r"\1: ", content)
    
    # Fix unindented comments
    content = re.sub(r"^#", r"  #", content, flags=re.MULTILINE)
    
    # Deduplicate adjacent identical comment lines (handling different possible indentations)
    # This handles both 0 and 2 space indents due to the ^# ->   # fix above
    content = re.sub(r"(\s*#.*\n)\1+", r"\1", content)
    
    return content

def apply_translations():
    with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    # Group by file
    files_data = {}
    for item in translations:
        file_path = item['file']
        if file_path not in files_data:
            files_data[file_path] = []
        files_data[file_path].append(item)

    for relative_path, items in files_data.items():
        # Determine target file path
        target_relative_path = relative_path.replace('l_simp_chinese', 'l_english')
        target_full_path = TARGET_BASE / target_relative_path
        
        print(f"Processing {target_full_path}...")
        
        # Ensure directory exists
        target_full_path.parent.mkdir(parents=True, exist_ok=True)
        
        raw_content = ""
        data = None
        file_existed = target_full_path.exists()
        
        if file_existed:
            try:
                with open(target_full_path, 'r', encoding='utf-8-sig') as f:
                    raw_content = f.read()
                
                if not raw_content.strip():
                    data = CommentedMap()
                    data["l_english"] = CommentedMap()
                else:
                    clean_content = clean_yaml_content(raw_content)
                    data = yaml.load(clean_content)
            except Exception as e:
                print(f"CRITICAL ERROR: Failed to load {target_full_path}: {e}")
                continue

        if data is None:
            if file_existed:
                 print(f"CRITICAL ERROR: Loaded data is None for {target_full_path}. SKIPPING.")
                 continue
            else:
                data = CommentedMap()
                data["l_english"] = CommentedMap()
        
        english_block = data.get("l_english")
        if english_block is None:
             english_block = CommentedMap()
             data["l_english"] = english_block

        processed_keys = set()
        for item in items:
            key = item['key']
            original = item['original']
            translation = item['translation']
            
            if key == "l_simp_chinese" or key in processed_keys: 
                continue
            processed_keys.add(key)

            new_val = DoubleQuotedScalarString(translation)
            
            # Simple skip check: value is same AND comment is already in the raw content
            # (Rough check for comment in raw content is usually enough since we cleansed it)
            if key in english_block and english_block[key] == new_val:
                # Check for comment in raw content (more reliable than ruamel for skipping)
                if f"# {original}" in raw_content or f"#{original}" in raw_content:
                    continue

            # Update value
            english_block[key] = new_val
            
            # Clean up existing comments for this key in ruamel to avoid growing
            if key in english_block.ca.items:
                del english_block.ca.items[key]

            # Add comment
            comment_text = f" {original}"
            english_block.yaml_set_comment_before_after_key(key, before=comment_text)

        # Save the file
        try:
            # Write with utf-8-sig to preserve usage of BOM if it was there (or forcing it)
            # Actually standard utf-8 is better but if we want to be consistent with read:
            # If we read with sig, we might want to write with sig.
            # But ruamel.yaml might handle BOM on load but dump usually doesn't add it unless we write \ufeff
            # Let's just use utf-8. If Paradox needs BOM, we might need to add it explicitly. 
            # Most Paradox games operate fine with UTF-8 w/o BOM (newer ones), but some prefer BOM.
            # Localisation files usually HAVE BOM.
            # So I will use utf-8-sig for writing too.
            
            with open(target_full_path, 'w', encoding='utf-8-sig') as f:
                yaml.dump(data, f)
            print(f"Saved {target_full_path}")
        except Exception as e:
            print(f"Error saving {target_full_path}: {e}")

if __name__ == "__main__":
    apply_translations()
