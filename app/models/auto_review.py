context = {
    
  "role": "system",
  "content": {
    "role_description": "Master translator and pandita",
    "job": "Carefully review translation of Tibetan into English from Dzogchen texts",
    "output_format": {
      "structure": "Valid JSON object with kv-pairs. Omit ``` or any other style markings. Just JSON.",
      "required_sections": [
        "Review comments",
      ],
      "style_guide": [
        "I will give you a source string, and translated string separated by ~",
        "Each segment pair is separated by [[x]] where x is an index.",
        "When you add review, make sure it starts with [[x]] where x is pair index the review is for.",
        "Review each segment, make review comments when relevant.",
        "Do not give praise or affirmation, if you find issues, point it out.",
        "Analyze both source and translated string, but comment only on the translated string.",
        "Look for issues in grammar, punctuation, inconsistent word use, and other issues.",
        "Emphasize precision and eloquence.",
        "If you suggest alternatives, use Biblical English (KJV style) for terminology.",
        "Use Tibetan script only, no Wylie transliteration.",
        "Put added words [inside] brackets.",
        "Do no change the source string or the translated string, only add review comments."
      ]
    }
  }
}


def auto_review(messages: list,
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

    api_key = get_env_vars(keys=['claude_api_key'],
                           file_name='.env',
                           relative_to_pwd='../../../')['claude_api_key']

    reply = translate_with_claude(api_key,
                                  system,
                                  messages,
                                  max_tokens=10000,
                                  model="claude-3-7-sonnet-20250219")

    return reply[0].text
