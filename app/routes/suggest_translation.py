from urllib import request


def suggest_translation(self):

    import json

    from json import JSONDecodeError
    from flask import request, jsonify, render_template

    from utils.session_manager import session_manager
    from models.suggest_translation import suggest_translation

    request_data = request.json
    text = request_data.get("text", "")
    text = suggest_translation([text])
    response_text = f"{text}"

    session_manager(response_text)

    try:
        return jsonify(result=render_template("context_template.html",
                                                data=json.loads(response_text)))
    except JSONDecodeError:
        return {"response_text": response_text}
    