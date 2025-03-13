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

    # Add error handling for JSON parsing
    try:
        # Try to parse as JSON first
        parsed_json = json.loads(response_text)
        if isinstance(parsed_json, dict) and 'Translation' in parsed_json:
            text = parsed_json['Translation']
        else:
            # If JSON doesn't have 'Translation' key, use the whole response
            text = response_text
    except json.JSONDecodeError:
        # If not valid JSON, use the response text directly
        print(f"JSONDecodeError: Could not parse response as JSON. Using raw response.")
        text = response_text

    # Split the text by the row markers
    text = re.split(r'(?=\[\[)', text)
    
    '''
    for i in range(len(column_values)):
        print(str(i), text[i+1])
    '''

    # Make sure we have at least one element after splitting
    if len(text) > 1:
        # Remove the row markers and use the translated text
        text = [re.sub(r'\[\[\d+\]\]', '', i) for i in text[1:]]
    else:
        # If splitting failed, create empty translations
        text = [''] * len(column_values)
        print("Warning: Could not parse translations from response.")

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
