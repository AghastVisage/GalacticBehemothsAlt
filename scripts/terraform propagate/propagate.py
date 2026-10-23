from_key = "urine"
to_keys = "urine2, juice, juice2, juice3, milk, semen, dirt0, dirt1, dirt2, dirt3, dirt4"

with open("base.txt", "r") as infile, open("done.txt", "w") as outfile:
    lines = infile.readlines()
    for item in to_keys.split(", "):
        for line in lines:
            outfile.write(line.replace(from_key, item))