# Automatically Organise Downloads Folder by File Type

## Project Overview
Scans your Downloads folder and automatically organizes files into categorized subfolders based on file extensions.

## How It Works
- Defines mapping of file extensions to folder categories
- Monitors Downloads folder for new files
- Moves files to appropriate subfolders (Images, Documents, Archives, etc.)
- Handles duplicate filenames and file conflicts

## Files
- organizer.py: Main organization script
- config.json: File type mapping configuration
- requirements.txt: Dependencies (standard library only)
- README.md: Usage instructions

## Setup Instructions
1. No external packages needed (uses Python standard library)
2. Customize config.json with your preferred categories
3. Run organizer.py manually or set up scheduled execution
4. Optionally install watchdog for real-time monitoring

## Features
- Customizable file type categories
- Duplicate filename handling
- Logging of all file movements
- Safe file moving with error handling

## Challenges Addressed
- Files in use/permission errors
- Unknown file extensions
- Partially downloaded files
- Cross-platform compatibility
