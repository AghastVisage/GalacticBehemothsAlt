import os
import argparse

def merge_translation_files(args):
    with open(args.output, "w", encoding="utf-8-sig") as out_tsv, open(args.trans_a, "r", encoding="utf-8-sig") as trans_a, open(args.trans_b, "r", encoding="utf-8-sig") as trans_b, open("diff.log", "w", encoding="utf-8-sig") as log_file:
        # key: path + key
        trans_entries = {}
        for line in trans_a.readlines():
            path, key, chinese, english = line.split("\t")
            trans_entries[f"{path}\t{key}"] = {"chinese": chinese, "english": english}
        for line in trans_b.readlines():
            path, key, chinese, english = line.split("\t")

            if not f"{path}\t{key}" in trans_entries: # If key missing
                log_file.write(f"new key: {path}\t{key} from {chinese} to {english}\n")
                trans_entries[f"{path}\t{key}"] = {"chinese": chinese, "english": english}
            elif trans_entries[f"{path}\t{key}"]["english"] == "": # If english missing - overwrite anyway
                log_file.write(f"new translation: {path}\t{key} from {trans_entries[f"{path}\t{key}"]["chinese"]} to {english}\n")
                trans_entries[f"{path}\t{key}"] = {"chinese": chinese, "english": english}
            elif trans_entries[f"{path}\t{key}"]["chinese"] != chinese: # If chinese updated - update translation too
                log_file.write(f"updated: {path}\t{key} from {trans_entries[f"{path}\t{key}"]["chinese"]} to {chinese} + {english}\n")
                trans_entries[f"{path}\t{key}"] = {"chinese": chinese, "english": english}

        for key, entry in trans_entries.items():
            out_tsv.write(f"{key}\t{entry["chinese"]}\t{entry["english"]}")


        
        pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge 2 translation files, filling in keys that are missing")
    parser.add_argument("-a", "--trans-a", help="Priority translation file; if a translation exists here, it will be used first.", required=True)
    parser.add_argument("-b", "--trans-b", help="Extra translation file; if a translation doesn't exist in trans-a, it will be copied from here.", required=True)
    parser.add_argument("-o", "--output", help="Output location of the merged TSV-formatted file as filepath,key,chinese,english")
    # Basepath is usually C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 for a default Steam install
    args = parser.parse_args()

    merge_translation_files(args)