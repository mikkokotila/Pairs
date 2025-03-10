from flask import request, jsonify, session
import os
import pandas as pd
from utils.db_operations import create_entries

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
        
        # Remove .json extension if it exists in the input name
        if name.endswith('.json'):
            name = name[:-5]
            
        # Store the base name (without extension) for session and display
        base_name = name
            
        # Add .json extension for checking if file exists
        file_path = os.path.join(self.db_path, name + '.json')
        if os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'A file with this name already exists'}), 400
        
        # Process content - split by newlines and remove empty lines
        lines = [line for line in content.split('\n') if line.strip()]
        
        # Create entries for TinyDB
        entries = []
        for line in lines:
            entries.append({
                'source_string': line,
                'target_string': '',
                'style': 'Normal',
                'annotation': []
            })
        
        # Save to TinyDB
        create_entries(self.db_path, name, entries)
        
        # Update session with the new file name
        session['selected_file'] = base_name
        
        return jsonify({
            'status': 'success', 
            'message': f'File "{base_name}" created successfully',
            'filename': base_name
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500 