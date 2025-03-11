from flask import request, jsonify
import requests
from bs4 import BeautifulSoup

def fetch_lotsawa(self):
    """
    Fetches Tibetan text content from a Lotsawa House URL.
    
    Expected POST parameters:
    - url: The Lotsawa House URL to fetch content from
    
    Returns:
    - JSON response with the fetched content or error message
    """
    try:
        # Get URL from request
        data = request.get_json()
        url = data.get('url', '').strip()
        
        # Validate URL
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400
            
        if 'lotsawahouse.org/bo/' not in url:
            return jsonify({'status': 'error', 'message': 'Only Lotsawa House Tibetan texts are supported'}), 400
        
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the element with id="maintext"
        main_text_element = soup.find(id='maintext')
        
        if not main_text_element:
            return jsonify({'status': 'error', 'message': 'Could not find the main text content on the page'}), 404
        
        # Extract the text content
        content = main_text_element.get_text('\n', strip=True)
        
        if not content:
            return jsonify({'status': 'error', 'message': 'No content found on the page'}), 404
        
        return jsonify({
            'status': 'success',
            'content': content
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'error', 'message': f'Error fetching content: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500 