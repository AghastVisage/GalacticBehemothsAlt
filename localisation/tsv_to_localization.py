import os
import argparse
import re

def read_translation_item(line):
    # Skip empty lines and whole-line comments
    if len(line.strip()) == 0 or line.strip()[0] == "#":
        return None, None

    split = line.strip().replace("\t", "").split(":", 1)
    if len(split) < 2:
        return None, None
    key = split[0].strip()
    value = split[1].strip()
    if key == "l_english" or key == "l_simp_chinese":
        return None, None

    # Strip out localization comment integer
    if len(value) > 0 and value[0].isdigit():
        value = value[2:].strip()

    # Remove beginning and end quotes
    if value[0] == "\"":
        value = value[1:]
    if value[-1] == "\"":
        value = value[:1]
    #value = re.sub(r"(?<!\\)\"", "\\\"", value)

    return key, value

def mark_untranslated_text(translations_filename):
    trans_entries = {}
    with open(translations_filename, "r", encoding="utf-8-sig") as in_tsv:
        for line in in_tsv.readlines():
            path, key, chinese, english = line.split("\t")
            trans_entries[f"{path}\t{key}"] = {"chinese": chinese, "english": english}

        for root, dirs, files in os.walk(os.path.join("localisation", "simp_chinese")):
            for file in files:
                if file.split(".")[-1] == "yml":
                    filepath = os.path.join(root, file)
                    # Derive English localization path by replacing the folder name, then replacing the end of the file name
                    english_filepath = filepath.replace("simp_chinese", "english_temp", 1).replace("simp_chinese.yml", "english.yml", 1)

                    # Create stub English translation files
                    if not os.path.exists(english_filepath):
                        os.makedirs(os.path.dirname(english_filepath), exist_ok=True)

                    # For each key in the Chinese localiztion file, write into the english file
                    with open(filepath, "r", encoding="utf-8-sig") as chinese_file, open(english_filepath, "w") as english_file:
                        english_file.write("l_english:\n")
                        chinese_text = chinese_file.readlines()[1:]
                        for line in chinese_text:
                            key, value = read_translation_item(line)
                            if key is None:
                                continue
                            english_file.write(f"# {chinese_text}\n")
                            english_file.write(f"{key}: \"{trans_entries[f"{filepath}\t{key}"]}\"\n")
                            english_file.write(f"\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write all translations into localization files, keeping the structure of the CN file")
    parser.add_argument("-i", "--translations", help="Input location of TSV-formatted file as filepath   key chinese english", required=True)
    # Basepath is usually C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 for a default Steam install
    parser.add_argument("-b", "--basepath", help="Base path of the mod; defaults to current directory", default=".")
    args = parser.parse_args()

    os.chdir(args.basepath)

    mark_untranslated_text(args.translation)