def index(self):
    
    import os
    from flask import render_template, request, session

    from utils.read_csv import read_csv
    # Gather base filenames (without extensions)
    self.all_files = [
        f.split('.')[0]
        for f in os.listdir(self.csv_file_path)
        if os.path.isfile(os.path.join(self.csv_file_path, f))
    ]

    # Filter out glossary.csv from the file list
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

    # Construct the .csv filename from the selected base name
    self.filename = self.selected + '.csv' if self.selected else None
    
    # Read the CSV data
    self.data = read_csv(self)
    
    # Drop any rows where all columns are empty
    self.data = self.data.dropna(how='all')
    
    # Reset index after dropping rows
    self.data = self.data.reset_index(drop=True)

    # Render the template, passing both the list of file base names and the currently selected one
    return render_template('index.html',
                            rows=self.data.values.tolist(),
                            files=self.all_files,
                            selected=self.selected)
