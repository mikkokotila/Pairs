def get_context(self):

    """Get the context data for a specific row"""
    
    import os
    import pandas as pd
    from flask import jsonify, request
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
        
        # Check if we have a fourth column (index 3) for annotations
        if self.data.shape[1] > 3:
            # Get the value from the fourth column (index 3)
            context_value = self.data.iloc[row_index, 3]
            
            # Simple check for empty values
            if pd.isna(context_value) or context_value is None or context_value == "":
                return jsonify({"result": "", "has_content": False})
            
            # Handle list type
            if isinstance(context_value, list):
                if len(context_value) == 0:
                    return jsonify({"result": "", "has_content": False})
                try:
                    # Safely convert list items to strings
                    safe_items = []
                    for item in context_value:
                        if item is not None:
                            safe_items.append(str(item))
                    context_value = "<br>".join(safe_items)
                except Exception as e:
                    print(f"Error converting list to string: {str(e)}")
                    return jsonify({"result": "", "has_content": False})
            else:
                # Convert to string safely
                try:
                    context_value = str(context_value)
                    if context_value.strip() == "":
                        return jsonify({"result": "", "has_content": False})
                except Exception as e:
                    print(f"Error converting value to string: {str(e)}")
                    return jsonify({"result": "", "has_content": False})
            
            # Add heading and content with the new heading "Annotations"
            formatted_content = f"<h3>Annotations</h3><div class='review-content'>{context_value}</div>"
            return jsonify({"result": formatted_content, "has_content": True})
        else:
            return jsonify({"result": "", "has_content": False})
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in get_context: {str(e)}")
        return jsonify({"result": f"Error: {str(e)}", "has_content": False}), 500
