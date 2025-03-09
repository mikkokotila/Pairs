def lookup_glossary(self):

    import requests

    from flask import jsonify, render_template, request

    from utils.session_manager import session_manager

    request_data = request.json
    text = request_data.get("text", "")

    response = requests.get(f"http://127.0.0.1:5001/lookup-glossary?keyword={text}").json()

    session_manager(response)

    return jsonify(result=render_template("context_template.html", data=response))
