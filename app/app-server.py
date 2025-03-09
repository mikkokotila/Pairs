from flask import Flask
from flask_session import Session

import sys
sys.path.insert(0, '../../Bokit')
import bokit


class TranslationApp:
    
    def __init__(self):
        
        # App setup
        self.app = Flask(__name__)
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['SECRET_KEY'] = '1234'
        Session(self.app)
        self.app.secret_key = '1234'
        self.csv_file_path = "data/"
        
        # Navigational routes
        self.app.add_url_rule("/", "index", self.index, methods=["GET", "POST"])
        self.app.add_url_rule("/new", "new", self.new, methods=["GET", "POST"])
        self.app.add_url_rule("/translate", "translate", self.translate, methods=["GET", "POST"])
        self.app.add_url_rule("/review", "review", self.review, methods=["GET", "POST"])
        self.app.add_url_rule("/commit", "commit", self.commit, methods=["GET"])
        self.app.add_url_rule("/publish", "publish", self.publish, methods=["GET"])

        # Glossary routes
        self.app.add_url_rule("/glossary", "glossary", self.glossary, methods=["POST"])

        # Context menu routes
        self.app.add_url_rule("/research-keyword", "research_keyword", self.research_keyword, methods=["POST"])
        self.app.add_url_rule("/suggest-translation", "suggest_translation", self.suggest_translation, methods=["POST"])
        self.app.add_url_rule("/lookup-glossary", "lookup_glossary", self.lookup_glossary, methods=["POST"])
        self.app.add_url_rule("/find-examples", "find_examples", self.find_examples, methods=["POST"])
        self.app.add_url_rule("/explain-grammar", "explain_grammar", self.explain_grammar, methods=["POST"])

        # Hidden functionality routes
        self.app.add_url_rule("/history", "history", self.history, methods=["GET"])
        self.app.add_url_rule("/get-context", "get_context", self.get_context, methods=["POST"])
        self.app.add_url_rule("/autosave", "autosave", self.autosave, methods=["POST"])
        self.app.add_url_rule("/create-text", "create_text", self.create_text, methods=["POST"])

    ## Navigation routes
    def index(self):

        from routes.index import index
        return index(self)
    
    def new(self):

        from routes.new import new
        return new(self)
    
    def translate(self):

        from routes.translate import translate
        return translate(self)
    
    def review(self):

        from routes.review import review
        return review(self)
    
    def commit(self):

        from routes.commit import commit
        return commit(self)
    
    def publish(self):

        from routes.publish import publish
        return publish(self)
    
    ## Glossary routes
    def glossary(self):

        from routes.glossary import glossary
        return glossary(self)
    
    ## Context menu routes
    def research_keyword(self):

        from routes.research_keyword import research_keyword
        return research_keyword(self)
    
    def suggest_translation(self):

        from routes.suggest_translation import suggest_translation
        return suggest_translation(self)
    
    def lookup_glossary(self):

        from routes.lookup_glossary import lookup_glossary
        return lookup_glossary(self)
    
    def find_examples(self):

        from routes.find_examples import find_examples
        return find_examples(self)
    
    def explain_grammar(self):

        from routes.explain_grammar import explain_grammar
        return explain_grammar(self)    
    
    ## Hidden functionality routes
    def history(self):

        from routes.history import history
        return history(self)
    
    def get_context(self):

        from routes.get_context import get_context
        return get_context(self)
    
    def autosave(self):

        from routes.autosave import autosave
        return autosave(self)
    
    def create_text(self):

        from routes.create_text import create_text
        return create_text(self)
        

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    TranslationApp().run()