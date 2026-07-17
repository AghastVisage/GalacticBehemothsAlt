# GTSS Development Guidelines

## Mod Overview
- Stellaris mod: "星河巨影" ("Stellar Giant Shadow")
- Supported Stellaris version: 3.14.*
- Workshop ID: 3057941504

## Development Commands
- Testing: Load mod through Stellaris launcher with debug mode enabled
- Linting: Manual verification of syntax in Paradox script files
- Deployment: Upload to Steam Workshop via Stellaris launcher

## File Structure
- Prefix mod-specific files with `gts_` (e.g., `gts_traits.txt`)
- Organize files by content type in appropriate directories
- Use descriptive filenames indicating content purpose

## Coding Style
- Follow Paradox scripting syntax conventions
- Use indentation (tabs) for nested blocks
- Include comments for complex logic sections
- Keep related functionality in same file
- Maintain consistent naming scheme across related files

## Localization
- Store translations in localization directory
- Use standard Stellaris localization format
- Ensure all player-facing text has proper localization

## Version Control
- Make granular commits with clear descriptions
- Include feature/bugfix details in commit messages
- Use branches for major feature development