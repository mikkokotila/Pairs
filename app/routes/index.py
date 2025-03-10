def index(self):
    
    import os
    from flask import render_template, request, session
    from utils.db_operations import get_all_entries
    
    # Gather base filenames (without extensions)
    self.all_files = [
        f.split('.')[0]
        for f in os.listdir(self.db_path)
        if os.path.isfile(os.path.join(self.db_path, f)) and f.endswith('.json')
    ]

    # Filter out glossary.json from the file list
    self.all_files = [f for f in self.all_files if f != 'glossary']

    # Get user selection from the form (POST). Returns None if nothing posted.
    self.selected = request.form.get('filename')

    # If no file is selected from the form, check if there's a file in the session
    if self.selected is None:
        # Check if there's a selected file in the session
        self.selected = session.get('selected_file')
        
        # If still no file is selected, select the first in dir listing
        if self.selected is None or self.selected not in self.all_files:
            self.selected = self.all_files[0] if self.all_files else None

    # Store the selected filename for other routes
    self.filename = self.selected
    
    # Get data from TinyDB
    self.data = get_all_entries(self.db_path, self.selected) if self.selected else None
    
    # Drop any rows where all columns are empty
    if self.data is not None:
        self.data = self.data.dropna(how='all')
        
        # Reset index after dropping rows
        self.data = self.data.reset_index(drop=True)

    # Prepare data for template
    rows = self.data[['source_string', 'target_string', 'style']].values.tolist() if self.data is not None else []

    # Render the template, passing both the list of file base names and the currently selected one
    return render_template('index.html',
                          rows=rows,
                          files=self.all_files,
                          selected=self.selected)
