def review(self):
        
        import re
        import json

        from models.auto_review import auto_review
        
        # Get the source column values and target column values
        source_column = self.data.iloc[:, 0].astype(str)
        target_column = self.data.iloc[:, 1].astype(str)

        # Initialize an empty list to store formatted strings
        formatted_rows = []

        # Iterate over each row with its index and format it
        # Only include rows where the target column is not empty
        for i, (source, target) in enumerate(zip(source_column, target_column)):
            if target.strip():  # Check if target is not empty
                formatted_rows.append(f'[[{i}]]{source}~{target}')

        # Join all formatted rows into a single string
        result_string = ''.join(formatted_rows)

        # If no rows to review, return early
        if not formatted_rows:
            return '', 204

        text = auto_review([result_string])
        response_text = f"{text}"

        # Make sure we're working with a string
        try:
            # Try to parse as JSON first
            review_data = json.loads(response_text)
            if isinstance(review_data, dict) and 'Review comments' in review_data:
                text = review_data['Review comments']
            else:
                text = str(review_data)
        except json.JSONDecodeError:
            # If not valid JSON, use the response text directly
            text = response_text
            
        # Ensure text is a string before splitting
        if not isinstance(text, str):
            text = str(text)

        text = re.split(r'(?=\[\[)', text)
        
        # Create a dictionary to map row indices to their review comments
        review_dict = {}
        
        # Skip the first element which is empty due to the split
        for comment in text[1:]:
            # Extract the row index from the comment
            match = re.match(r'\[\[(\d+)\]\]', comment)
            if match:
                row_idx = int(match.group(1))
                # Remove the [[i]] marker
                clean_comment = re.sub(r'\[\[\d+\]\]', '', comment)
                review_dict[row_idx] = clean_comment

        try:
            self.data[3]
        except KeyError:
            self.data[3] = ''

        # Update only the rows that have review comments
        for idx, comment in review_dict.items():
            self.data.iloc[idx, 3] = comment

        self.data.to_csv(self.csv_file_path + self.filename,
                         index=False,
                         header=False,
                         sep="~",
                         encoding="utf-8")

        return '', 204
