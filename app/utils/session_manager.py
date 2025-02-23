from flask import session


def session_manager(response_text):

    if 'context_history' not in session:
        session['context_history'] = []

    session['context_history'].append(response_text)
    session.modified = True
    session['history_index'] = len(session['context_history']) - 1
