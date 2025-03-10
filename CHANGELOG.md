# Changelog

## 22:54 on 10-03-2025
- Migrated data storage from CSV to TinyDB
  - Added TinyDB dependency to the project
  - Created db_operations.py with TinyDB utility functions
  - Updated routes to use TinyDB instead of CSV files
  - Modified data structure to use source_string, target_string, style, and annotation

## 22:30 on 09-03-2025
- Added ability to add new text from GUI
  - Added 'New' button to the navigation menu
  - Moved CSS from new.html to style.css
  - Implemented active state styling for navigation buttons

## 17:30 on 09-03-2025
- Fixed Reader view feature to match requirements
  - Removed heading from the reader modal
  - Swapped order to show translation above Tibetan text
  - Adjusted spacing between pairs for better readability

## 16:58 on 09-03-2025
- Added Reader view feature
  - Added a Read button to the navigation menu
  - Implemented a modal for the reader view
  - Formatted content with Tibetan text followed by its translation
  - Added responsive styling for the reader modal
