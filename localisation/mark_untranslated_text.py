import os
import argparse

def read_translation_item(line):
    # Skip empty lines and whole-line comments
    if len(line.strip()) == 0 or line.strip()[0] == "#":
        return None, None

    split = line.strip().split(":", 1)
    if len(split) < 2:
        return None, None
    key = split[0].strip()
    value = split[1].strip()
    if key == "l_english" or key == "l_simp_chinese":
        return None, None

    # Strip out localization comment integer
    if len(value) > 0 and value[0].isdigit():
        value = value[1:]


    if value[0] != "\"":
        value = "\"" + value
    if value[-1] != "\"":
        value = value + "\""

    return key, value

def mark_untranslated_text(untranslated_filename):
    with open(untranslated_filename, "w", encoding="utf-8-sig") as out_csv:
        out_csv.write("filepath,key,chinese,english\n")

        for root, dirs, files in os.walk(os.path.join("localisation", "simp_chinese")):
            for file in files:
                if file.split(".")[-1] == "yml":
                    filepath = os.path.join(root, file)
                    # Derive English localization path by replacing the folder name, then replacing the end of the file name
                    english_filepath = filepath.replace("simp_chinese", "english", 1).replace("simp_chinese.yml", "english.yml", 1)

                    # Create stub English translation files, if they are missing
                    if not os.path.exists(english_filepath):
                        print("missing localization file:", english_filepath)
                        os.makedirs(os.path.dirname(english_filepath), exist_ok=True)
                        with open(english_filepath, "w") as english_file:
                            english_file.write("l_english:\n")

                    # Step 1: Read from the English localization, and find out what we have
                    english_has_items = {}
                    with open(english_filepath, "r", encoding="utf-8-sig") as english_file:
                        print(english_filepath)
                        english_text = english_file.readlines()[1:]
                        for line in english_text:
                            if len(line.strip()) == 0 or line.strip()[0] == "#":
                                continue
                            key, value = read_translation_item(line)
                            if key is None or value == "": # Also mark empty lines as missing
                                continue
                            english_has_items[key] = value

                    # Step 2: Read from the Chinese localization, and record every item that is missing from the English localization
                    with open(filepath, "r", encoding="utf-8-sig") as chinese_file:
                        chinese_text = chinese_file.readlines()[1:]
                        for line in chinese_text:
                            key, value = read_translation_item(line)
                            if key is None:
                                continue
                            if not key in english_has_items:
                                out_csv.write(f"{english_filepath.replace("\\", "/")},{key},{value.replace("\\n", "\\\\n")},\"\"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record missing translations into CSV, and create stub translation files for whole files that are missing.")
    parser.add_argument("-o", "--output", help="Output location of CSV-formatted file as filepath,key,chinese,english")
    # Basepath is usually C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 for a default Steam install
    parser.add_argument("-b", "--basepath", help="Base path of the mod; defaults to current directory", default=".")
    args = parser.parse_args()

    os.chdir(args.basepath)

    mark_untranslated_text(args.output)