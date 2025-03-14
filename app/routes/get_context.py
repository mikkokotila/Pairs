def get_context(self):

    """Get the context data for a specific row"""
    
    import os
    import pandas as pd
    from flask import jsonify, request, render_template
    from utils.db_operations import get_all_entries
    
    try:
        # Ensure self.data is available
        if not hasattr(self, 'data') or self.data is None:
            # If self.selected is not set, set it to the first file
            if not hasattr(self, 'selected') or self.selected is None:
                self.all_files = [
                    f.split('.')[0]
                    for f in os.listdir(self.db_path)
                    if os.path.isfile(os.path.join(self.db_path, f)) and f.endswith('.json')
                ]
                self.all_files = [f for f in self.all_files if f != 'glossary']
                self.selected = self.all_files[0] if self.all_files else None
            
            # Get the data from TinyDB
            self.filename = self.selected
            self.data = get_all_entries(self.db_path, self.selected) if self.selected else None
            
            if self.data is not None:
                self.data = self.data.dropna(how='all')
                self.data = self.data.reset_index(drop=True)
        
        row_index = int(request.json.get('row_index', 0))
        
        # Ensure the row index is valid
        if row_index >= len(self.data):
            return jsonify({"result": "", "has_content": False})
        
        # Get the annotation field for the specified row
        # The annotation field is a column in the DataFrame
        if 'annotation' in self.data.columns:
            annotation_value = self.data.iloc[row_index]['annotation']
            
            # Check if the annotation is a list (as per the database structure)
            if isinstance(annotation_value, list):
                # If it's a list, check if it's empty
                if not annotation_value:
                    # Empty list, no annotations
                    context_data = {
                        "Annotations": "No annotations for this row"
                    }
                else:
                    # List has items, render them
                    context_data = {
                        "Annotations": annotation_value
                    }
            else:
                # If it's not a list or it's None/NaN
                if pd.isna(annotation_value) or annotation_value is None or annotation_value == "":
                    context_data = {
                        "Annotations": "No annotations for this row"
                    }
                else:
                    # Convert to string if it's not already
                    context_data = {
                        "Annotations": str(annotation_value)
                    }
            
            # Render the context template with the data
            rendered_html = render_template('context_template.html', data=context_data)
            return jsonify({"result": rendered_html, "has_content": True})
        else:
            # If annotation column doesn't exist
            context_data = {
                "Annotations": "No annotations for this row"
            }
            rendered_html = render_template('context_template.html', data=context_data)
            return jsonify({"result": rendered_html, "has_content": True})
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"result": f"Error: {str(e)}", "has_content": False}), 500
