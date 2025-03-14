import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

from app.routes.publish import publish


@pytest.fixture
def mock_self():
    """Create a mock self object for the publish function."""
    mock = MagicMock()
    mock.selected = 'test_file'
    mock.data = pd.DataFrame({
        'source_string': ['Source 1', 'Source 2', 'Source 3'],
        'target_string': ['Target 1', 'Target 2', 'Target 3'],
        'style': ['Normal', 'Normal', 'Normal'],
        'annotation': [[], [], []]
    })
    return mock


@pytest.fixture
def mock_get_env_vars():
    """Create a mock for the get_env_vars function."""
    with patch('app.routes.publish.get_env_vars') as mock:
        mock.return_value = {
            'service_account_subject': 'test@example.com'
        }
        yield mock


@pytest.fixture
def mock_publish_to_docs():
    """Create a mock for the publish_to_docs function."""
    with patch('app.routes.publish.publish_to_docs') as mock:
        yield mock


@pytest.fixture
def mock_redirect():
    """Create a mock for the redirect function."""
    with patch('app.routes.publish.redirect') as mock:
        mock.return_value = 'Redirected'
        yield mock


@pytest.fixture
def mock_url_for():
    """Create a mock for the url_for function."""
    with patch('app.routes.publish.url_for') as mock:
        mock.return_value = '/'
        yield mock


def test_publish_basic(mock_self, mock_get_env_vars, mock_publish_to_docs, mock_redirect, mock_url_for):
    """Test the basic functionality of the publish function."""
    result = publish(mock_self)
    
    # Check that get_env_vars was called with the correct arguments
    mock_get_env_vars.assert_called_once_with(
        keys=['google_service_account_subject', 'google_service_account_file'],
        file_name='.env',
        relative_to_pwd='../../../'
    )
    
    # Check that publish_to_docs was called with the correct arguments
    mock_publish_to_docs.assert_called_once_with(
        '../service-account-file.json',
        'test@example.com',
        mock_self.data[['source_string', 'target_string', 'style']].values.tolist(),
        'test_file'
    )
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_publish_different_selected(mock_self, mock_get_env_vars, mock_publish_to_docs, mock_redirect, mock_url_for):
    """Test the publish function with a different selected file."""
    # Change the selected file in the mock_self
    mock_self.selected = 'different_file'
    
    result = publish(mock_self)
    
    # Check that publish_to_docs was called with the correct arguments
    mock_publish_to_docs.assert_called_once_with(
        '../service-account-file.json',
        'test@example.com',
        mock_self.data[['source_string', 'target_string', 'style']].values.tolist(),
        'different_file'
    )
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_publish_different_data(mock_self, mock_get_env_vars, mock_publish_to_docs, mock_redirect, mock_url_for):
    """Test the publish function with different data."""
    # Change the data in the mock_self
    mock_self.data = pd.DataFrame({
        'source_string': ['Different 1', 'Different 2'],
        'target_string': ['Different Target 1', 'Different Target 2'],
        'style': ['Bold', 'Italic'],
        'annotation': [[], []]
    })
    
    result = publish(mock_self)
    
    # Check that publish_to_docs was called with the correct arguments
    mock_publish_to_docs.assert_called_once_with(
        '../service-account-file.json',
        'test@example.com',
        mock_self.data[['source_string', 'target_string', 'style']].values.tolist(),
        'test_file'
    )
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected'


def test_publish_different_env_vars(mock_self, mock_get_env_vars, mock_publish_to_docs, mock_redirect, mock_url_for):
    """Test the publish function with different environment variables."""
    # Change the return value of get_env_vars
    mock_get_env_vars.return_value = {
        'service_account_subject': 'different@example.com'
    }
    
    result = publish(mock_self)
    
    # Check that publish_to_docs was called with the correct arguments
    mock_publish_to_docs.assert_called_once_with(
        '../service-account-file.json',
        'different@example.com',
        mock_self.data[['source_string', 'target_string', 'style']].values.tolist(),
        'test_file'
    )
    
    # Check that redirect was called with the correct arguments
    mock_url_for.assert_called_once_with('index')
    mock_redirect.assert_called_once_with('/')
    
    # Check the return value
    assert result == 'Redirected' 