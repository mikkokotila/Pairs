from urllib import request


def history(self):

    import json
    from json import JSONDecodeError
    from flask import jsonify, render_template, request, session

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