from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import html

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
        
        # Fetch the content from the URL with explicit encoding
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # Explicitly set encoding to UTF-8
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the element with id="maintext"
        main_text_element = soup.find(id='maintext')
        
        if not main_text_element:
            return jsonify({'status': 'error', 'message': 'Could not find the main text content on the page'}), 404
        
        # Try multiple methods to extract the Tibetan text
        content = ""
        
        # Method 1: Extract text from each paragraph individually
        paragraphs = main_text_element.find_all('p')
        if paragraphs:
            paragraph_texts = []
            for p in paragraphs:
                # Get the text directly from the HTML to preserve encoding
                p_text = str(p)
                # Extract just the text content using regex
                text_only = re.sub(r'<[^>]+>', '', p_text)
                # Decode HTML entities
                text_only = html.unescape(text_only)
                paragraph_texts.append(text_only.strip())
            
            content = '\n'.join(paragraph_texts)
        
        # Method 2: If no paragraphs or content is empty, try direct extraction
        if not content:
            # Get all direct text nodes
            texts = []
            for element in main_text_element.find_all(text=True, recursive=True):
                if element.parent.name not in ['script', 'style', 'head', 'title']:
                    texts.append(element.strip())
            
            content = '\n'.join([t for t in texts if t])
        
        # Method 3: Last resort - get the raw HTML and extract text
        if not content:
            html_content = str(main_text_element)
            content = re.sub(r'<[^>]+>', ' ', html_content)
            content = html.unescape(content)
            content = re.sub(r'\s+', ' ', content).strip()
        
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