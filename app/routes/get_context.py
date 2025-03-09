def get_context(self):

    """Get the context data for a specific row"""
    
    import os
    import pandas as pd
    from flask import jsonify, request
    
    try:
        # Ensure self.data is available
        if not hasattr(self, 'data') or self.data is None:
            # If self.selected is not set, set it to the first file
            if not hasattr(self, 'selected') or self.selected is None:
                self.all_files = [
                    f.split('.')[0]
                    for f in os.listdir(self.csv_file_path)
                    if os.path.isfile(os.path.join(self.csv_file_path, f))
                ]
                self.all_files = [f for f in self.all_files if f != 'glossary']
                self.selected = self.all_files[0]
            
            # Set the filename and read the CSV
            self.filename = self.selected + '.csv'
            self.data = self.read_csv()
            self.data = self.data.dropna(how='all')
            self.data = self.data.reset_index(drop=True)
        
        row_index = int(request.json.get('row_index', 0))
        
        # Check if the DataFrame has at least 4 columns (for review comments)
        
        # Ensure the row index is valid
        if row_index >= len(self.data):
           
            return jsonify({"result": "", "has_content": False})
        
        # Check if we have a fourth column (index 3) for review comments
        if self.data.shape[1] > 3:
            # Get the value from the fourth column (index 3)
            context_value = self.data.iloc[row_index, 3]
            
            
            # Convert to string and handle NaN/None values
            if pd.isna(context_value) or context_value is None or context_value == "":
                
                return jsonify({"result": "", "has_content": False})
            else:
                context_value = str(context_value)
                
                # Add heading and content
                formatted_content = f"<h3>Review Comment</h3><div class='review-content'>{context_value}</div>"
                return jsonify({"result": formatted_content, "has_content": True})
        else:
            
            return jsonify({"result": "", "has_content": False})
    except Exception as e:
        
        import traceback
        traceback.print_exc()
        return jsonify({"result": f"Error: {str(e)}", "has_content": False}), 500
