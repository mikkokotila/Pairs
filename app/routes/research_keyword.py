def research_keyword(self):

    import json

    from flask import request, jsonify, render_template

    from models.keyword_research import keyword_research
    from utils.session_manager import session_manager
    
    request_data = request.json
    text = request_data.get("text", "")
    text = keyword_research(text)
    response_text = f"{text}"

    session_manager(response_text)

    return jsonify(result=render_template("context_template.html",
                                            data=json.loads(response_text)))
