import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock

from app.routes.index import index


@pytest.fixture
def mock_self():
    """Create a mock self object for the index function."""
    mock = MagicMock()
    mock.db_path = '/fake/path/'
    mock.all_files = ['file1', 'file2', 'file3']
    mock.selected = 'file1'
    mock.data = pd.DataFrame({
        'source_string': ['Source 1', 'Source 2', 'Source 3'],
        'target_string': ['Target 1', 'Target 2', 'Target 3'],
        'style': ['Normal', 'Normal', 'Normal'],
        'annotation': [[], [], []]
    })
    return mock


@pytest.fixture
def mock_render_template():
    """Create a mock for the render_template function."""
    with patch('app.routes.index.render_template') as mock:
        mock.return_value = '<html>Rendered template</html>'
        yield mock


@pytest.fixture
def mock_request():
    """Create a mock for the request object."""
    with patch('app.routes.index.request') as mock:
        mock.method = 'GET'
        mock.form = {}
        yield mock


@pytest.fixture
def mock_session():
    """Create a mock for the session object."""
    with patch('app.routes.index.session') as mock:
        mock.get.return_value = None
        yield mock


@pytest.fixture
def mock_get_all_entries():
    """Create a mock for the get_all_entries function."""
    with patch('app.routes.index.get_all_entries') as mock:
        mock.return_value = pd.DataFrame({
            'source_string': ['Source 1', 'Source 2', 'Source 3'],
            'target_string': ['Target 1', 'Target 2', 'Target 3'],
            'style': ['Normal', 'Normal', 'Normal'],
            'annotation': [[], [], []]
        })
        yield mock


def test_index_get_basic(mock_self, mock_render_template, mock_request, mock_session):
    """Test the basic GET functionality of the index function."""
    result = index(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name = mock_render_template.call_args[0][0]
    assert template_name == 'index.html'
    
    # Check the template context
    context = mock_render_template.call_args[1]
    assert context['files'] == ['file1', 'file2', 'file3']
    assert context['selected'] == 'file1'
    assert isinstance(context['data'], pd.DataFrame)
    assert len(context['data']) == 3
    
    # Check the return value
    assert result == '<html>Rendered template</html>'


def test_index_get_no_files(mock_self, mock_render_template, mock_request, mock_session):
    """Test the index function when there are no files."""
    # Set all_files to an empty list
    mock_self.all_files = []
    mock_self.selected = None
    mock_self.data = None
    
    result = index(mock_self)
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name = mock_render_template.call_args[0][0]
    assert template_name == 'index.html'
    
    # Check the template context
    context = mock_render_template.call_args[1]
    assert context['files'] == []
    assert context['selected'] is None
    assert context['data'] is None


def test_index_get_with_session_selected(mock_self, mock_render_template, mock_request, mock_session, mock_get_all_entries):
    """Test the index function when there's a selected file in the session."""
    # Set up the session to return a selected file
    mock_session.get.return_value = 'file2'
    
    result = index(mock_self)
    
    # Check that the selected file was updated
    assert mock_self.selected == 'file2'
    
    # Check that get_all_entries was called with the correct arguments
    mock_get_all_entries.assert_called_once_with('/fake/path/', 'file2')
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name = mock_render_template.call_args[0][0]
    assert template_name == 'index.html'
    
    # Check the template context
    context = mock_render_template.call_args[1]
    assert context['selected'] == 'file2'


def test_index_post_select_file(mock_self, mock_render_template, mock_request, mock_session, mock_get_all_entries):
    """Test the index function when a file is selected via POST."""
    # Set up the request as a POST with a selected file
    mock_request.method = 'POST'
    mock_request.form = {'selected': 'file3'}
    
    result = index(mock_self)
    
    # Check that the selected file was updated
    assert mock_self.selected == 'file3'
    
    # Check that get_all_entries was called with the correct arguments
    mock_get_all_entries.assert_called_once_with('/fake/path/', 'file3')
    
    # Check that the session was updated
    mock_session.__setitem__.assert_called_once_with('selected_file', 'file3')
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name = mock_render_template.call_args[0][0]
    assert template_name == 'index.html'
    
    # Check the template context
    context = mock_render_template.call_args[1]
    assert context['selected'] == 'file3'


def test_index_post_no_selection(mock_self, mock_render_template, mock_request, mock_session):
    """Test the index function when POST is used but no file is selected."""
    # Set up the request as a POST with no selected file
    mock_request.method = 'POST'
    mock_request.form = {}
    
    result = index(mock_self)
    
    # Check that the selected file was not updated
    assert mock_self.selected == 'file1'
    
    # Check that render_template was called with the correct arguments
    mock_render_template.assert_called_once()
    template_name = mock_render_template.call_args[0][0]
    assert template_name == 'index.html'
    
    # Check the template context
    context = mock_render_template.call_args[1]
    assert context['selected'] == 'file1'


def test_index_first_load(mock_self, mock_render_template, mock_request, mock_session):
    """Test the index function on first load when no files have been loaded yet."""
    # Remove attributes that would be set during normal operation
    delattr(mock_self, 'all_files')
    delattr(mock_self, 'selected')
    delattr(mock_self, 'data')
    
    # Mock os.listdir to return a list of files
    with patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = ['file1.json', 'file2.json', 'glossary.json']
        
        # Mock os.path.isfile to return True for all files
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            
            result = index(mock_self)
            
            # Check that the attributes were set correctly
            assert mock_self.all_files == ['file1', 'file2']
            assert mock_self.selected == 'file1'
            
            # Check that render_template was called with the correct arguments
            mock_render_template.assert_called_once()
            template_name = mock_render_template.call_args[0][0]
            assert template_name == 'index.html'


def test_index_no_db_files(mock_self, mock_render_template, mock_request, mock_session):
    """Test the index function when there are no database files."""
    # Remove attributes that would be set during normal operation
    delattr(mock_self, 'all_files')
    delattr(mock_self, 'selected')
    delattr(mock_self, 'data')
    
    # Mock os.listdir to return an empty list
    with patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = []
        
        result = index(mock_self)
        
        # Check that the attributes were set correctly
        assert mock_self.all_files == []
        assert mock_self.selected is None
        assert mock_self.data is None
        
        # Check that render_template was called with the correct arguments
        mock_render_template.assert_called_once()
        template_name = mock_render_template.call_args[0][0]
        assert template_name == 'index.html'
        
        # Check the template context
        context = mock_render_template.call_args[1]
        assert context['files'] == []
        assert context['selected'] is None
        assert context['data'] is None 