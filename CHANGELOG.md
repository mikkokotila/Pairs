# Changelog

## 16:45 on 13-03-2025
- Fixed Claude API authentication issue
  - Added proper error handling for missing API key
  - Created .env.template file with instructions for setting up API key
  - Updated README.md with detailed API key setup instructions
  - Improved error messages for better user experience

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

## 23:15 on 11-03-2025
- Added Lotsawa House integration
  - Updated "Add Text" functionality to accept Lotsawa House URLs
  - Created a new route to fetch content from Lotsawa House
  - Modified placeholder text to indicate the new functionality
  - Added automatic content extraction from Lotsawa House pages

## 23:30 on 11-03-2025
- Fixed Tibetan text extraction from Lotsawa House
  - Improved character encoding handling
  - Added multiple methods to extract text content
  - Added User-Agent header to requests
  - Enhanced text cleaning to preserve Tibetan characters
