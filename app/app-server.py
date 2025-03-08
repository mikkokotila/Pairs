from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session

import pandas as pd

import json
from json import JSONDecodeError
import requests
import os

from utils.session_manager import session_manager
from models.keyword_research import keyword_research as kr
from models.auto_translate import auto_translate
from models.pre_translate import pre_translate
from models.explain_grammar import explain_grammar
from models.commit_to_github import commit_to_github

import sys
sys.path.insert(0, '../../Bokit')
import bokit


class TranslationApp:
    
    def __init__(self):
        
        self.app = Flask(__name__)
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['SECRET_KEY'] = '1234'
        Session(self.app)
        self.app.secret_key = '1234'
        self.csv_file_path = "data/"
        self.app.add_url_rule("/", "index", self.index, methods=["GET", "POST"])
        self.app.add_url_rule("/autosave", "autosave", self.autosave, methods=["POST"])
        self.app.add_url_rule("/commit", "commit", self.commit, methods=["GET"])
        self.app.add_url_rule("/publish", "publish", self.publish, methods=["GET"])
        self.app.add_url_rule("/history", "history", self.history, methods=["GET"])
        self.app.add_url_rule("/glossary", "glossary", self.glossary, methods=["POST"])
        self.app.add_url_rule("/keyword-research", "keyword_research", self.keyword_research, methods=["POST"])
        self.app.add_url_rule("/pre-translation", "pre_translation", self.pre_translation, methods=["POST"])
        self.app.add_url_rule("/auto-translation", "auto_translation", self.auto_translation, methods=["GET", "POST"])
        self.app.add_url_rule("/auto-review", "auto_review", self.auto_review, methods=["GET", "POST"])
        self.app.add_url_rule("/lookup-glossary", "lookup_glossary", self.lookup_glossary, methods=["POST"])
        self.app.add_url_rule("/find-examples", "find_examples", self.find_examples, methods=["POST"])
        self.app.add_url_rule("/explain-grammar", "explain_grammar", self.explain_grammar, methods=["POST"])
        self.app.add_url_rule("/get-context", "get_context", self.get_context, methods=["POST"])

    def index(self):
        
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

        # If no file is selected, select the first in dir listing 
        if self.selected is None:
            self.selected = self.all_files[0]

        # Construct the .csv filename from the selected base name
        self.filename = self.selected + '.csv'
        
        # Read the CSV data
        self.data = self.read_csv()
        
        # Drop any rows where all columns are empty
        self.data = self.data.dropna(how='all')
        
        # Reset index after dropping rows
        self.data = self.data.reset_index(drop=True)

        # Render the template, passing both the list of file base names and the currently selected one
        return render_template('index.html',
                               rows=self.data.values.tolist(),
                               files=self.all_files,
                               selected=self.selected)

    def read_csv(self):

        print(self.csv_file_path + self.filename)

        # Read in the local datastore from csv
        data = pd.read_csv(self.csv_file_path + self.filename,
                           header=None,
                           sep="~",
                           dtype=str,
                           keep_default_na=False,
                           engine="c")
        
        # If the CSV has just one column, add a target column
        if data.shape[1] == 1:
            data["target"] = ""
            data['style'] = "Normal"

        return data

    def autosave(self):
        
        content = request.json["content"]
        row = request.json["row"]

        data = self.read_csv()
        data.iloc[row, 1] = content

        data.to_csv(self.csv_file_path + self.filename,
                    index=False,
                    header=False,
                    sep="~",
                    encoding="utf-8")

        return jsonify(status="saved")
    

    def commit(self):

        commit_to_github(self.filename)

        return '', 204


    def history(self):

        direction = request.args.get('direction', '')

        if 'context_history' not in session or not session['context_history']:
            return jsonify({'error': 'No history available'}), 400
        
        if 'history_index' not in session:
            session['history_index'] = len(session['context_history']) - 1

        if direction == 'back' and session['history_index'] > 0:
            session['history_index'] -= 1
        
        elif direction == 'forward' and session['history_index'] < len(session['context_history']) - 1:
            session['history_index'] += 1

        response_text = session['context_history'][session['history_index']]

        try:
            return jsonify(result=render_template("context_template.html",
                                                  data=response_text))
        except JSONDecodeError:
            return jsonify(result=render_template("context_template.html",
                                                  data=response_text))

    # CONTEXT MENU FUNCTIONS ->

    def keyword_research(self):
        
        request_data = request.json
        text = request_data.get("text", "")
        text = kr(text)
        response_text = f"{text}"

        session_manager(response_text)

        return jsonify(result=render_template("context_template.html",
                                              data=json.loads(response_text)))
    
    def auto_translation(self):

        import re
        
        # Get the source column values
        column_values = self.data.iloc[:, 0].astype(str)

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

        for i in range(len(column_values)):
            print(str(i), text[i+1])

        text = [re.sub(r'\[\[\d+\]\]', '', i) for i in text[1:]]

        self.data.iloc[:, 1] = text

        return render_template('index.html',
                               rows=self.data.values.tolist(),
                               files=self.all_files,
                               selected=self.selected)

    def auto_review(self):
        from models.auto_review import auto_review
        import re
        
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
    

    def publish(self):

        from utils.get_env_vars import get_env_vars
        from models.publish_to_docs import publish_to_docs

        env_vars = get_env_vars(keys=['service_account_subject', 'service_account_file'],
                                file_name='.env',
                                relative_to_pwd='../../../')

        publish_to_docs(
            '../service-account-file.json',
            env_vars['service_account_subject'],
            self.data.values.tolist(),
            self.selected)

        return '', 204
    
    def glossary(self):

        # Sufficient for lookup
        search_term = request.form.get('search_term').strip()

        # Needed for the case where new entry is added
        if search_term.startswith('+'):

            content = search_term.split('+')[-1].strip().split(' ')
            source_language = content[0]
            target_language = content[-1]

            with open('data/glossary.txt', 'a') as file:
                file.write(f"{source_language}~{target_language}\n")

            return jsonify(result=render_template("context_template.html",
                                                  data={source_language: target_language}))
        
        # Handle the case where keyword lookup is made
        with open('data/glossary.txt', 'r') as file:
            glossary = file.readlines()
        
        for line in glossary:
            
            if search_term == line.split('~')[0]:
                return jsonify(result=render_template("context_template.html", data={search_term: line.split('~')[1]}))
            
        return jsonify(result=render_template("context_template.html",
                                                      data={search_term: 'No results found'}))

    def pre_translation(self):

        request_data = request.json
        text = request_data.get("text", "")
        text = pre_translate([text])
        response_text = f"{text}"

        session_manager(response_text)

        try:
            return jsonify(result=render_template("context_template.html",
                                                  data=json.loads(response_text)))
        except JSONDecodeError:
            return {"response_text": response_text}
    
    def lookup_glossary(self):

        request_data = request.json
        text = request_data.get("text", "")

        response = requests.get(f"http://127.0.0.1:5001/lookup-glossary?keyword={text}").json()

        session_manager(response)

        return jsonify(result=render_template("context_template.html", data=response))
    
    def find_examples(self):

        request_data = request.json
        text = request_data.get("text", "")

        response = requests.get(f"http://127.0.0.1:5002/find-examples?keyword={text}").json()

        session_manager(response)

        return jsonify(result=render_template("context_template.html", data=response))
    
    def explain_grammar(self):

        request_data = request.json
        text = request_data.get("text", "")
        text = explain_grammar(text)
        response_text = f"{text}"

        session_manager(response_text)

        try:
            return jsonify(result=render_template("context_template.html",
                                                data=json.loads(response_text)))
        except JSONDecodeError:
            return {"response_text": response_text}

    def get_context(self):
        """Get the context data for a specific row"""
        try:
            print("get_context called")
            
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
                print(f"Initialized self.data with shape: {self.data.shape}")
            
            row_index = int(request.json.get('row_index', 0))
            print(f"Row index: {row_index}")
            
            # Check if the DataFrame has at least 4 columns (for review comments)
            print(f"DataFrame shape: {self.data.shape}")
            
            # Ensure the row index is valid
            if row_index >= len(self.data):
                print(f"Row index {row_index} is out of bounds for DataFrame with {len(self.data)} rows")
                return jsonify({"result": "", "has_content": False})
            
            # Check if we have a fourth column (index 3) for review comments
            if self.data.shape[1] > 3:
                # Get the value from the fourth column (index 3)
                context_value = self.data.iloc[row_index, 3]
                print(f"Context value: {context_value}")
                
                # Convert to string and handle NaN/None values
                if pd.isna(context_value) or context_value is None or context_value == "":
                    print("No content found")
                    return jsonify({"result": "", "has_content": False})
                else:
                    context_value = str(context_value)
                    print(f"Content found: {context_value}")
                    # Add heading and content
                    formatted_content = f"<h3>Review Comment</h3><div class='review-content'>{context_value}</div>"
                    return jsonify({"result": formatted_content, "has_content": True})
            else:
                print("DataFrame doesn't have enough columns for review comments")
                return jsonify({"result": "", "has_content": False})
        except Exception as e:
            print(f"Error in get_context: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"result": f"Error: {str(e)}", "has_content": False}), 500

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    TranslationApp().run()