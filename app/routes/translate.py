def translate(self):

    import re
    import json

    from flask import render_template
    from models.auto_translate import auto_translate
    from utils.db_operations import update_entry
    
    # Get the source column values
    column_values = self.data['source_string'].astype(str)

    # Initialize an empty list to store formatted strings
    formatted_rows = []

    # Iterate over each row with its index and format it
    for i, row in enumerate(column_values):
        formatted_rows.append(f'[[{i}]]{row}')

    # Join all formatted rows into a single string
    result_string = ''.join(formatted_rows)

    text = auto_translate([result_string])
    response_text = f"{text}"

    text = json.loads(response_text)['Translation']

    text = re.split(r'(?=\[\[)', text)
    
    '''
    for i in range(len(column_values)):
        print(str(i), text[i+1])
    '''

    text = [re.sub(r'\[\[\d+\]\]', '', i) for i in text[1:]]

    # Update the dataframe with the translated text
    self.data.iloc[:, 1] = text

    # Get the current filename from the app instance (without .csv extension)
    filename = self.filename.replace('.csv', '')
    
    # Save all translated rows to the database
    try:
        for i, translated_text in enumerate(text):
            # Update each row in the database
            update_entry(self.db_path, filename, i, 'target_string', translated_text)
    except Exception as e:
        print(f"Error saving translations to database: {str(e)}")

    return render_template('index.html',
                            rows=self.data.values.tolist(),
                            files=self.all_files,
                            selected=self.selected)
