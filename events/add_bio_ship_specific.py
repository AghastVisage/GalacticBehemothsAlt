import os

search_add = {
    "gts_bruh_shipgirl_ship_sizes_1": "gts_bruh_shipgirl_ship_sizes_1_bio",
    "gts_bruh_shipgirl_ship_sizes_2": "gts_bruh_shipgirl_ship_sizes_2_bio",
    "gts_bruh_shipgirl_ship_sizes_3": "gts_bruh_shipgirl_ship_sizes_3_bio",
    "gts_destroyer_ship": "gts_destroyer_ship_bio",
    "gts_battleship_ship": "gts_battleship_ship_bio",
    "gts_titan_ship": "gts_titan_ship_bio"
}
for file in ["gts_event_bruh_shipgirl.txt"]:
    if os.path.isfile(file):
        with open(file, "r", encoding="utf-8-sig") as orig, open("gts_event_bruh_shipgirl_modded.txt", "w", encoding="utf-8-sig") as mod:
            for line in orig.readlines():
                mod.write(line)
                for search, add in search_add.items():
                    if search in line:
                        mod.write(line.replace(search, add))