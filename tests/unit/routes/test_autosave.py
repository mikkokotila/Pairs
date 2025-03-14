import pytest
from unittest.mock import patch, MagicMock

from app.routes.autosave import autosave


@pytest.fixture
def mock_self():
    """Create a mock self object for the autosave function."""
    mock = MagicMock()
    mock.filename = 'test_file.csv'
    mock.db_path = '/fake/path/'
    return mock


@pytest.fixture
def mock_request():
    """Create a mock for the request object."""
    with patch('app.routes.autosave.request') as mock:
        mock.json = {
            'content': 'Updated content',
            'row': 0
        }
        yield mock


@pytest.fixture
def mock_jsonify():
    """Create a mock for the jsonify function."""
    with patch('app.routes.autosave.jsonify') as mock:
        mock.return_value = {'status': 'saved'}
        yield mock


@pytest.fixture
def mock_update_entry():
    """Create a mock for the update_entry function."""
    with patch('app.routes.autosave.update_entry') as mock:
        yield mock


@pytest.fixture
def mock_get_all_entries():
    """Create a mock for the get_all_entries function."""
    with patch('app.routes.autosave.get_all_entries') as mock:
        yield mock


def test_autosave_basic(mock_self, mock_request, mock_jsonify, mock_update_entry):
    """Test the basic functionality of the autosave function."""
    result = autosave(mock_self)
    
    # Check that update_entry was called with the correct arguments
    mock_update_entry.assert_called_once_with('/fake/path/', 'test_file', 0, 'target_string', 'Updated content')
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with(status="saved")
    
    # Check the return value
    assert result == {'status': 'saved'}


def test_autosave_different_row(mock_self, mock_request, mock_jsonify, mock_update_entry):
    """Test the autosave function with a different row."""
    # Change the row in the request
    mock_request.json['row'] = 5
    
    result = autosave(mock_self)
    
    # Check that update_entry was called with the correct arguments
    mock_update_entry.assert_called_once_with('/fake/path/', 'test_file', 5, 'target_string', 'Updated content')
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with(status="saved")
    
    # Check the return value
    assert result == {'status': 'saved'}


def test_autosave_different_content(mock_self, mock_request, mock_jsonify, mock_update_entry):
    """Test the autosave function with different content."""
    # Change the content in the request
    mock_request.json['content'] = 'Different content'
    
    result = autosave(mock_self)
    
    # Check that update_entry was called with the correct arguments
    mock_update_entry.assert_called_once_with('/fake/path/', 'test_file', 0, 'target_string', 'Different content')
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with(status="saved")
    
    # Check the return value
    assert result == {'status': 'saved'}


def test_autosave_different_filename(mock_self, mock_request, mock_jsonify, mock_update_entry):
    """Test the autosave function with a different filename."""
    # Change the filename in the mock_self
    mock_self.filename = 'different_file.csv'
    
    result = autosave(mock_self)
    
    # Check that update_entry was called with the correct arguments
    mock_update_entry.assert_called_once_with('/fake/path/', 'different_file', 0, 'target_string', 'Updated content')
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with(status="saved")
    
    # Check the return value
    assert result == {'status': 'saved'}


def test_autosave_no_csv_extension(mock_self, mock_request, mock_jsonify, mock_update_entry):
    """Test the autosave function with a filename that doesn't have a .csv extension."""
    # Change the filename in the mock_self to one without a .csv extension
    mock_self.filename = 'test_file'
    
    result = autosave(mock_self)
    
    # Check that update_entry was called with the correct arguments
    mock_update_entry.assert_called_once_with('/fake/path/', 'test_file', 0, 'target_string', 'Updated content')
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with(status="saved")
    
    # Check the return value
    assert result == {'status': 'saved'} 