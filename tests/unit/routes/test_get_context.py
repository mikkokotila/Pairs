import pytest
import pandas as pd
import json
import os
from unittest.mock import patch, MagicMock, mock_open

from app.routes.get_context import get_context


@pytest.fixture
def mock_self():
    """Create a mock self object for the get_context function."""
    mock = MagicMock()
    mock.data = pd.DataFrame({
        'source_string': ['Test string 1', 'Test string 2', 'Test string 3'],
        'target_string': ['Target 1', 'Target 2', 'Target 3'],
        'style': ['Normal', 'Normal', 'Normal'],
        'annotation': [['Annotation 1'], ['Annotation 2'], []]
    })
    mock.selected = 'test_file'
    mock.filename = 'test_file'
    mock.db_path = '/fake/path/'
    return mock


@pytest.fixture
def mock_request():
    """Create a mock for the request object."""
    with patch('app.routes.get_context.request') as mock:
        mock.json = {'row_index': 0}
        yield mock


@pytest.fixture
def mock_jsonify():
    """Create a mock for the jsonify function."""
    with patch('app.routes.get_context.jsonify') as mock:
        mock.return_value = {'result': 'mocked_result', 'has_content': True}
        yield mock


@pytest.fixture
def mock_render_template():
    """Create a mock for the render_template function."""
    with patch('app.routes.get_context.render_template') as mock:
        mock.return_value = '<html>Rendered template</html>'
        yield mock


@pytest.fixture
def mock_get_all_entries():
    """Create a mock for the get_all_entries function."""
    with patch('app.routes.get_context.get_all_entries') as mock:
        mock.return_value = pd.DataFrame({
            'source_string': ['Test string 1', 'Test string 2', 'Test string 3'],
            'target_string': ['Target 1', 'Target 2', 'Target 3'],
            'style': ['Normal', 'Normal', 'Normal'],
            'annotation': [['Annotation 1'], ['Annotation 2'], []]
        })
        yield mock


