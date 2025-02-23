import sys
sys.path.insert(0, '../../Bokit/')

import bokit

import random

from flask import Flask, jsonify, request

from models.build_corpus import build_corpus

corpus = build_corpus()

app = Flask(__name__)


@app.route("/find-examples", methods=["GET"])
def corpus_api():
    keyword = request.args.get("keyword", "").strip()

    result = {}
    
    for text in corpus.keys():
        text_result = []
        for segment in corpus[text]:
            if keyword in segment:
                text_result.append(segment)
        if len(text_result) > 5:
            result[text] = random.choices(list(set(text_result)), k=5)
        elif len(text_result) > 0:
            result[text] = list(set(text_result))

    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
