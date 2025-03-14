import os
import pytest
import pandas as pd
from tinydb import TinyDB

from app.utils.db_operations import (
    init_db,
    get_db,
    get_all_entries,
    update_entry,
    create_entries,
    delete_entry,
    csv_to_tinydb
)


@pytest.fixture
def temp_db_path(tmpdir):
    """Create a temporary database path for testing."""
    db_path = os.path.join(tmpdir, "db/")
    os.makedirs(db_path, exist_ok=True)
    return db_path


@pytest.fixture
def mock_app_instance():
    """Create a mock app instance for testing."""
    class MockApp:
        def __init__(self):
            self.db_path = None
    
    return MockApp()


def test_init_db(mock_app_instance, tmpdir):
    """Test initializing the database."""
    # Set up a temporary path for the app instance
    mock_app_instance.db_path = os.path.join(tmpdir, "data/")
    
    # Call init_db
    result = init_db(mock_app_instance)
    
    # Check that the database directory was created
    assert os.path.exists(os.path.join(tmpdir, "data/db/"))
    assert result == "data/db/"


def test_get_db(temp_db_path):
    """Test getting a database instance."""
    # Test with filename without extension
    db1 = get_db(temp_db_path, "test_db")
    assert isinstance(db1, TinyDB)
    assert db1.name == f"{temp_db_path}test_db.json"
    
    # Test with filename with extension
    db2 = get_db(temp_db_path, "test_db.json")
    assert isinstance(db2, TinyDB)
    assert db2.name == f"{temp_db_path}test_db.json"


def test_get_all_entries_empty(temp_db_path):
    """Test getting all entries from an empty database."""
    # Create an empty database
    db_name = "empty_db"
    
    # Get all entries
    df = get_all_entries(temp_db_path, db_name)
    
    # Check that an empty DataFrame with the correct columns was returned
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert list(df.columns) == ['source_string', 'target_string', 'style', 'annotation']


def test_get_all_entries_with_data(temp_db_path):
    """Test getting all entries from a database with data."""
    # Create a database with data
    db_name = "test_db"
    db = get_db(temp_db_path, db_name)
    
    # Add some test data
    test_data = [
        {'source_string': 'Source 1', 'target_string': 'Target 1', 'style': 'Normal', 'annotation': []},
        {'source_string': 'Source 2', 'target_string': 'Target 2', 'style': 'Bold', 'annotation': ['Note 1']},
        {'source_string': 'Source 3', 'target_string': 'Target 3', 'style': 'Italic', 'annotation': ['Note 2', 'Note 3']}
    ]
    db.insert_multiple(test_data)
    
    # Get all entries
    df = get_all_entries(temp_db_path, db_name)
    
    # Check that the DataFrame has the correct data
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ['source_string', 'target_string', 'style', 'annotation']
    assert df['source_string'].tolist() == ['Source 1', 'Source 2', 'Source 3']
    assert df['target_string'].tolist() == ['Target 1', 'Target 2', 'Target 3']
    assert df['style'].tolist() == ['Normal', 'Bold', 'Italic']
    assert df['annotation'].tolist() == [[], ['Note 1'], ['Note 2', 'Note 3']]


def test_update_entry(temp_db_path):
    """Test updating an entry in the database."""
    # Create a database with data
    db_name = "test_db"
    db = get_db(temp_db_path, db_name)
    
    # Add some test data
    test_data = [
        {'source_string': 'Source 1', 'target_string': 'Target 1', 'style': 'Normal', 'annotation': []},
        {'source_string': 'Source 2', 'target_string': 'Target 2', 'style': 'Bold', 'annotation': ['Note 1']}
    ]
    db.insert_multiple(test_data)
    
    # Update an entry
    update_entry(temp_db_path, db_name, 0, 'target_string', 'Updated Target 1')
    
    # Get all entries
    df = get_all_entries(temp_db_path, db_name)
    
    # Check that the entry was updated
    assert df['target_string'].iloc[0] == 'Updated Target 1'


def test_update_entry_invalid_index(temp_db_path, capsys):
    """Test updating an entry with an invalid index."""
    # Create a database with data
    db_name = "test_db"
    db = get_db(temp_db_path, db_name)
    
    # Add some test data
    test_data = [
        {'source_string': 'Source 1', 'target_string': 'Target 1', 'style': 'Normal', 'annotation': []}
    ]
    db.insert_multiple(test_data)
    
    # Update an entry with an invalid index
    update_entry(temp_db_path, db_name, 10, 'target_string', 'Updated Target')
    
    # Check that a warning was printed
    captured = capsys.readouterr()
    assert "Warning: Index 10 out of range" in captured.out


def test_update_entry_empty_db(temp_db_path, capsys):
    """Test updating an entry in an empty database."""
    # Create an empty database
    db_name = "empty_db"
    
    # Update an entry
    update_entry(temp_db_path, db_name, 0, 'target_string', 'Updated Target')
    
    # Check that a warning was printed
    captured = capsys.readouterr()
    assert "Warning: No documents found in database" in captured.out


def test_create_entries(temp_db_path):
    """Test creating entries in the database."""
    # Create a database
    db_name = "test_db"
    
    # Create entries
    test_data = [
        {'source_string': 'Source 1', 'target_string': 'Target 1', 'style': 'Normal', 'annotation': []},
        {'source_string': 'Source 2', 'target_string': 'Target 2', 'style': 'Bold', 'annotation': ['Note 1']}
    ]
    create_entries(temp_db_path, db_name, test_data)
    
    # Get all entries
    df = get_all_entries(temp_db_path, db_name)
    
    # Check that the entries were created
    assert len(df) == 2
    assert df['source_string'].tolist() == ['Source 1', 'Source 2']
    assert df['target_string'].tolist() == ['Target 1', 'Target 2']
    assert df['style'].tolist() == ['Normal', 'Bold']
    assert df['annotation'].tolist() == [[], ['Note 1']]


def test_delete_entry(temp_db_path):
    """Test deleting an entry from the database."""
    # Create a database with data
    db_name = "test_db"
    db = get_db(temp_db_path, db_name)
    
    # Add some test data
    test_data = [
        {'source_string': 'Source 1', 'target_string': 'Target 1', 'style': 'Normal', 'annotation': []},
        {'source_string': 'Source 2', 'target_string': 'Target 2', 'style': 'Bold', 'annotation': ['Note 1']}
    ]
    db.insert_multiple(test_data)
    
    # Delete an entry
    delete_entry(temp_db_path, db_name, 0)
    
    # Get all entries
    df = get_all_entries(temp_db_path, db_name)
    
    # Check that the entry was deleted
    assert len(df) == 1
    assert df['source_string'].iloc[0] == 'Source 2'


def test_csv_to_tinydb(temp_db_path, tmpdir):
    """Test converting a CSV file to TinyDB format."""
    # This is a placeholder test since the function is not implemented
    # Create a CSV file
    csv_path = os.path.join(tmpdir, "test.csv")
    
    # Call the function
    csv_to_tinydb(csv_path, temp_db_path, "test_db")
    
    # Since the function is a placeholder, we just check that it doesn't raise an exception
    assert True 