def test_get_context_basic(mock_self, mock_request, mock_jsonify, mock_render_template):
    """Test the basic functionality of the get_context function."""
    result = get_context(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name, data = mock_render_template.call_args[0][0], mock_render_template.call_args[1]['data']
    assert template_name == 'context_template.html'
    assert 'Annotations' in data
    assert data['Annotations'] == ['Annotation 1']
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({"result": '<html>Rendered template</html>', "has_content": True})
    
    # Check the return value
    assert result == {'result': 'mocked_result', 'has_content': True}


def test_get_context_no_data(mock_self, mock_request, mock_jsonify, mock_render_template, mock_get_all_entries):
    """Test the get_context function when self.data is not available."""
    # Remove the data attribute
    delattr(mock_self, 'data')
    
    # Mock os.listdir to return a list of files
    with patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = ['test_file.json', 'glossary.json']
        
        # Mock os.path.isfile to return True for all files
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            
            result = get_context(mock_self)
            
            # Check that get_all_entries was called
            mock_get_all_entries.assert_called_once_with('/fake/path/', 'test_file')
            
            # Check that render_template was called
            mock_render_template.assert_called_once()
            
            # Check that jsonify was called
            mock_jsonify.assert_called_once()


def test_get_context_no_selected(mock_self, mock_request, mock_jsonify, mock_render_template, mock_get_all_entries):
    """Test the get_context function when self.selected is not available."""
    # Remove the selected attribute
    delattr(mock_self, 'selected')
    
    # Remove the data attribute
    delattr(mock_self, 'data')
    
    # Mock os.listdir to return a list of files
    with patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = ['test_file.json', 'glossary.json']
        
        # Mock os.path.isfile to return True for all files
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            
            result = get_context(mock_self)
            
            # Check that mock_self.all_files was set correctly
            assert mock_self.all_files == ['test_file']
            
            # Check that mock_self.selected was set to the first file
            assert mock_self.selected == 'test_file'
            
            # Check that get_all_entries was called
            mock_get_all_entries.assert_called_once_with('/fake/path/', 'test_file')
            
            # Check that render_template was called
            mock_render_template.assert_called_once()
            
            # Check that jsonify was called
            mock_jsonify.assert_called_once()


def test_get_context_invalid_row_index(mock_self, mock_request, mock_jsonify):
    """Test the get_context function with an invalid row index."""
    # Set the row_index to a value that's out of range
    mock_request.json = {'row_index': 10}
    
    result = get_context(mock_self)
    
    # Check that jsonify was called with the correct arguments
    mock_jsonify.assert_called_once_with({"result": "", "has_content": False})


def test_get_context_annotation_list(mock_self, mock_request, mock_jsonify, mock_render_template):
    """Test the get_context function with an annotation that's a list."""
    # Set the row_index to a row with a non-empty list annotation
    mock_request.json = {'row_index': 0}
    
    result = get_context(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name, data = mock_render_template.call_args[0][0], mock_render_template.call_args[1]['data']
    assert template_name == 'context_template.html'
    assert 'Annotations' in data
    assert data['Annotations'] == ['Annotation 1']


def test_get_context_annotation_empty_list(mock_self, mock_request, mock_jsonify, mock_render_template):
    """Test the get_context function with an annotation that's an empty list."""
    # Set the row_index to a row with an empty list annotation
    mock_request.json = {'row_index': 2}
    
    result = get_context(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name, data = mock_render_template.call_args[0][0], mock_render_template.call_args[1]['data']
    assert template_name == 'context_template.html'
    assert 'Annotations' in data
    assert data['Annotations'] == "<span class='no-annotations-text'>No annotations for this row</span>"


def test_get_context_annotation_string(mock_self, mock_request, mock_jsonify, mock_render_template):
    """Test the get_context function with an annotation that's a string."""
    # Change the annotation for row 0 to a string
    mock_self.data.at[0, 'annotation'] = 'String annotation'
    
    # Set the row_index to a row with a string annotation
    mock_request.json = {'row_index': 0}
    
    result = get_context(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name, data = mock_render_template.call_args[0][0], mock_render_template.call_args[1]['data']
    assert template_name == 'context_template.html'
    assert 'Annotations' in data
    assert data['Annotations'] == 'String annotation'


def test_get_context_annotation_none(mock_self, mock_request, mock_jsonify, mock_render_template):
    """Test the get_context function with an annotation that's None."""
    # Change the annotation for row 0 to None
    mock_self.data.at[0, 'annotation'] = None
    
    # Set the row_index to a row with a None annotation
    mock_request.json = {'row_index': 0}
    
    result = get_context(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name, data = mock_render_template.call_args[0][0], mock_render_template.call_args[1]['data']
    assert template_name == 'context_template.html'
    assert 'Annotations' in data
    assert data['Annotations'] == "<span class='no-annotations-text'>No annotations for this row</span>"


def test_get_context_no_annotation_column(mock_self, mock_request, mock_jsonify, mock_render_template):
    """Test the get_context function when there's no annotation column."""
    # Remove the annotation column
    mock_self.data = mock_self.data.drop(columns=['annotation'])
    
    result = get_context(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name, data = mock_render_template.call_args[0][0], mock_render_template.call_args[1]['data']
    assert template_name == 'context_template.html'
    assert 'Annotations' in data
    assert data['Annotations'] == "<span class='no-annotations-text'>No annotations for this row</span>"


def test_get_context_exception(mock_self, mock_request, mock_jsonify):
    """Test the get_context function when an exception is raised."""
    # Make request.json.get raise an exception
    mock_request.json.get.side_effect = Exception('Test exception')
    
    # Mock traceback.print_exc to avoid printing the traceback
    with patch('traceback.print_exc'):
        result = get_context(mock_self)
        
        # Check that jsonify was called with the correct arguments
        mock_jsonify.assert_called_once_with({"result": "Error: Test exception", "has_content": False}) 