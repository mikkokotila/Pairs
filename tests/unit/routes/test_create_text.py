import pytest
import os
import json
from unittest.mock import patch, MagicMock

from app.routes.create_text import create_text


@pytest.fixture
def mock_self():
    """Create a mock self object for the create_text function."""
    mock = MagicMock()
    mock.db_path = '/fake/path/'
    return mock


@pytest.fixture
def mock_request():
    """Create a mock for the request object."""
    with patch('app.routes.create_text.request') as mock:
        yield mock


@pytest.fixture
def mock_jsonify():
    """Create a mock for the jsonify function."""
    with patch('app.routes.create_text.jsonify') as mock:
        mock.return_value = {'status': 'success', 'message': 'File created successfully'}
        yield mock


@pytest.fixture
def mock_session():
    """Create a mock for the session object."""
    with patch('app.routes.create_text.session') as mock:
        yield mock


@pytest.fixture
def mock_create_entries():
    """Create a mock for the create_entries function."""
    with patch('app.routes.create_text.create_entries') as mock:
        yield mock


def test_create_text_basic(mock_self, mock_request, mock_jsonify, mock_session, mock_create_entries):
    """Test the basic functionality of the create_text function."""
    # Set up the request data
    mock_request.get_json.return_value = {
        'name': 'test_file',
        'content': 'Line 1\nLine 2\nLine 3'
    }
    
    # Mock os.path.exists to return False (file doesn't exist)
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        
        result = create_text(mock_self)
        
        # Check that create_entries was called with the correct arguments
        mock_create_entries.assert_called_once()
        db_path, name, entries = mock_create_entries.call_args[0]
        assert db_path == '/fake/path/'
        assert name == 'test_file'
        assert len(entries) == 3
        assert entries[0]['source_string'] == 'Line 1'
        assert entries[0]['target_string'] == ''
        assert entries[0]['style'] == 'Normal'
        assert entries[0]['annotation'] == []
        
        # Check that session was updated
        mock_session.__setitem__.assert_called_once_with('selected_file', 'test_file')
        
        # Check that jsonify was called with the correct arguments
        mock_jsonify.assert_called_once()
        status, message, filename = mock_jsonify.call_args[0][0]['status'], mock_jsonify.call_args[0][0]['message'], mock_jsonify.call_args[0][0]['filename']
        assert status == 'success'
        assert 'test_file' in message
        assert filename == 'test_file'


def test_create_text_file_exists(mock_self, mock_request, mock_jsonify):
    """Test the create_text function when the file already exists."""
    # Set up the request data
    mock_request.get_json.return_value = {
        'name': 'test_file',
        'content': 'Line 1\nLine 2\nLine 3'
    }
    
    # Mock os.path.exists to return True (file exists)
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        
        result = create_text(mock_self)
        
        # Check that jsonify was called with the correct arguments
        mock_jsonify.assert_called_once()
        status, message = mock_jsonify.call_args[0][0]['status'], mock_jsonify.call_args[0][0]['message']
        assert status == 'error'
        assert 'already exists' in message


def test_create_text_no_name(mock_self, mock_request, mock_jsonify):
    """Test the create_text function when no name is provided."""
    # Set up the request data with an empty name
    mock_request.get_json.return_value = {
        'name': '',
        'content': 'Line 1\nLine 2\nLine 3'
    }
    
    result = create_text(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once()
    status, message = mock_jsonify.call_args[0][0]['status'], mock_jsonify.call_args[0][0]['message']
    assert status == 'error'
    assert 'name is required' in message.lower()


def test_create_text_no_content(mock_self, mock_request, mock_jsonify):
    """Test the create_text function when no content is provided."""
    # Set up the request data with empty content
    mock_request.get_json.return_value = {
        'name': 'test_file',
        'content': ''
    }
    
    result = create_text(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once()
    status, message = mock_jsonify.call_args[0][0]['status'], mock_jsonify.call_args[0][0]['message']
    assert status == 'error'
    assert 'content is required' in message.lower()


def test_create_text_with_json_extension(mock_self, mock_request, mock_jsonify, mock_session, mock_create_entries):
    """Test the create_text function when the name includes a .json extension."""
    # Set up the request data with a .json extension in the name
    mock_request.get_json.return_value = {
        'name': 'test_file.json',
        'content': 'Line 1\nLine 2\nLine 3'
    }
    
    # Mock os.path.exists to return False (file doesn't exist)
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        
        result = create_text(mock_self)
        
        # Check that create_entries was called with the correct arguments
        mock_create_entries.assert_called_once()
        db_path, name, entries = mock_create_entries.call_args[0]
        assert db_path == '/fake/path/'
        assert name == 'test_file'  # .json should be removed
        
        # Check that session was updated
        mock_session.__setitem__.assert_called_once_with('selected_file', 'test_file')


def test_create_text_empty_lines(mock_self, mock_request, mock_jsonify, mock_session, mock_create_entries):
    """Test the create_text function with content that includes empty lines."""
    # Set up the request data with empty lines in the content
    mock_request.get_json.return_value = {
        'name': 'test_file',
        'content': 'Line 1\n\nLine 2\n\n\nLine 3'
    }
    
    # Mock os.path.exists to return False (file doesn't exist)
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        
        result = create_text(mock_self)
        
        # Check that create_entries was called with the correct arguments
        mock_create_entries.assert_called_once()
        db_path, name, entries = mock_create_entries.call_args[0]
        assert db_path == '/fake/path/'
        assert name == 'test_file'
        assert len(entries) == 3  # Empty lines should be removed
        assert entries[0]['source_string'] == 'Line 1'
        assert entries[1]['source_string'] == 'Line 2'
        assert entries[2]['source_string'] == 'Line 3'


def test_create_text_exception(mock_self, mock_request, mock_jsonify):
    """Test the create_text function when an exception is raised."""
    # Set up the request data
    mock_request.get_json.return_value = {
        'name': 'test_file',
        'content': 'Line 1\nLine 2\nLine 3'
    }
    
    # Mock os.path.exists to raise an exception
    with patch('os.path.exists') as mock_exists:
        mock_exists.side_effect = Exception('Test exception')
        
        result = create_text(mock_self)
        
        # Check that jsonify was called with the correct arguments
        mock_jsonify.assert_called_once()
        status, message = mock_jsonify.call_args[0][0]['status'], mock_jsonify.call_args[0][0]['message']
        assert status == 'error'
        assert 'Test exception' in message 