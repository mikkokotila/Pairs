from urllib import request
import traceback
import sys


def suggest_translation(self):
    import json
    from json import JSONDecodeError
    from flask import request, jsonify, render_template
    from utils.session_manager import session_manager
    from models.suggest_translation import suggest_translation

    try:
        request_data = request.json
        text = request_data.get("text", "")
        
        if not text:
            return jsonify(result="No text provided for translation."), 400
        
        print(f"Suggest translation request received for text: {text[:50]}...")
        
        # Call the model to get the translation
        translation_text = suggest_translation([text])
        print(f"Translation received: {translation_text[:100]}...")
        
        # Save to session history
        session_manager(translation_text)
        
        # Try to parse as JSON first
        try:
            json_data = json.loads(translation_text)
            return jsonify(result=render_template("context_template.html", data=json_data))
        except JSONDecodeError:
            # If not valid JSON, return as plain text
            print("Response is not valid JSON, returning as plain text")
            return jsonify(result=translation_text)
            
    except Exception as e:
        error_message = f"Error in suggest_translation: {str(e)}"
        print(error_message, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return jsonify(result=f"An error occurred: {str(e)}"), 500
    