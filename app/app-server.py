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
        self.app.add_url_rule("/keyword-research", "keyword_research", self.keyword_research, methods=["POST"])
        self.app.add_url_rule("/pre-translation", "pre_translation", self.pre_translation, methods=["POST"])
        self.app.add_url_rule("/auto-translation", "auto_translation", self.auto_translation, methods=["GET", "POST"])
        self.app.add_url_rule("/lookup-glossary", "lookup_glossary", self.lookup_glossary, methods=["POST"])
        self.app.add_url_rule("/find-examples", "find_examples", self.find_examples, methods=["POST"])
        self.app.add_url_rule("/explain-grammar", "explain_grammar", self.explain_grammar, methods=["POST"])

    def index(self):
        # Gather base filenames (without extensions)
        self.all_files = [
            f.split('.')[0]
            for f in os.listdir(self.csv_file_path)
            if os.path.isfile(os.path.join(self.csv_file_path, f))
        ]

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

        print(self.data)

        return render_template('index.html',
                               rows=self.data.values.tolist(),
                               files=self.all_files,
                               selected=self.selected)

    def publish(self):

        from utils.get_env_vars import get_env_vars
        from models.publish_to_docs import publish_to_docs

        env_vars = get_env_vars(keys=['service_account_subject', 'service_account_file'],
                                file_name='.env',
                                relative_to_pwd='../../../')
        
        #rint(self.data.values.tolist())

        publish_to_docs(
            '../service-account-file.json',
            env_vars['service_account_subject'],
            self.data.values.tolist(),
            self.selected)

        return '', 204

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

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    TranslationApp().run()