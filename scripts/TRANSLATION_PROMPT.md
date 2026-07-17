# Translation Task Prompt

When I need you to translate missing keys, please follow these steps:

1. **Generate Missing Translations:**
   Use virtual environment `venv`.
   Run the coverage script to find all missing localization keys and output them to a JSON file:
   ```bash
   python scripts/check_translation_coverage.py -o scripts/missing_translations.json
   ```

2. **Translate the Keys:**
   Read the generated `scripts/missing_translations.json` file and translate the `original` Chinese text into English. 
   
   **Requirements for translation:**
   * **Schema Adherence:** Your final output MUST strictly match the JSON schema defined in `scripts/missing_translations_translated_schema.json`. It should be a JSON array of objects containing `file`, `key`, `original`, and `translation`.
   * **Terminology Consistency:** You must ensure consistency with names, proper nouns, and tags from the existing English translations. Search the existing English `.yml` localization files if you are unsure about a specific term.
   * **Formatting:** Preserve any Paradox localization formatting, color codes (e.g., `§Y...§!`), and variables (e.g., `[Root.GetName]`) exactly as they appear in the original text.
   
3. **Save Output:**
   Save your translated JSON array to `scripts/missing_translations_translated.json`.
