# Mod translation scripts

All scripts should be run from the root of the mod, usually `C:\Program Files (x86)\Steam\steamapps\workshop\content\281990\3057941504`

## Step 0: Setup mod git repository
The mod already is a git repository, but it seems to be setup weirdly, with a bunch of uncommitted changes.

To make it possible to revert when things go wrong, I recommend doing `git add ./` then `git commit -m "baseline"` to have a baseline commit of the state of the mod before modifications.

Also, you should apply patches 0001 and 0002 first - patch 0001 restores a bunch of translations that were made but unimplemented for whatever reason, while patch 0002 fixes some essential quotes issues in the Chinese script that breaks the parsing.

## Step 1: Mark untranslated text

    python localisation/mark_untranslated_text.py -o untranslated_text.csv

## Step 2: Translate text

### Test run - just copies Chinese text to English text

    python localisation/translate_text.py -i untranslated_text.csv -o translated_text.csv

### Actual run - Use DeepL for serviceable translations

#### DeepL setup

1. Go to DeepL website and register for free developer API
2. Import glossary.csv (important!) as the glossary, so that character names translate correctly
3. Put the API key into a file, e.g. deepl.key

#### Running the Python script

    python localisation/translate_text.py -i untranslated_text.csv -o translated_text.csv -d deepl.key -t deepl

### Step 3: Apply translated text onto the mod
This step will actually modify the localization files
    
    python localisation/apply_translated_text.py -i translated_text.csv

### Step 4: Fixup un-supported symbols
This script actually backs up the original files, simply because it's easier to do it this way

    python localisation/fixup_symbols.py

### Bonus: make_glossary.py

This script needs to be run from the root of the mod repository, and generates a dirty CSV glossary based on all the NAME_ definitions in all localization files. You'll need to manually go through the glossary to pick out any entries that don't make sense, or are duplicated.