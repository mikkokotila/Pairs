context = {
    
  "role": "system",
  "content": {
    "role_description": "Master translator and pandita",
    "job": "Translate Tibetan into English from Dzogchen texts",
    "output_format": {
      "structure": "Valid JSON object with kv-pairs. Omit ``` or any other style markings. Just JSON.",
      "required_sections": [
        "Translation",
      ],
      "style_guide": [
        "Translate segment by segment, segments are marked with [x]",
        "Keep the [x] always on its place, simply replace the source string with English with [x] intact",
        "Translate word for word, do not borrow words from one segment to another",
        "If text is in prose, make sure the inter-segment punctuation is correct",
        "If text is in verse, always capitalize first letter of each line and end with correct punctuation",
        "Leave technical sanskrit terms in sanskrit (e.g. dharmakaya, dharma, etc.)",
        "Emphasize precision and eloquence.",
        "Use Biblical English (KJV style) for terminology.",
        "Use Tibetan script only, no Wylie transliteration.",
        "Put added words [inside] brackets."
      ]
    }
  }
}


def auto_translate(messages: list,
                  context: dict = context) -> str:

    '''
    Pre-translate a list of messages using the Claude API.

    Parameters:

    messages (list): A list of messages to be translated.
    context (dict): A dictionary containing the context of the translation.

    Returns:

    str: The translated response from the API.
    '''

    import os
    import json
    from utils.get_env_vars import get_env_vars

    from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
    from bokit.workflows.translate_with_claude import translate_with_claude

    messages = prepare_messages_for_translate(messages)

    system = " ".join(f"{key}: {value}; " for key, value in context.items())

    # Try to get API key from environment variables
    env_vars = get_env_vars(keys=['api_key'],
                           file_name='.env',
                           relative_to_pwd='../../../')
    
    api_key = env_vars.get('api_key')
    
    # Check if API key is available
    if not api_key:
        # Return a JSON error message if API key is not found
        error_message = {
            "Translation": "ERROR: Claude API key not found. Please add your API key to the .env file in the parent directory with the format 'api_key=your_api_key_here'."
        }
        return json.dumps(error_message)

    try:
        reply = translate_with_claude(api_key,
                                    system,
                                    messages,
                                    max_tokens=10000,
                                    model="claude-3-7-sonnet-20250219")
        
        return reply[0].text
    except Exception as e:
        # Return a JSON error message if there's an exception
        error_message = {
            "Translation": f"ERROR: Failed to translate with Claude API. Error: {str(e)}"
        }
        return json.dumps(error_message)
