import pytest
import os
import subprocess
from unittest.mock import patch, MagicMock

from app.routes.commit import commit


@pytest.fixture
def mock_self():
    """Create a mock self object for the commit function."""
    mock = MagicMock()
    mock.filename = 'test_file.csv'
    mock.db_path = '/fake/path/'
    return mock


@pytest.fixture
def mock_subprocess_run():
    """Create a mock for the subprocess.run function."""
    with patch('app.routes.commit.subprocess.run') as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def mock_redirect():
    """Create a mock for the redirect function."""
    with patch('app.routes.commit.redirect') as mock:
        mock.return_value = 'Redirected'
        yield mock


@pytest.fixture
def mock_url_for():
    """Create a mock for the url_for function."""
    with patch('app.routes.commit.url_for') as mock:
        mock.return_value = '/'
        yield mock


@pytest.fixture
def mock_print():
    """Create a mock for the print function."""
    with patch('builtins.print') as mock:
        yield mock


def test_commit_basic(mock_self, mock_subprocess_run, mock_redirect, mock_url_for, mock_print):
    """Test the basic functionality of the commit function."""
    result = commit(mock_self)
    
    # Check that subprocess.run was called with the correct arguments
    assert mock_subprocess_run.call_count == 3
    mock_subprocess_run.assert_any_call(["git", "add", "/fake/path/test_file.json"], check=True)
    mock_subprocess_run.assert_any_call(["git", "commit", "-m", "Autosave commit"], check=True)
    mock_subprocess_run.assert_any_call(["git", "push", "origin", "main"], check=True)
    
    # Check that print was called with the correct message
    mock_print.assert_called_once_with("Changes committed and pushed to GitHub successfully.")
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_commit_error(mock_self, mock_subprocess_run, mock_redirect, mock_url_for, mock_print):
    """Test the commit function when an error occurs."""
    # Make subprocess.run raise an exception
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git')
    
    result = commit(mock_self)
    
    # Check that print was called with the correct error message
    mock_print.assert_called_once()
    assert "An error occurred while committing to GitHub" in mock_print.call_args[0][0]
    
    # Check that redirect was still called
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_commit_different_filename(mock_self, mock_subprocess_run, mock_redirect, mock_url_for, mock_print):
    """Test the commit function with a different filename."""
    # Change the filename in the mock_self
    mock_self.filename = 'different_file.csv'
    
    result = commit(mock_self)
    
    # Check that subprocess.run was called with the correct arguments
    assert mock_subprocess_run.call_count == 3
    mock_subprocess_run.assert_any_call(["git", "add", "/fake/path/different_file.json"], check=True)
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_commit_no_csv_extension(mock_self, mock_subprocess_run, mock_redirect, mock_url_for, mock_print):
    """Test the commit function with a filename that doesn't have a .csv extension."""
    # Change the filename in the mock_self to one without a .csv extension
    mock_self.filename = 'test_file'
    
    result = commit(mock_self)
    
    # Check that subprocess.run was called with the correct arguments
    assert mock_subprocess_run.call_count == 3
    mock_subprocess_run.assert_any_call(["git", "add", "/fake/path/test_file.json"], check=True)
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected' 