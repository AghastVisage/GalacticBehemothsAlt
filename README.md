# GalacticBehemothsAlt

What can I say, I'm a Determined Separatist. Come what may, I'll not suffer flaws in the system, unity or community be damned.

This is a fork-mod of [Galactic Behemoths](https://steamcommunity.com/sharedfiles/filedetails/?id=3057941504), focused on fixing bugs, restoring half-gone content, filling in localization, plus a bunch of random functional changes that I put in just because I liked it.

To use this mod:
  1. Click Code -> Download Zip on this page
  2. Unzip the mod
  3. Copy 3057941504.mod to <your user directory>/Documents/Paradox Interactive\Stellaris\mod
  4. Edit 3057941504.mod after it's been copied, so that the line starting with path= contains the path where you extracted the mod
  5. The mod should appear on the launcher, I think; I don't really use the launcher, so I haven't tested that.

Alternatively, just delete C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504 and replace its contents with this mod, although when the proper mod is updated, it will overwrite all changes.

I might put this onto Steam Workshop in the future, but I'll navigate that account later.

All credit goes to them.

## List of changes

### Filled in missing localization

Using DeepL (instead of generic LLM, because I don't like to open letters with swords), I filled in all missing translations per-file.

I don't know how the original team manages to screw it up every patch, maybe the translation was run on individual branches instead of 

In 4.6, the new translations are just added to the end - in 4.7, I'll be using the (newer) tsv versions of the scripts so the English loc keeps the same order of keys as the Chinese loc, which should make it easier to fix up stuff like the menu that explains what each character does.

There are also persistent name screwups that I'll fix in the 4.7 version:
 - Xino -> Xinuo
 - Apro -> Aplog (aplog, your username is aplog, and that's your OC, right)
 - Liuying (Firefly) -> Firefly

I also did a bunch of translations manually. I can read Chinese, I just don't like writing it for trauma reasons.

### Bugfixes

 - Illya_warship_active and Illya_school_warship_active are cleared when the fleets are recalled from the communications
 - Fixed unequipping GTS leader item causing the save file to crash the game when next loaded
 - Fixed GTS bio-trophies requiring Synthetic Dawn DLC, which no longer exists and the check no longer passes
 - Some planet events -> carrier events, notably fixes Guya's recruitment chain
 - Aurora's Slumber system now spawns correctly
 - Huatian's special project now creates fewer errors in the log
 - Size-based workforce multipliers no longer affect Wilderness & Virtuality, which caused many bugs
 - Virtuality now ignores jobs that the founder species pop can never take (tiny-trophy, arkship unlimited civilians)
 - Attempted to fix Eyjafalla for Wilderness by triggering event on terraforming (untested)
 - Attempted to fix Evolutionary Catalyst for Wilderness by triggering event on terraforming without adding real pops (untested)
 - Fixed crisis perk conditions, Endbringers are no longer able to pick a crisis, Wilderness can pick Behemoth Fury again, and there should be no remaining cases where a second crisis perk can be picked
 - Eliza & Blemishine hiring now function
 - Obsolete ai_categories block removed
 - Infernals with a size traitnow correctly have alloy upkeep and no food upkeep
 - Suppress errors for generic leader traits that refer to their owners, when they have no owner
 - Fix Giant Magical Girls being bound to the pre-Shadow of the Shroud Psionic tradition
 - Restore some tradition effects that went missing when copied into the mod
 - Shipgirls are now available to countries using a Biological Shipset
 - Clicking Seele/Black Seele/Bronya's icons and then cancelling the hiring no longer sets their hired flag without starting the hiring event chain
 - Tiny Servitors also apply boosts to Complex Drones
 - Fixed Jump Drive Cooldown effect from Gateway GTS item
 - Made it possible to pick Self-Serve without picking its civic
   - They should have mutual dependencies, but I'm too lazy to try to implement that
 - Fixed Xinuo's fleet event, so that it actually adds the relevant trait/fleet when the option is picked


### Changes
 - Survive tradition now reduces leader upkeep as stated in description
 - gts_leader_body_5_2 trait now gives Entertainer instead of Historical Curator jobs, which is a job swap and can't be assigned directly
 - GTS cloning buildings now also respond to Biogenesis Cloning tradition's build caps
 - GTS Terrain Pioneer now has a Gestalt version
   - This will be superceded by the main mod 4.7 giving every job a Gestalt version. Terrain Pioneer particularly needs a Gestalt version, because using Consumer Goods basically bricks this job when it appears at the beginning of the game
 - Leader body traits give Gestalt jobs
   - Will be superceded by main mod 4.7
 - Blue Seele also gets fast affection growth like Red Seele and Bronya
   - 4.7 removes *all* fast affection. This is a problem, because with enough abuse, you can basically be at endgame by 2215
   - I'll probably restore fast affection, but tie it to body exploration. Doing body exploration early is key to 
 - Psionic Sovereign in the base game is overriden to allow Holy Imperial System authority
 - A humiliation event that could cause 100% devastation now just causes 98%, so it doesn't insta-destroy arkships
 - Moved a few gts system spawns into gts_common_ui so their location shows up
 - Arkships get access to Wilderness district specializations
 - Wilderness can briefly colonize Aurora, enough to give her food
 - Seele/Dark Seele/Bronya arkships get Production Overseer jobs for their main districts
 - Holy Imperial authority gives edict fund, instead of the now-obsolete Admin Cap
 - Getting the tech that improves Love Juice/Semen habitability for spiritualists no longer removes 2 of the pop/influence generating blockers

### Nomad Compatibility
 - Sonxi picks a random planet near the arkship if nomadic, and the special project works
 - Eyjafjalla and Aurora now spawn a Contract when their planets appear, clearing that contract progresses their event
 - Nomads can now research megastructures too, even though they can only be used as GTS equipment and not built in the galaxy
 - Several random_owned_system checks changed to 1-6 jumps from capital (Bronya, Hitomi, Bruh shipgirls)
 - Su Xiaobai can be hired without colony loss as Nomad, 4.7 will have new behaviour for Su Xiaobai
 - Nomads can build GTS habitats with Arkship Engineering, Wilderness does not need any tech to do the same

### Changes made on a whim
 - gts_civilians_unlimited_seele/seele_li/bronya is now limited to 100000 instead of 9999999
   - Starchasm Nyx now gets the same modifiers as the other max-level Arkships
   - (it's in the Sonxi nomad commit because I made a mistake)
 - GTS equippable Research Nexus gives +0.1 to Physicist, Engineer & Biologist so that it can boost normal, non-mod researchers, down from +1 to just nonspecific researchers
   - +1 is significantly too powerful, with +0.1 & 15% Research Speed you'd still need to equip quite a few Nexuses & actually build your empire to get 1 technology per month, +1 just hands that to you a bit too early
 - Isharm'la no longer destroys anything if you trigger the "Skadi saves the galaxy" case with 5 favours
   - The script quite frankly didn't work properly to begin with, especially if you have habitable megas from mods
 - AIs are significantly more likely to pick crisis perks, and the requirement to conquer 10% of the galaxy no longer applies
 - GTS planets are no longer considered artificial (use discretion and do not try to turn them into Ecumenopolises or Resort Worlds, things will break)
 - GTS planets can be terraformed back into normal planets
 - Bronya Scientist increases resources produced by stations instead of increasing size of deposits
 - Seele Governor applies Psionic Job Efficiency to Planet too, not just Sector
 - Removed build cap for GTS arkship
   - They're not that overpowered until you get to Tier 3 and get access to the truly ludicrous weapons, especially compared to infinite Netherworld Guardians from Tilipoca
   - And if you build too many arkships, the upkeep will kill your empire.
 - GTS research center researchers split into 3 jobs - one for each reserach type, and Giantess researchers job now only produce 1 type of research instead of all 3
   - Makes them compatible with base game produced research boosts
 - Fixed the script that creates FE planets after you win Cosmogenesis
   - Yes, this is entirely a base game fix that has nothing to do with the mod.
   - It still creates duplicates of buildings, but it's fine, they went through Cosmo, they ought to do some impossible things
 - Hitomi's Colossus weapon can target any planet, I just added this to blow up a Holy World early for fun, and then decided against removing it


### Broken stuff not fixed
 - The Shrink/GTS resource cost for activating body effects (gts_bruh_get_gts_*_cost_amount_variable) is calculated as 10000/5000/2500 + (resource income) * 12. But if the resource income is negative - which can happen once you have access to the market & at least 833 Shrunken People/Giantess Fluid - you can activate body effects and instead *gain* gts/shrink resources.
   - Also, the variable is blank on 2200.01.01, so you can immediately activate Isonami's body for 375 Influence and permanent resource income.