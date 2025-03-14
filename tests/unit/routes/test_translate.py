import pytest
import pandas as pd
import json
import re
from unittest.mock import patch, MagicMock, mock_open

from app.routes.translate import translate


@pytest.fixture
def mock_self():
    """Create a mock self object for the translate function."""
    mock = MagicMock()
    mock.data = pd.DataFrame({
        'source_string': ['Test string 1', 'Test string 2', 'Test string 3'],
        'target_string': ['', '', ''],
        'style': ['Normal', 'Normal', 'Normal'],
        'annotation': [[], [], []]
    })
    mock.filename = 'test_file.csv'
    mock.db_path = '/fake/path/'
    return mock


@pytest.fixture
def mock_auto_translate():
    """Create a mock for the auto_translate function."""
    with patch('app.routes.translate.auto_translate') as mock:
        mock.return_value = '[[0]]Translated string 1[[1]]Translated string 2[[2]]Translated string 3'
        yield mock


@pytest.fixture
def mock_update_entry():
    """Create a mock for the update_entry function."""
    with patch('app.routes.translate.update_entry') as mock:
        yield mock


@pytest.fixture
def mock_redirect():
    """Create a mock for the redirect function."""
    with patch('app.routes.translate.redirect') as mock:
        mock.return_value = 'Redirected'
        yield mock


@pytest.fixture
def mock_url_for():
    """Create a mock for the url_for function."""
    with patch('app.routes.translate.url_for') as mock:
        mock.return_value = '/'
        yield mock


def test_translate_basic(mock_self, mock_auto_translate, mock_update_entry, mock_redirect, mock_url_for):
    """Test the basic functionality of the translate function."""
    result = translate(mock_self)
    
    # Check that auto_translate was called with the correct arguments
    mock_auto_translate.assert_called_once()
    call_args = mock_auto_translate.call_args[0][0]
    assert '[[0]]Test string 1[[1]]Test string 2[[2]]Test string 3' in call_args[0]
    
    # Check that the data was updated correctly
    assert mock_self.data.iloc[0, 1] == 'Translated string 1'
    assert mock_self.data.iloc[1, 1] == 'Translated string 2'
    assert mock_self.data.iloc[2, 1] == 'Translated string 3'
    
    # Check that update_entry was called for each row
    assert mock_update_entry.call_count == 3
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 0, 'target_string', 'Translated string 1')
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 1, 'target_string', 'Translated string 2')
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 2, 'target_string', 'Translated string 3')
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_translate_json_response(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the translate function with a JSON response."""
    with patch('app.routes.translate.auto_translate') as mock_auto_translate:
        # Return a JSON string with a Translation key
        mock_auto_translate.return_value = json.dumps({
            'Translation': '[[0]]Translated string 1[[1]]Translated string 2[[2]]Translated string 3'
        })
        
        result = translate(mock_self)
        
        # Check that the data was updated correctly
        assert mock_self.data.iloc[0, 1] == 'Translated string 1'
        assert mock_self.data.iloc[1, 1] == 'Translated string 2'
        assert mock_self.data.iloc[2, 1] == 'Translated string 3'


def test_translate_json_no_translation_key(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the translate function with a JSON response that doesn't have a Translation key."""
    with patch('app.routes.translate.auto_translate') as mock_auto_translate:
        # Return a JSON string without a Translation key
        mock_auto_translate.return_value = json.dumps({
            'OtherKey': '[[0]]Translated string 1[[1]]Translated string 2[[2]]Translated string 3'
        })
        
        result = translate(mock_self)
        
        # Check that the data was updated correctly (should use the whole response)
        assert mock_self.data.iloc[0, 1] == '{"OtherKey": "[[0]]Translated string 1[[1]]Translated string 2[[2]]Translated string 3"}'


def test_translate_json_decode_error(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the translate function with a response that can't be parsed as JSON."""
    with patch('app.routes.translate.auto_translate') as mock_auto_translate:
        # Return a string that's not valid JSON
        mock_auto_translate.return_value = '[[0]]Translated string 1[[1]]Translated string 2[[2]]Translated string 3'
        
        # Mock print to capture the warning message
        with patch('builtins.print') as mock_print:
            result = translate(mock_self)
            
            # Check that the warning was printed
            mock_print.assert_any_call("JSONDecodeError: Could not parse response as JSON. Using raw response.")
        
        # Check that the data was updated correctly (should use the raw response)
        assert mock_self.data.iloc[0, 1] == 'Translated string 1'
        assert mock_self.data.iloc[1, 1] == 'Translated string 2'
        assert mock_self.data.iloc[2, 1] == 'Translated string 3'


def test_translate_split_failure(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the translate function when splitting the response fails."""
    with patch('app.routes.translate.auto_translate') as mock_auto_translate:
        # Return a response that doesn't have row markers
        mock_auto_translate.return_value = 'No row markers here'
        
        # Mock print to capture the warning message
        with patch('builtins.print') as mock_print:
            result = translate(mock_self)
            
            # Check that the warning was printed
            mock_print.assert_any_call("Warning: Could not parse translations from response.")
        
        # Check that the data was updated with empty strings
        assert mock_self.data.iloc[0, 1] == ''
        assert mock_self.data.iloc[1, 1] == ''
        assert mock_self.data.iloc[2, 1] == ''


def test_translate_database_error(mock_self, mock_auto_translate, mock_redirect, mock_url_for):
    """Test the translate function when there's an error saving to the database."""
    with patch('app.routes.translate.update_entry') as mock_update_entry:
        # Make update_entry raise an exception
        mock_update_entry.side_effect = Exception('Database error')
        
        # Mock print to capture the error message
        with patch('builtins.print') as mock_print:
            result = translate(mock_self)
            
            # Check that the error was printed
            mock_print.assert_any_call("Error saving translations to database: Database error")
        
        # Check that redirect was still called
        mock_redirect.assert_called_once_with('/') 