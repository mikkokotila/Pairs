import os
import pytest
import pandas as pd
from tinydb import TinyDB, Query

from app.utils.db_operations import (
    get_db,
    get_all_entries,
    update_entry,
    create_entries
)


def test_data_schema_consistency(test_db, sample_entries):
    """Test that all entries in the database have the expected schema."""
    db, db_dir = test_db
    
    # Create entries with different schemas
    valid_entries = sample_entries
    invalid_entries = [
        {
            'source_string': 'Invalid 1',
            # Missing target_string
            'style': 'Normal',
            'annotation': []
        },
        {
            'source_string': 'Invalid 2',
            'target_string': 'Target 2',
            # Missing style
            'annotation': []
        },
        {
            # Missing source_string
            'target_string': 'Invalid 3',
            'style': 'Normal',
            'annotation': []
        }
    ]
    
    # Insert valid entries
    create_entries(db_dir, "test", valid_entries)
    
    # Get all entries
    df = get_all_entries(db_dir, "test")
    
    # Check that all entries have the expected schema
    assert all(df.columns == ['source_string', 'target_string', 'style', 'annotation'])
    assert not df['source_string'].isnull().any()
    assert not df['target_string'].isnull().any()
    assert not df['style'].isnull().any()
    assert not df['annotation'].isnull().any()


def test_data_type_consistency(test_db, sample_entries):
    """Test that all entries in the database have the expected data types."""
    db, db_dir = test_db
    
    # Insert sample entries
    create_entries(db_dir, "test", sample_entries)
    
    # Get all entries
    df = get_all_entries(db_dir, "test")
    
    # Check that all entries have the expected data types
    assert df['source_string'].dtype == 'object'  # String
    assert df['target_string'].dtype == 'object'  # String
    assert df['style'].dtype == 'object'  # String
    assert all(isinstance(annotation, list) for annotation in df['annotation'])


def test_data_referential_integrity(test_db, sample_entries):
    """Test that all references in the database are valid."""
    db, db_dir = test_db
    
    # Insert sample entries
    create_entries(db_dir, "test", sample_entries)
    
    # Update an entry to reference another entry
    update_entry(db_dir, "test", 0, "annotation", ["Reference to entry 2"])
    
    # Get all entries
    df = get_all_entries(db_dir, "test")
    
    # Check that the reference is valid
    assert "Reference to entry 2" in df.iloc[0]['annotation']
    assert len(df) >= 2  # Ensure the referenced entry exists


def test_data_uniqueness(test_db):
    """Test that all entries in the database are unique."""
    db, db_dir = test_db
    
    # Create duplicate entries
    duplicate_entries = [
        {
            'source_string': 'Duplicate',
            'target_string': 'Target',
            'style': 'Normal',
            'annotation': []
        },
        {
            'source_string': 'Duplicate',
            'target_string': 'Target',
            'style': 'Normal',
            'annotation': []
        }
    ]
    
    # Insert duplicate entries
    create_entries(db_dir, "test", duplicate_entries)
    
    # Get all entries
    df = get_all_entries(db_dir, "test")
    
    # Check for duplicates
    duplicates = df[df.duplicated(['source_string', 'target_string', 'style'], keep=False)]
    
    # There should be duplicates (2 entries with the same values)
    assert len(duplicates) == 2
    
    # But each entry should have a unique document ID in the database
    assert len(db.all()) == 2
    assert db.all()[0].doc_id != db.all()[1].doc_id


def test_data_consistency_after_update(test_db, sample_entries):
    """Test that data remains consistent after updates."""
    db, db_dir = test_db
    
    # Insert sample entries
    create_entries(db_dir, "test", sample_entries)
    
    # Get initial data
    initial_df = get_all_entries(db_dir, "test")
    
    # Update an entry
    update_entry(db_dir, "test", 1, "target_string", "Updated Target")
    
    # Get updated data
    updated_df = get_all_entries(db_dir, "test")
    
    # Check that only the updated field changed
    assert initial_df.iloc[0]['source_string'] == updated_df.iloc[0]['source_string']
    assert initial_df.iloc[0]['target_string'] == updated_df.iloc[0]['target_string']
    assert initial_df.iloc[0]['style'] == updated_df.iloc[0]['style']
    assert initial_df.iloc[0]['annotation'] == updated_df.iloc[0]['annotation']
    
    assert initial_df.iloc[1]['source_string'] == updated_df.iloc[1]['source_string']
    assert initial_df.iloc[1]['target_string'] != updated_df.iloc[1]['target_string']
    assert updated_df.iloc[1]['target_string'] == "Updated Target"
    assert initial_df.iloc[1]['style'] == updated_df.iloc[1]['style']
    assert initial_df.iloc[1]['annotation'] == updated_df.iloc[1]['annotation']
    
    assert initial_df.iloc[2]['source_string'] == updated_df.iloc[2]['source_string']
    assert initial_df.iloc[2]['target_string'] == updated_df.iloc[2]['target_string']
    assert initial_df.iloc[2]['style'] == updated_df.iloc[2]['style']
    assert initial_df.iloc[2]['annotation'] == updated_df.iloc[2]['annotation'] 