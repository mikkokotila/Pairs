import os
import pytest
import pandas as pd
from unittest.mock import patch, mock_open

from app.utils.read_csv import read_csv


@pytest.fixture
def mock_csv_content():
    """Create a mock CSV file content."""
    return "source_string,target_string,style,annotation\nSource 1,Target 1,Normal,[]\nSource 2,Target 2,Bold,[Note 1]"


def test_read_csv_file_exists(mock_csv_content):
    """Test reading a CSV file that exists."""
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=pd.DataFrame({
             'source_string': ['Source 1', 'Source 2'],
             'target_string': ['Target 1', 'Target 2'],
             'style': ['Normal', 'Bold'],
             'annotation': [[], ['Note 1']]
         })):
        
        # Call the function
        result = read_csv('test.csv')
        
        # Check the result
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['source_string', 'target_string', 'style', 'annotation']
        assert len(result) == 2
        assert result['source_string'].tolist() == ['Source 1', 'Source 2']
        assert result['target_string'].tolist() == ['Target 1', 'Target 2']
        assert result['style'].tolist() == ['Normal', 'Bold']
        assert result['annotation'].tolist() == [[], ['Note 1']]


def test_read_csv_file_not_exists():
    """Test reading a CSV file that doesn't exist."""
    with patch('os.path.exists', return_value=False):
        
        # Call the function
        result = read_csv('nonexistent.csv')
        
        # Check the result
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['source_string', 'target_string', 'style', 'annotation']
        assert result.empty


def test_read_csv_with_path():
    """Test reading a CSV file with a path."""
    with patch('os.path.exists', return_value=True), \
         patch('pandas.read_csv', return_value=pd.DataFrame({
             'source_string': ['Source 1'],
             'target_string': ['Target 1'],
             'style': ['Normal'],
             'annotation': [[]]
         })):
        
        # Call the function
        result = read_csv('/path/to/test.csv')
        
        # Check the result
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ['source_string', 'target_string', 'style', 'annotation']
        assert len(result) == 1 