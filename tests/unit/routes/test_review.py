import pytest
import pandas as pd
import json
import re
from unittest.mock import patch, MagicMock, mock_open

from app.routes.review import review


@pytest.fixture
def mock_self():
    """Create a mock self object for the review function."""
    mock = MagicMock()
    mock.data = pd.DataFrame({
        'source_string': ['Source 1', 'Source 2', 'Source 3'],
        'target_string': ['Target 1', 'Target 2', 'Target 3'],
        'style': ['Normal', 'Normal', 'Normal'],
        'annotation': [[], [], []]
    })
    mock.filename = 'test_file.csv'
    mock.db_path = '/fake/path/'
    return mock


@pytest.fixture
def mock_auto_review():
    """Create a mock for the auto_review function."""
    with patch('app.routes.review.auto_review') as mock:
        mock.return_value = '[[0]]Review comment 1[[1]]Review comment 2[[2]]Review comment 3'
        yield mock


@pytest.fixture
def mock_update_entry():
    """Create a mock for the update_entry function."""
    with patch('app.routes.review.update_entry') as mock:
        yield mock


@pytest.fixture
def mock_redirect():
    """Create a mock for the redirect function."""
    with patch('app.routes.review.redirect') as mock:
        mock.return_value = 'Redirected'
        yield mock


@pytest.fixture
def mock_url_for():
    """Create a mock for the url_for function."""
    with patch('app.routes.review.url_for') as mock:
        mock.return_value = '/'
        yield mock


def test_review_basic(mock_self, mock_auto_review, mock_update_entry, mock_redirect, mock_url_for):
    """Test the basic functionality of the review function."""
    result = review(mock_self)
    
    # Check that auto_review was called with the correct arguments
    mock_auto_review.assert_called_once()
    call_args = mock_auto_review.call_args[0][0]
    assert '[[0]]Source 1\nTarget 1[[1]]Source 2\nTarget 2[[2]]Source 3\nTarget 3' in call_args[0]
    
    # Check that update_entry was called for each row
    assert mock_update_entry.call_count == 3
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 0, 'annotation', ['Review comment 1'])
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 1, 'annotation', ['Review comment 2'])
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 2, 'annotation', ['Review comment 3'])
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_review_json_response(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the review function with a JSON response."""
    with patch('app.routes.review.auto_review') as mock_auto_review:
        # Return a JSON string with a Review key
        mock_auto_review.return_value = json.dumps({
            'Review': '[[0]]Review comment 1[[1]]Review comment 2[[2]]Review comment 3'
        })
        
        result = review(mock_self)
        
        # Check that update_entry was called for each row
        assert mock_update_entry.call_count == 3
        mock_update_entry.assert_any_call('/fake/path/', 'test_file', 0, 'annotation', ['Review comment 1'])
        mock_update_entry.assert_any_call('/fake/path/', 'test_file', 1, 'annotation', ['Review comment 2'])
        mock_update_entry.assert_any_call('/fake/path/', 'test_file', 2, 'annotation', ['Review comment 3'])


def test_review_json_no_review_key(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the review function with a JSON response that doesn't have a Review key."""
    with patch('app.routes.review.auto_review') as mock_auto_review:
        # Return a JSON string without a Review key
        mock_auto_review.return_value = json.dumps({
            'OtherKey': '[[0]]Review comment 1[[1]]Review comment 2[[2]]Review comment 3'
        })
        
        result = review(mock_self)
        
        # Check that update_entry was called for each row with the whole response as the annotation
        assert mock_update_entry.call_count == 3
        for i in range(3):
            mock_update_entry.assert_any_call('/fake/path/', 'test_file', i, 'annotation', 
                                             ['{"OtherKey": "[[0]]Review comment 1[[1]]Review comment 2[[2]]Review comment 3"}'])


def test_review_json_decode_error(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the review function with a response that can't be parsed as JSON."""
    with patch('app.routes.review.auto_review') as mock_auto_review:
        # Return a string that's not valid JSON
        mock_auto_review.return_value = '[[0]]Review comment 1[[1]]Review comment 2[[2]]Review comment 3'
        
        # Mock print to capture the warning message
        with patch('builtins.print') as mock_print:
            result = review(mock_self)
            
            # Check that the warning was printed
            mock_print.assert_any_call("JSONDecodeError: Could not parse response as JSON. Using raw response.")
        
        # Check that update_entry was called for each row
        assert mock_update_entry.call_count == 3
        mock_update_entry.assert_any_call('/fake/path/', 'test_file', 0, 'annotation', ['Review comment 1'])
        mock_update_entry.assert_any_call('/fake/path/', 'test_file', 1, 'annotation', ['Review comment 2'])
        mock_update_entry.assert_any_call('/fake/path/', 'test_file', 2, 'annotation', ['Review comment 3'])


def test_review_split_failure(mock_self, mock_update_entry, mock_redirect, mock_url_for):
    """Test the review function when splitting the response fails."""
    with patch('app.routes.review.auto_review') as mock_auto_review:
        # Return a response that doesn't have row markers
        mock_auto_review.return_value = 'No row markers here'
        
        # Mock print to capture the warning message
        with patch('builtins.print') as mock_print:
            result = review(mock_self)
            
            # Check that the warning was printed
            mock_print.assert_any_call("Warning: Could not parse review comments from response.")
        
        # Check that update_entry was not called (no annotations to update)
        mock_update_entry.assert_not_called()


def test_review_existing_annotations(mock_self, mock_auto_review, mock_update_entry, mock_redirect, mock_url_for):
    """Test the review function when there are existing annotations."""
    # Add existing annotations to the data
    mock_self.data.at[0, 'annotation'] = ['Existing annotation 1']
    mock_self.data.at[1, 'annotation'] = ['Existing annotation 1', 'Existing annotation 2']
    
    result = review(mock_self)
    
    # Check that update_entry was called for each row with the new annotation appended to the existing ones
    assert mock_update_entry.call_count == 3
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 0, 'annotation', ['Existing annotation 1', 'Review comment 1'])
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 1, 'annotation', ['Existing annotation 1', 'Existing annotation 2', 'Review comment 2'])
    mock_update_entry.assert_any_call('/fake/path/', 'test_file', 2, 'annotation', ['Review comment 3'])


def test_review_database_error(mock_self, mock_auto_review, mock_redirect, mock_url_for):
    """Test the review function when there's an error saving to the database."""
    with patch('app.routes.review.update_entry') as mock_update_entry:
        # Make update_entry raise an exception
        mock_update_entry.side_effect = Exception('Database error')
        
        # Mock print to capture the error message
        with patch('builtins.print') as mock_print:
            result = review(mock_self)
            
            # Check that the error was printed
            mock_print.assert_any_call("Error saving review comments to database: Database error")
        
        # Check that redirect was still called
        mock_redirect.assert_called_once_with('/') 