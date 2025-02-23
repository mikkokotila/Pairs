import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, '../dev-notebooks')

# Add the parent directory to the system path
parent_path = os.path.abspath(os.path.join(os.getcwd(), '../../'))
load_dotenv(parent_path + '/.env')
api_key = os.getenv('api_key')

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


def pre_translate(messages: list,
                  context: dict = context,
                  api_key: str = api_key) -> str:

    '''
    Pre-translate a list of messages using the Claude API.

    Parameters:

    messages (list): A list of messages to be translated.
    context (dict): A dictionary containing the context of the translation.
    api_key (str): The API key for the Claude API.

    Returns:

    str: The translated response from the API.
    '''

    from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
    from bokit.workflows.translate_with_claude import translate_with_claude

    messages = prepare_messages_for_translate(messages)

    system = " ".join(f"{key}: {value}; " for key, value in context.items())

    reply = translate_with_claude(api_key, system, messages)

    return reply[0].text
