import os
import csv
import re
import argparse

def translate_text(untranslated_filename, translated_filename, translator, deepl_key):
    billable_characters_count = 0
    if translator == "argos":
        import argostranslate.package
        import argostranslate.translate
        # Offline translator. Completely inadequate, but at least it produces latin characters
        from_code = "zh"
        to_code = "en"
        # Download and install Argos Translate package
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())
    elif translator == "deepl":
        # Deepl translator, actually good, but you need an API key
        import deepl
        from_code = "ZH"
        to_code = "EN-US"
        deepl_client = deepl.DeepLClient(deepl_key)
        glossary=deepl_client.list_multilingual_glossaries()[0]
    else: # None translator, just copy Chinese text to English text field for testing
        pass

    phrase_to_key = {}
    with open(untranslated_filename, "r", encoding="utf-8-sig") as csv_file, open(translated_filename, "w", encoding="utf-8-sig") as out_file:
        dialect = csv.Sniffer().sniff(csv_file.read(1024))
        csv_file.seek(0)
        dialect.escapechar = '\\'
        csv_reader = csv.reader(csv_file, dialect=dialect)
        out_file.write("filepath,key,chinese,english\n")
        header = next(csv_reader)
        for line in csv_reader:
            filepath, key, chinese, english = line
            print(line)
            if english != "":
                raise Exception()
            phrase_to_key.setdefault(chinese, []).append((filepath, key))
        print(f"Done counting, got {len(phrase_to_key)} phrases")

        for phrase, keys in phrase_to_key.items():
            if phrase == "":
                english_phrase_quote_escape = ""
                phrase_quote_escape = ""
            else:
                if translator == "argos":
                    english_phrase = argostranslate.translate.translate(phrase, from_code, to_code)
                elif translator == "deepl":
                    text_result = deepl_client.translate_text(phrase, source_lang=from_code, target_lang=to_code, glossary=glossary)
                    english_phrase = text_result.text
                    billable_characters_count += text_result.billed_characters
                    print("Billed characters:",billable_characters_count)
                else:
                    english_phrase = phrase
                english_phrase_quote_escape = re.sub(r"(?<!\\)\"", "\\\"", english_phrase)
                phrase_quote_escape = re.sub(r"(?<!\\)\"", "\\\"", phrase)
            for filepath, key in keys:
                print(key)
                out_file.write(f"{filepath},{key},\"{phrase_quote_escape}\",\"{english_phrase_quote_escape}\"\n")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append translated text to mod files")
    parser.add_argument("-i", "--input", help="Untranslated CSV-formatted as filepath,key,chinese,english", required=True)
    parser.add_argument("-o", "--output", help="Output CSV-formatted as filepath,key,chinese,english", required=True)
    parser.add_argument("-d", "--deepl-key", help="Path to file containing deepl key", default="")
    parser.add_argument("-t", "--type", help="Which translation implementation to use", choices=["deepl", "argos", "none"], default="none")
    # Basepath is usually C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 for a default Steam install
    parser.add_argument("-b", "--basepath", help="Base path of the mod; defaults to current directory", default=".")
    args = parser.parse_args()

    os.chdir(args.basepath)

    deepl_key = ""
    with open(args.deepl_key, "r") as f:
        for line in f.readlines():
            deepl_key = line
            break

    translate_text(args.input, args.output, args.type, deepl_key)