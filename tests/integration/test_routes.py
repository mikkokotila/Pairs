import json
import pytest
from flask import url_for
from unittest.mock import patch


def test_index_route(client):
    """Test the index route."""
    # Test GET request
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'<title>' in response.data
    
    # Test POST request
    response = client.post('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_new_route(client):
    """Test the new route."""
    # Test GET request
    response = client.get('/new')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'<title>' in response.data
    
    # Test POST request
    response = client.post('/new')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_translate_route(client):
    """Test the translate route."""
    # Test GET request
    response = client.get('/translate')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'<title>' in response.data
    
    # Test POST request
    response = client.post('/translate')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_review_route(client):
    """Test the review route."""
    # Test GET request
    response = client.get('/review')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'<title>' in response.data
    
    # Test POST request
    response = client.post('/review')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_commit_route(client):
    """Test the commit route."""
    # Test GET request
    response = client.get('/commit')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    
    # Test with query parameters
    with patch('app.routes.commit.subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        response = client.get('/commit?message=Test%20commit')
        assert response.status_code == 302  # Redirect
        assert response.headers['Location'] == '/'
        mock_run.assert_called()


def test_publish_route(client):
    """Test the publish route."""
    # Test GET request
    response = client.get('/publish')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    
    # Test with query parameters
    with patch('app.routes.publish.subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        response = client.get('/publish?message=Test%20publish')
        assert response.status_code == 302  # Redirect
        assert response.headers['Location'] == '/'
        mock_run.assert_called()


def test_glossary_route(client):
    """Test the glossary route."""
    # Test POST request with form data
    response = client.post('/glossary', data={'search_term': 'test'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test POST request with JSON data
    response = client.post('/glossary', 
                          json={'search_term': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with empty search term
    response = client.post('/glossary', data={'search_term': ''})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_research_keyword_route(client):
    """Test the research keyword route."""
    # Test POST request with JSON data
    response = client.post('/research-keyword', 
                          json={'text': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with empty text
    response = client.post('/research-keyword', 
                          json={'text': ''},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_suggest_translation_route(client):
    """Test the suggest translation route."""
    # Test POST request with JSON data
    response = client.post('/suggest-translation', 
                          json={'text': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with empty text
    response = client.post('/suggest-translation', 
                          json={'text': ''},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with mocked auto_translate
    with patch('app.routes.suggest_translation.auto_translate') as mock_translate:
        mock_translate.return_value = "Mocked translation"
        response = client.post('/suggest-translation', 
                              json={'text': 'test'},
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == "Mocked translation"
        mock_translate.assert_called_once()


def test_lookup_glossary_route(client):
    """Test the lookup glossary route."""
    # Test POST request with JSON data
    response = client.post('/lookup-glossary', 
                          json={'text': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with empty text
    response = client.post('/lookup-glossary', 
                          json={'text': ''},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_find_examples_route(client):
    """Test the find examples route."""
    # Test POST request with JSON data
    response = client.post('/find-examples', 
                          json={'text': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with empty text
    response = client.post('/find-examples', 
                          json={'text': ''},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_explain_grammar_route(client):
    """Test the explain grammar route."""
    # Test POST request with JSON data
    response = client.post('/explain-grammar', 
                          json={'text': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with empty text
    response = client.post('/explain-grammar', 
                          json={'text': ''},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with mocked explain_grammar
    with patch('app.routes.explain_grammar.explain_grammar_model') as mock_explain:
        mock_explain.return_value = "Mocked grammar explanation"
        response = client.post('/explain-grammar', 
                              json={'text': 'test'},
                              content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['result'] == "Mocked grammar explanation"
        mock_explain.assert_called_once()


def test_history_route(client):
    """Test the history route."""
    # Test GET request with direction parameter
    response = client.get('/history?direction=back')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with forward direction
    response = client.get('/history?direction=forward')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test without direction parameter
    response = client.get('/history')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_get_context_route(client):
    """Test the get context route."""
    # Test POST request with JSON data
    response = client.post('/get-context', 
                          json={'row_index': 0},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'has_content' in data
    
    # Test with invalid row index
    response = client.post('/get-context', 
                          json={'row_index': -1},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'has_content' in data
    
    # Test with missing row index
    response = client.post('/get-context', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'has_content' in data


def test_autosave_route(client):
    """Test the autosave route."""
    # Test POST request with JSON data
    response = client.post('/autosave', 
                          json={'row': 0, 'content': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data
    
    # Test with invalid row
    response = client.post('/autosave', 
                          json={'row': -1, 'content': 'test'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data
    
    # Test with missing parameters
    response = client.post('/autosave', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data


def test_create_text_route(client):
    """Test the create text route."""
    # Test POST request with JSON data
    response = client.post('/create-text', 
                          json={'title': 'Test', 'content': 'Test content'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data
    
    # Test with empty title
    response = client.post('/create-text', 
                          json={'title': '', 'content': 'Test content'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data
    
    # Test with empty content
    response = client.post('/create-text', 
                          json={'title': 'Test', 'content': ''},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data
    
    # Test with missing parameters
    response = client.post('/create-text', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data


def test_fetch_lotsawa_route(client):
    """Test the fetch lotsawa route."""
    # Test POST request with JSON data
    with patch('app.routes.fetch_lotsawa.requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = "<html><body><div class='tibetan'>Test Tibetan</div><div class='english'>Test English</div></body></html>"
        
        response = client.post('/fetch-lotsawa', 
                              json={'url': 'https://example.com/test'},
                              content_type='application/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'result' in data
        mock_get.assert_called_once()
    
    # Test with invalid URL
    response = client.post('/fetch-lotsawa', 
                          json={'url': 'invalid-url'},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data
    
    # Test with missing URL
    response = client.post('/fetch-lotsawa', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data 