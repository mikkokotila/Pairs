import json
import pytest
from flask import url_for


def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_new_route(client):
    """Test the new route."""
    response = client.get('/new')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_translate_route(client):
    """Test the translate route."""
    response = client.get('/translate')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_review_route(client):
    """Test the review route."""
    response = client.get('/review')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_commit_route(client):
    """Test the commit route."""
    response = client.get('/commit')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_publish_route(client):
    """Test the publish route."""
    response = client.get('/publish')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data


def test_glossary_route(client):
    """Test the glossary route."""
    response = client.post('/glossary', data={'search_term': 'test'})
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_research_keyword_route(client):
    """Test the research keyword route."""
    response = client.post('/research-keyword', 
                          data=json.dumps({'text': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_suggest_translation_route(client):
    """Test the suggest translation route."""
    response = client.post('/suggest-translation', 
                          data=json.dumps({'text': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_lookup_glossary_route(client):
    """Test the lookup glossary route."""
    response = client.post('/lookup-glossary', 
                          data=json.dumps({'text': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_find_examples_route(client):
    """Test the find examples route."""
    response = client.post('/find-examples', 
                          data=json.dumps({'text': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_explain_grammar_route(client):
    """Test the explain grammar route."""
    response = client.post('/explain-grammar', 
                          data=json.dumps({'text': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_history_route(client):
    """Test the history route."""
    response = client.get('/history?direction=back')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data


def test_get_context_route(client):
    """Test the get context route."""
    response = client.post('/get-context', 
                          data=json.dumps({'row_index': 0}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'has_content' in data


def test_autosave_route(client):
    """Test the autosave route."""
    response = client.post('/autosave', 
                          data=json.dumps({'row': 0, 'content': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data


def test_create_text_route(client):
    """Test the create text route."""
    response = client.post('/create-text', 
                          data=json.dumps({'title': 'Test', 'content': 'Test content'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'success' in data


def test_fetch_lotsawa_route(client):
    """Test the fetch lotsawa route."""
    response = client.post('/fetch-lotsawa', 
                          data=json.dumps({'text': 'test'}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = json.loads(response.data)
    assert 'result' in data 