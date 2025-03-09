def explain_grammar(self):

    import json
    from json import JSONDecodeError

    from flask import jsonify, render_template, request

    from utils.session_manager import session_manager
    from models.explain_grammar import explain_grammar

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
