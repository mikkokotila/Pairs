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
    delete_entry
)


def test_init_db(tmpdir):
    """Test initializing the database directory."""
    # Create a temporary app instance mock
    class AppMock:
        pass
    
    app_mock = AppMock()
    app_mock.csv_file_path = str(tmpdir)
    
    # Call init_db with the mock app instance
    db_path = init_db(app_mock)
    
    # Check that the database directory was created
    assert os.path.exists(os.path.join(str(tmpdir), "db"))
    assert db_path == "data/db/"


def test_get_db(test_db):
    """Test getting a TinyDB instance."""
    db, db_dir = test_db
    
    # Get a TinyDB instance for a specific file
    test_db_instance = get_db(db_dir, "test")
    
    # Check that the database instance is a TinyDB instance
    assert isinstance(test_db_instance, TinyDB)
    assert test_db_instance.name == os.path.join(db_dir, "test.json")


def test_get_all_entries_empty(test_db):
    """Test getting all entries from an empty database."""
    db, db_dir = test_db
    
    # Get all entries from the empty database
    df = get_all_entries(db_dir, "test")
    
    # Check that the result is a DataFrame with the expected columns
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['source_string', 'target_string', 'style', 'annotation']
    assert len(df) == 0


def test_get_all_entries_with_data(test_db, sample_entries):
    """Test getting all entries from a database with data."""
    db, db_dir = test_db
    
    # Insert sample entries into the database
    db.insert_multiple(sample_entries)
    
    # Get all entries from the database
    df = get_all_entries(db_dir, "test")
    
    # Check that the result is a DataFrame with the expected data
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['source_string', 'target_string', 'style', 'annotation']
    assert len(df) == len(sample_entries)
    assert df.iloc[0]['source_string'] == 'Source 1'
    assert df.iloc[1]['target_string'] == 'Target 2'
    assert df.iloc[2]['style'] == 'Italic'
    assert df.iloc[1]['annotation'] == ['Comment 1']


def test_update_entry(test_db, sample_entries):
    """Test updating an entry in the database."""
    db, db_dir = test_db
    
    # Insert sample entries into the database
    db.insert_multiple(sample_entries)
    
    # Update an entry
    update_entry(db_dir, "test", 1, "target_string", "Updated Target")
    
    # Get all entries from the database
    df = get_all_entries(db_dir, "test")
    
    # Check that the entry was updated
    assert df.iloc[1]['target_string'] == 'Updated Target'


def test_create_entries(test_db, sample_entries):
    """Test creating entries in the database."""
    db, db_dir = test_db
    
    # Create entries in the database
    create_entries(db_dir, "test", sample_entries)
    
    # Get all entries from the database
    df = get_all_entries(db_dir, "test")
    
    # Check that the entries were created
    assert len(df) == len(sample_entries)
    assert df.iloc[0]['source_string'] == 'Source 1'
    assert df.iloc[1]['target_string'] == 'Target 2'
    assert df.iloc[2]['style'] == 'Italic'


def test_delete_entry(test_db, sample_entries):
    """Test deleting an entry from the database."""
    db, db_dir = test_db
    
    # Insert sample entries into the database
    db.insert_multiple(sample_entries)
    
    # Delete an entry
    delete_entry(db_dir, "test", 1)
    
    # Get all entries from the database
    all_docs = db.all()
    
    # Check that the entry was deleted
    assert len(all_docs) == len(sample_entries) - 1
    # The remaining entries should be the first and third sample entries
    assert all_docs[0]['source_string'] == 'Source 1'
    assert all_docs[1]['source_string'] == 'Source 3' 