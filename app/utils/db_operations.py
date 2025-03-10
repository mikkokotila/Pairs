import os
from tinydb import TinyDB, Query
import pandas as pd

def init_db(app_instance):
    """Initialize the TinyDB database directory if it doesn't exist"""
    db_path = "data/db/"
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    return db_path

def get_db(db_path, filename):
    """Get a TinyDB instance for a specific file"""
    if not filename.endswith('.json'):
        filename = f"{filename}.json"
    return TinyDB(f"{db_path}{filename}")

def get_all_entries(db_path, filename):
    """Get all entries from a specific database file
    
    Returns:
        DataFrame: Pandas DataFrame with columns for source_string, target_string, style, and annotation
    """
    db = get_db(db_path, filename)
    data = db.all()
    
    # Create empty dataframe if no data exists
    if not data:
        return pd.DataFrame(columns=['source_string', 'target_string', 'style', 'annotation'])
    
    # Convert to pandas DataFrame for compatibility with existing code
    df = pd.DataFrame([
        {
            'source_string': item.get('source_string', ''),
            'target_string': item.get('target_string', ''),
            'style': item.get('style', 'Normal'),
            'annotation': item.get('annotation', [])
        }
        for item in data
    ])
    
    return df

def update_entry(db_path, filename, index, field, content):
    """Update a specific field of an entry
    
    Args:
        db_path: Path to the database directory
        filename: Name of the file (without extension)
        index: Index of the entry to update
        field: Field to update ('source_string', 'target_string', 'style', or 'annotation')
        content: New content for the field
    """
    db = get_db(db_path, filename)
    all_docs = db.all()
    
    if not all_docs:
        print(f"Warning: No documents found in database {filename}")
        return
    
    if index >= len(all_docs):
        print(f"Warning: Index {index} out of range for database {filename} with {len(all_docs)} entries")
        return
    
    # Get the actual document ID (might not be sequential)
    doc_id = db.all()[index].doc_id
    print(f"Updating document with ID {doc_id} at index {index} for field {field}")
    
    # Update the document with the correct ID
    result = db.update({field: content}, doc_ids=[doc_id])
    print(f"Update result: {result}")

def create_entries(db_path, filename, entries):
    """Create new entries in the database
    
    Args:
        db_path: Path to the database directory
        filename: Name of the file (without extension)
        entries: List of dictionaries with 'source_string', 'target_string', 'style', and 'annotation' keys
    """
    db = get_db(db_path, filename)
    
    # Insert all entries
    db.insert_multiple(entries)
    
def delete_entry(db_path, filename, index):
    """Delete an entry from the database
    
    Args:
        db_path: Path to the database directory
        filename: Name of the file (without extension)
        index: Index of the entry to delete
    """
    db = get_db(db_path, filename)
    db.remove(doc_ids=[index + 1])  # TinyDB doc_ids start at 1

def csv_to_tinydb(csv_path, db_path, filename):
    """Convert an existing CSV file to TinyDB format
    
    Args:
        csv_path: Path to the CSV file
        db_path: Path to the database directory
        filename: Name of the file (without extension)
    """
    # This function is for migration purposes if needed
    # For this task, we're not migrating existing data
    pass 