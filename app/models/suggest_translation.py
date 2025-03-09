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
                        context: dict = context) -> str:

    '''
    Pre-translate a list of messages using the Claude API.

    Parameters:

    messages (list): A list of messages to be translated.
    context (dict): A dictionary containing the context of the translation.

    Returns:

    str: The translated response from the API.
    '''

    from utils.get_env_vars import get_env_vars

    from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
    from bokit.workflows.translate_with_claude import translate_with_claude

    messages = prepare_messages_for_translate(messages)

    system = " ".join(f"{key}: {value}; " for key, value in context.items())

    api_key = get_env_vars(keys=['api_key'],
                           file_name='.env',
                           relative_to_pwd='../../../')['api_key']

    reply = translate_with_claude(api_key, system, messages, model="claude-3-7-sonnet-20250219")

    return reply[0].text
