import json
import os
import re

# Glossary of terms for consistency
GLOSSARY = {
    "巨娘": "Giantess",
    "小人": "Tiny person",
    "艦娘": "Shipgirl",
    "胖次": "Panties",
    "汗液": "Sweat",
    "爱液": "Love fluid",
    "消化液": "Digestive fluid",
    "缩小": "Shrink",
    "精炼": "Refining",
    "体验": "Experience",
    "核心元件": "Core component",
    "Bruh系列": "Bruh Series",
    "希诺": "Xino",
}

def apply_glossary(text):
    for cn, en in GLOSSARY.items():
        text = text.replace(cn, en)
    return text

def translate_text(text):
    # This is a placeholder for actual translation logic.
    # In a real scenario, this could call an LLM API.
    # For now, we apply the glossary and basic formatting.
    translated = apply_glossary(text)
    
    # Simple heuristic to handle Paradox formatting if necessary
    # Example: If it starts with §Y and ends with §!, ensure it's preserved
    return translated

def main():
    source_file = 'scripts/missing_translations.json'
    output_file = 'scripts/missing_translations_translated.json'
    
    if not os.path.exists(source_file):
        print(f"Source file {source_file} not found.")
        return

    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for entry in data:
        original = entry.get('original', '')
        if original and entry.get('status') != 'empty':
            # Check if it's already translated (if we were appending, but we replace)
            translation = translate_text(original)
            results.append({
                "file": entry['file'],
                "key": entry['key'],
                "original": original,
                "translation": translation
            })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print(f"Translated {len(results)} entries to {output_file}")

if __name__ == "__main__":
    main()
