import os
import pytest
from unittest.mock import patch, mock_open

from app.utils.get_env_vars import get_env_vars


@pytest.fixture
def mock_env_file():
    """Create a mock .env file content."""
    return "TEST_KEY=test_value\nANOTHER_KEY=another_value\n"


def test_get_env_vars_single_key(mock_env_file):
    """Test getting a single environment variable."""
    with patch('os.path.join', return_value='/fake/path'), \
         patch('os.path.abspath', return_value='/fake/path'), \
         patch('builtins.open', mock_open(read_data=mock_env_file)), \
         patch('os.getenv', return_value='test_value'):
        
        # Call the function
        result = get_env_vars(keys=['TEST_KEY'], file_name='.env', relative_to_pwd='../')
        
        # Check the result
        assert result == {'TEST_KEY': 'test_value'}


def test_get_env_vars_multiple_keys(mock_env_file):
    """Test getting multiple environment variables."""
    def mock_getenv(key):
        if key == 'TEST_KEY':
            return 'test_value'
        elif key == 'ANOTHER_KEY':
            return 'another_value'
        return None
    
    with patch('os.path.join', return_value='/fake/path'), \
         patch('os.path.abspath', return_value='/fake/path'), \
         patch('builtins.open', mock_open(read_data=mock_env_file)), \
         patch('os.getenv', side_effect=mock_getenv):
        
        # Call the function
        result = get_env_vars(
            keys=['TEST_KEY', 'ANOTHER_KEY'], 
            file_name='.env', 
            relative_to_pwd='../'
        )
        
        # Check the result
        assert result == {'TEST_KEY': 'test_value', 'ANOTHER_KEY': 'another_value'}


def test_get_env_vars_missing_key(mock_env_file):
    """Test getting a missing environment variable."""
    with patch('os.path.join', return_value='/fake/path'), \
         patch('os.path.abspath', return_value='/fake/path'), \
         patch('builtins.open', mock_open(read_data=mock_env_file)), \
         patch('os.getenv', return_value=None):
        
        # Call the function
        result = get_env_vars(keys=['MISSING_KEY'], file_name='.env', relative_to_pwd='../')
        
        # Check the result
        assert result == {'MISSING_KEY': None}


def test_get_env_vars_different_file(mock_env_file):
    """Test getting environment variables from a different file."""
    with patch('os.path.join', return_value='/fake/path'), \
         patch('os.path.abspath', return_value='/fake/path'), \
         patch('builtins.open', mock_open(read_data=mock_env_file)), \
         patch('os.getenv', return_value='test_value'):
        
        # Call the function
        result = get_env_vars(keys=['TEST_KEY'], file_name='.env.test', relative_to_pwd='../')
        
        # Check the result
        assert result == {'TEST_KEY': 'test_value'} 