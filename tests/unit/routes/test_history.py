import pytest
from unittest.mock import patch, MagicMock

from app.routes.history import history


@pytest.fixture
def mock_self():
    """Create a mock self object for the history function."""
    mock = MagicMock()
    return mock


@pytest.fixture
def mock_request():
    """Create a mock for the request object."""
    with patch('app.routes.history.request') as mock:
        mock.args = {}
        yield mock


@pytest.fixture
def mock_jsonify():
    """Create a mock for the jsonify function."""
    with patch('app.routes.history.jsonify') as mock:
        mock.return_value = {'result': 'mocked_result'}
        yield mock


@pytest.fixture
def mock_session():
    """Create a mock for the session object."""
    with patch('app.routes.history.session') as mock:
        # Set up the session with a context_history and history_index
        mock.get.side_effect = lambda key, default=None: {
            'context_history': ['History item 1', 'History item 2', 'History item 3'],
            'history_index': 1
        }.get(key, default)
        yield mock


def test_history_no_direction(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when no direction is specified."""
    # Set up the request with no direction
    mock_request.args = {}
    
    result = history(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': 'History item 2'})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_back_direction(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when the direction is 'back'."""
    # Set up the request with direction=back
    mock_request.args = {'direction': 'back'}
    
    result = history(mock_self)
    
    # Check that the history_index was decremented
    mock_session.__setitem__.assert_called_once_with('history_index', 0)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': 'History item 1'})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_forward_direction(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when the direction is 'forward'."""
    # Set up the request with direction=forward
    mock_request.args = {'direction': 'forward'}
    
    result = history(mock_self)
    
    # Check that the history_index was incremented
    mock_session.__setitem__.assert_called_once_with('history_index', 2)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': 'History item 3'})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_back_at_beginning(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when going back at the beginning of history."""
    # Set up the request with direction=back
    mock_request.args = {'direction': 'back'}
    
    # Set up the session with history_index at 0 (beginning of history)
    mock_session.get.side_effect = lambda key, default=None: {
        'context_history': ['History item 1', 'History item 2', 'History item 3'],
        'history_index': 0
    }.get(key, default)
    
    result = history(mock_self)
    
    # Check that the history_index was not changed
    mock_session.__setitem__.assert_not_called()
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': 'History item 1'})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_forward_at_end(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when going forward at the end of history."""
    # Set up the request with direction=forward
    mock_request.args = {'direction': 'forward'}
    
    # Set up the session with history_index at the end of history
    mock_session.get.side_effect = lambda key, default=None: {
        'context_history': ['History item 1', 'History item 2', 'History item 3'],
        'history_index': 2
    }.get(key, default)
    
    result = history(mock_self)
    
    # Check that the history_index was not changed
    mock_session.__setitem__.assert_not_called()
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': 'History item 3'})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_no_history(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when there's no history."""
    # Set up the session with no context_history
    mock_session.get.side_effect = lambda key, default=None: {
        'context_history': None,
        'history_index': None
    }.get(key, default)
    
    result = history(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': ''})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_empty_history(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when the history is empty."""
    # Set up the session with an empty context_history
    mock_session.get.side_effect = lambda key, default=None: {
        'context_history': [],
        'history_index': None
    }.get(key, default)
    
    result = history(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': ''})
    
    # Check the return value
    assert result == {'result': 'mocked_result'}


def test_history_invalid_index(mock_self, mock_request, mock_jsonify, mock_session):
    """Test the history function when the history_index is invalid."""
    # Set up the session with an invalid history_index
    mock_session.get.side_effect = lambda key, default=None: {
        'context_history': ['History item 1', 'History item 2', 'History item 3'],
        'history_index': 10  # Out of range
    }.get(key, default)
    
    result = history(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({'result': ''})
    
    # Check the return value
    assert result == {'result': 'mocked_result'} 