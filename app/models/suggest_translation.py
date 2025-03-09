context = {
    
  "role": "system",
  "content": {
    "role_description": "Master translator and pandita",
    "job": "Translate Tibetan into English from Dzogchen texts",
    "output_format": {
      "structure": "JSON object with kv-pairs",
      "required_sections": [
        "Translation",
        "Alternative Translation",
        "Breakdown word-by-word",
        "Doubts",
      ],
      "style_guide": [
        "Emphasize precision and eloquence.",
        "Use Biblical English (KJV style) for terminology.",
        "Use Tibetan script only, no Wylie transliteration.",
        "Translate word for word.",
        "Put added words [inside] brackets."
      ]
    }
  }
}


def suggest_translation(messages: list,
                        context: dict = context,
                        timeout: int = 25) -> str:

    '''
    Pre-translate a list of messages using the Claude API.

    Parameters:

    messages (list): A list of messages to be translated.
    context (dict): A dictionary containing the context of the translation.
    timeout (int): Timeout in seconds for the API call.

    Returns:

    str: The translated response from the API.
    '''

    import traceback
    import sys
    from utils.get_env_vars import get_env_vars

    try:
        from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
        from bokit.workflows.translate_with_claude import translate_with_claude

        print(f"Preparing messages for translation: {messages[:1]}")
        messages = prepare_messages_for_translate(messages)

        system = " ".join(f"{key}: {value}; " for key, value in context.items())

        api_key = get_env_vars(keys=['api_key'],
                            file_name='.env',
                            relative_to_pwd='../../../')['api_key']

        print("Calling Claude API for translation...")
        
        # Try with timeout parameter, fall back to without if not supported
        try:
            reply = translate_with_claude(api_key, system, messages, model="claude-3-7-sonnet-20250219", timeout=timeout)
        except TypeError:
            # If timeout parameter is not supported
            print("Timeout parameter not supported, calling without timeout")
            reply = translate_with_claude(api_key, system, messages, model="claude-3-7-sonnet-20250219")

        if not reply or len(reply) == 0:
            print("No reply received from Claude API", file=sys.stderr)
            return '{"Translation": "Error: No response from translation service."}'

        print(f"Translation received, length: {len(reply[0].text)}")
        return reply[0].text
        
    except Exception as e:
        error_message = f"Error in suggest_translation model: {str(e)}"
        print(error_message, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return f'{{"Translation": "Error during translation: {str(e)}"}}'
