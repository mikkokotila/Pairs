from flask import session


def session_manager(response_text):
    """Add a response to the context history in the session."""
    if 'context_history' not in session:
        session['context_history'] = []

    session['context_history'].append(response_text)
    session.modified = True
    session['history_index'] = len(session['context_history']) - 1


def add_to_history(item):
    """Add an item to the history in the session.
    
    Args:
        item: The item to add to the history.
    """
    if 'history' not in session:
        session['history'] = []
    
    # Add the item to the history
    session['history'].append(item)
    
    # Limit the history to 10 items
    if len(session['history']) > 10:
        session['history'] = session['history'][1:]
    
    session.modified = True


def get_history():
    """Get the history from the session.
    
    Returns:
        list: The history items.
    """
    if 'history' not in session:
        session['history'] = []
    
    return session['history']


def get_history_item(index):
    """Get a specific item from the history.
    
    Args:
        index: The index of the item to get.
        
    Returns:
        The history item, or None if the index is invalid.
    """
    history = get_history()
    
    if index < 0 or index >= len(history):
        return None
    
    return history[index]
