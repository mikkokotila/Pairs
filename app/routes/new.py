from flask import render_template, request, session
import os

def new(self):
    """
    Renders the page with the modal for adding new text.
    """
    # Get list of available files (without extensions)
    files = [f.replace('.csv', '') for f in os.listdir(self.csv_file_path) if f.endswith('.csv')]
    
    # If no files, provide a default empty list
    if not files:
        files = []
    
    # Get selected file from session or use the first file
    selected = session.get('selected_file', files[0] if files else None)
    
    return render_template('new.html', files=files, selected=selected) 