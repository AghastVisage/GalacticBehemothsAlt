from_key = "pc_gtsra_loli"
to_keys = "pc_gts_luanzi, pc_gtsra_shipgirl_body, pc_gtsra_loli_slave, pc_gts_kasa, pc_cheng_hui, pc_gts_yarong, pc_gtsra_bronya_slave, pc_wazi_cracked, pc_gts_seele, pc_gts_seele_li, pc_gts_bronya, pc_gts_linfeng_planet, pc_lottie_shoes, pc_gts_uniform_shoes_colonizable, pc_gts_laceup_heel, pc_gts_claudia_boots, pc_gts_normal_boots, pc_yarong_boots, pc_gts_cyrene_shoes_1, pc_gts_cyrene_shoes_2, pc_gts_underware, pc_gts_linfeng_shoes1_planet, pc_gts_linfeng_shoes2_planet, pc_gts_linfeng_shoes3_planet, pc_gts_Starchasm_Nyx_shoes_planet, pc_gts_bronya_shoes_planet, pc_gts_Mirrored_Flourishes_shoes_planet, pc_gts_straw_planet"

with open("base.txt", "r") as infile, open("done.txt", "w") as outfile:
    lines = infile.readlines()
    for item in to_keys.split(", "):
        for line in lines:
            outfile.write(line.replace(from_key, item))