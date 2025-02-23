import dictionary_lookup
from flask import Flask, jsonify, request

dictionary = dictionary_lookup.DictionaryLookup(['tony_duff', 'verb_lexicon', 'monlam'])

app = Flask(__name__)


@app.route("/lookup-glossary", methods=["GET"])
def dictionary_api():

    keyword = request.args.get("keyword", "").strip()

    if keyword[-1] != '་':
        keyword += '་'

    if not keyword: 
        return jsonify({"error": "Missing 'keyword' parameter"}), 400

    result = {keyword: dictionary.lookup(keyword)}

    return jsonify(result[keyword])


if __name__ == "__main__":
    app.run(port=5001, debug=True)
