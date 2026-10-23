import csv
import os
import re
import argparse

def apply_translated_text(translations_filename):
    with open(translations_filename, "r", encoding="utf-8-sig") as csv_in, open("translations_temp.csv", "w+", encoding="utf-8-sig") as csv_file:
        # Weird CSV quirk: newlines just don't work correctly in CSV
        # So they are replaced with \\n, and then swapped back 
        for line in csv_in.readlines():
            csv_file.write(line.replace("\\n", "\\\\n").replace("\\ n", "\\\\n"))
        csv_file.seek(0)
        # Preserve newlines
        dialect = csv.Sniffer().sniff(csv_file.read(1024))
        dialect.escapechar = '\\'
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file, dialect=dialect)
        header = next(csv_reader) # Just ignore the header
        for line in csv_reader:
            print(line)
            filepath, key, chinese, english = line

            # Don't write empty localization entries
            if english == "":
                continue

            # Fix \n, and escape all quotes that aren't already escaped
            english_quote_escape = re.sub(r"(?<!\\)\"", "\\\"", english).replace("\\\\n", "\\n")

            with open(filepath, "a", encoding="utf-8-sig") as file:
                file.write(f"\n  {key}: \"{english_quote_escape}\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append translated text to mod files")
    parser.add_argument("-i", "--input", help="CSV-formatted as filepath,key,chinese,english")
    # Basepath is usually C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 for a default Steam install
    parser.add_argument("-b", "--basepath", help="Base path of the mod; defaults to current directory", default=".")
    args = parser.parse_args()

    os.chdir(args.basepath)

    apply_translated_text(args.input)
