import os

# If the glossary term wasn't already translated, the script would not be able to pick up on it - they are defined manually here
glossary = {
    "三月希瞳": "Hitomi Mitsuki",
    "小橘子长": "Mora",
    "宁古塔": "Ningguta",
    "寒岭": "Hanling",
    "鸟音山水": "Qinwen",
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
    "秦雯": "Qinwen",
    "小柠": "Little Kaining",
    "海柠": "Kaining",
    "布洛妮娅": "Veliona",
    "白希": "White Seele",
    "白丝": "white silk stockings"
}

def read_translation_item(line):
    # Skip empty lines and whole-line comments
    if len(line.strip()) == 0 or line.strip()[0] == "#":
        return None, None

    split = line.strip().split(":", 1)
    if len(split) < 2:
        return None, None
    key = split[0].strip()
    value = split[1].strip()

    # Strip out localization comment integer
    if len(value) > 0 and value[0].isdigit():
        value = value[1:]

    return key, value

out_csv = open("glossary.csv", "w", encoding="utf-8-sig")
for key, value in glossary.items():
    out_csv.write(f"{key},{value},ZH,EN\n")
# Headers: Chinese text, English text, ZH, EN

for root, dirs, files in os.walk(os.path.join("localisation", "simp_chinese")):
    for file in files:
        if file.split(".")[-1] == "yml":
            filepath = os.path.join(root, file)
            # Derive English localization path by replacing the folder name, then replacing the end of the file name
            english_filepath = filepath.replace("simp_chinese", "english", 1).replace("simp_chinese.yml", "english.yml", 1)

            # Skip missing English localization files
            if not os.path.exists(english_filepath):
                continue

            # Step 1: Read from the English localization, and find out what we have
            english_names = {}
            with open(english_filepath, "r", encoding="utf-8-sig") as english_file:
                english_text = english_file.readlines()[1:]
                for line in english_text:
                    if len(line.strip()) == 0 or line.strip()[0] == "#":
                        continue
                    key, value = read_translation_item(line)
                    if key is None or not key.startswith("NAME_"): # Also mark empty lines as missing
                        continue
                    print(key)
                    english_names[key] = value

            # Step 2: Read from the Chinese localization, and record every item that is missing from the English localization
            with open(filepath, "r", encoding="utf-8-sig") as chinese_file:
                chinese_text = chinese_file.readlines()[1:]
                for line in chinese_text:
                    key, value = read_translation_item(line)
                    if key is None or not key.startswith("NAME_"):
                        continue
                    if key in english_names:
                        out_csv.write(f"{value},{english_names[key]},ZH,EN\n")

out_csv.close()