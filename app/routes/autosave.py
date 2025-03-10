def autosave(self):

    from flask import request, jsonify
    from utils.db_operations import update_entry, get_all_entries
    
    content = request.json["content"]
    row = request.json["row"]
    
    # Get the current filename from the app instance
    filename = self.filename.replace('.csv', '')
    
    # Update the specific field in TinyDB
    update_entry(self.db_path, filename, row, 'target_string', content)

    return jsonify(status="saved")
