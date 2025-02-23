from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

import pandas as pd

import json
from json import JSONDecodeError
import requests
import os

from session_manager import session_manager
from models.keyword_research import keyword_research as kr
from models.pre_translate import pre_translate
from models.explain_grammar import explain_grammar
from models.commit_to_github import commit_to_github

import sys
sys.path.insert(0, '../Bokit')
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
        self.app.add_url_rule("/history", "history", self.history, methods=["GET"])
        self.app.add_url_rule("/keyword-research", "keyword_research", self.keyword_research, methods=["POST"])
        self.app.add_url_rule("/pre-translation", "pre_translation", self.pre_translation, methods=["POST"])
        self.app.add_url_rule("/lookup-glossary", "lookup_glossary", self.lookup_glossary, methods=["POST"])
        self.app.add_url_rule("/find-examples", "find_examples", self.find_examples, methods=["POST"])
        self.app.add_url_rule("/explain-grammar", "explain_grammar", self.explain_grammar, methods=["POST"])

    def index(self):
        # Gather base filenames (without extensions)
        all_files = [
            f.split('.')[0]
            for f in os.listdir(self.csv_file_path)
            if os.path.isfile(os.path.join(self.csv_file_path, f))
        ]

        # Get user selection from the form (POST). Returns None if nothing posted.
        selected = request.form.get('filename')

        # If the user hasn't selected anything yet, default to the first file
        if not selected:
            selected = all_files[0]

        # Construct the .csv filename from the selected base name
        self.filename = selected + '.csv'
        
        # Read the CSV data
        self.data = self.read_csv()

        # Render the template, passing both the list of file base names and the currently selected one
        return render_template('index.html',
                               rows=self.data.values.tolist(),
                               files=all_files,
                               selected=selected)

    def read_csv(self):

        # Read in the local datastore from csv
        data = pd.read_csv(self.csv_file_path + self.filename,
                           header=None,
                           sep="~",
                           dtype=str,
                           keep_default_na=False,
                           engine="python")
        
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
        
        # Call the commit_to_github function
        # commit_to_github()

        return jsonify(status="saved")
    
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