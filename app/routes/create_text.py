from flask import request, jsonify, session
import os
import pandas as pd
import csv

def create_text(self):
    """
    Handles the POST request to create a new text file.
    
    Expected POST parameters:
    - name: The name of the new file (without extension)
    - content: The content of the new file (Tibetan text)
    
    Returns:
    - JSON response with success/error message
    """
    try:
        # Get data from request
        data = request.get_json()
        name = data.get('name', '').strip()
        content = data.get('content', '').strip()
        
        # Validate input
        if not name:
            return jsonify({'status': 'error', 'message': 'File name is required'}), 400
        
        if not content:
            return jsonify({'status': 'error', 'message': 'Content is required'}), 400
        
        # Remove .csv extension if it exists in the input name
        if name.endswith('.csv'):
            name = name[:-4]
            
        # Store the base name (without extension) for session and display
        base_name = name
            
        # Add .csv extension for the actual file
        file_name = name + '.csv'
        
        # Check if file already exists
        file_path = os.path.join(self.csv_file_path, file_name)
        if os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'A file with this name already exists'}), 400
        
        # Process content - split by newlines and remove empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        
        # Create DataFrame with Tibetan text, empty translation column, style column, and empty notes column
        df = pd.DataFrame({
            'source': lines,
            'target': [''] * len(lines),
            'style': ['Normal'] * len(lines),
            'notes': [''] * len(lines)  # Add fourth column to ensure trailing tilde after "Normal"
        })
        
        # Save to CSV file with tilde (~) separator, without quoting
        df.to_csv(file_path, 
                 index=False, 
                 header=False, 
                 sep="~", 
                 quoting=csv.QUOTE_NONE,
                 encoding="utf-8",
                 escapechar='\\')  # Escape character needed when QUOTE_NONE is used
        
        # Update session with the new file (without .csv extension)
        session['selected_file'] = base_name
        
        return jsonify({
            'status': 'success', 
            'message': f'File "{base_name}" created successfully',
            'filename': base_name
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500 