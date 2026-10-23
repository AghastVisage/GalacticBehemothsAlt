import os
import argparse

replacements= [
    ("„", "\\\""),
    ("“", "\\\""),
    ("‚", "'"),
    ("‘", "'"),
    ("–", " - "),
    ("”", "\\\""),
    ("’", "'"),
    ("…", "..."),
    ("—", " - "),
    ("［", "<"),
    ("］", ">"),
    ("[Star Destroyer]","<Star Destroyer>"), # I don't have a good way of automatically locating every square-bracketed phrase without hitting actual commands
    ("[Blasphemer]","<Blasphemer>"), # Square brackets can be escaped, but it seems inconsistent
    ("[Insert into Aperture]", "<Insert into Aperture>"),
    ("[Seele]","<Seele>"),
    ("[Bronya]","<Bronya>"),
    ("【", "<"),
    ("】", ">"),
    ("\\\\n", "\\n"),
    ("少女", " maiden"), # I must have made a mistake in the translation software somewhere...
    ("视频", " video"),
    ]

def fixup_symbols(in_path):
    os.makedirs(in_path + "_fixed")

    for root, dirs, files in os.walk(in_path):
        for file in files:
            if file.split(".")[-1] == "yml":
                filepath = os.path.join(root, file)
                fixed_filepath = filepath.replace("english", "english_fixed", 1)
                os.makedirs(os.path.dirname(fixed_filepath), exist_ok=True)

                with open(filepath, "r", encoding="utf-8-sig") as input_file, open(fixed_filepath, "w", encoding="utf-8-sig") as fixed_file:
                    for line in input_file:
                        new_line = line
                        for from_str, to_str in replacements:
                            new_line = new_line.replace(from_str, to_str)
                        fixed_file.write(new_line)
    os.rename(in_path, in_path + "_bak")
    os.rename(in_path + "_fixed", in_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fixup symbols that Stellaris cannot parse.")
    # Basepath is usually C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 for a default Steam install
    parser.add_argument("-b", "--basepath", help="Base path of the mod; defaults to current directory", default=".")
    args = parser.parse_args()

    os.chdir(args.basepath)
    fixup_symbols(os.path.join("localisation", "english"))
    fixup_symbols(os.path.join("localisation", "replace", "english"))