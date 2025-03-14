import pytest
from flask import session

from app.utils.session_manager import (
    add_to_history,
    get_history,
    get_history_item
)


def test_add_to_history(app, client):
    """Test adding an item to the history."""
    with client.session_transaction() as sess:
        # Initialize an empty history
        sess['history'] = []
    
    with app.test_request_context():
        # Add an item to the history
        add_to_history('Test Item')
        
        # Check that the item was added to the history
        assert session['history'] == ['Test Item']
        
        # Add another item to the history
        add_to_history('Another Item')
        
        # Check that both items are in the history
        assert session['history'] == ['Test Item', 'Another Item']


def test_add_to_history_limit(app, client):
    """Test that the history is limited to 10 items."""
    with client.session_transaction() as sess:
        # Initialize a history with 10 items
        sess['history'] = [f'Item {i}' for i in range(10)]
    
    with app.test_request_context():
        # Add an item to the history
        add_to_history('New Item')
        
        # Check that the history still has 10 items
        assert len(session['history']) == 10
        
        # Check that the oldest item was removed
        assert session['history'][0] == 'Item 1'
        
        # Check that the new item was added
        assert session['history'][-1] == 'New Item'


def test_get_history_empty(app, client):
    """Test getting an empty history."""
    with client.session_transaction() as sess:
        # Initialize an empty history
        sess['history'] = []
    
    with app.test_request_context():
        # Get the history
        history = get_history()
        
        # Check that the history is empty
        assert history == []


def test_get_history(app, client):
    """Test getting a history with items."""
    with client.session_transaction() as sess:
        # Initialize a history with items
        sess['history'] = ['Item 1', 'Item 2', 'Item 3']
    
    with app.test_request_context():
        # Get the history
        history = get_history()
        
        # Check that the history has the expected items
        assert history == ['Item 1', 'Item 2', 'Item 3']


def test_get_history_item_valid_index(app, client):
    """Test getting a history item with a valid index."""
    with client.session_transaction() as sess:
        # Initialize a history with items
        sess['history'] = ['Item 1', 'Item 2', 'Item 3']
    
    with app.test_request_context():
        # Get a history item
        item = get_history_item(1)
        
        # Check that the item is the expected one
        assert item == 'Item 2'


def test_get_history_item_invalid_index(app, client):
    """Test getting a history item with an invalid index."""
    with client.session_transaction() as sess:
        # Initialize a history with items
        sess['history'] = ['Item 1', 'Item 2', 'Item 3']
    
    with app.test_request_context():
        # Get a history item with an invalid index
        item = get_history_item(10)
        
        # Check that None is returned
        assert item is None 