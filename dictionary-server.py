import sys
sys.path.insert(0, '../dev-notebooks')

import dictionary_lookup
from flask import Flask, jsonify, request  # Import `request` to handle query parameters

dictionary = dictionary_lookup.DictionaryLookup(['tony_duff', 'verb_lexicon', 'monlam'])

app = Flask(__name__)


@app.route("/lookup-glossary", methods=["GET"])
def dictionary_api():
    # Get the keyword from the query string (e.g., ?keyword=nnn)
    keyword = request.args.get("keyword", "").strip()

    if keyword[-1] != '་':
        keyword += '་'

    if not keyword:  # If no keyword is provided, return an error
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    result = {keyword: dictionary.lookup(keyword)}

    return jsonify(result[keyword])


if __name__ == "__main__":
    app.run(port=5001, debug=True)