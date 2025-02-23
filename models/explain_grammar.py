import os

from dotenv import load_dotenv

# Add the parent directory to the system path
parent_path = os.path.abspath(os.path.join(os.getcwd(), '../../'))
load_dotenv(parent_path + '/.env')
api_key = os.getenv('api_key')

context = {
    
  "role": "system",
  "content": {
    "role_description": "Master translator and pandita",
    "job": "Explain grammar in English for segments of Dzogchen texts",
    "output_format": {
      "structure": "JSON object with kv-pairs",
      "required_sections": [
        "Segment",
        "Morphological Structure",
        "Syntactic Ambiguities",
        "Missing Elements"
      ],
      "style_guide": [
        "Emphasize precision and eloquence.",
        "Use Biblical English (KJV style) for terminology.",
        "Use Tibetan script only, no Wylie transliteration.",
      ]
    }
  }
}


def explain_grammar(keyword, context=context, dictionary_window=800):
    
    import re
    import random
    import requests
    
    from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
    from bokit.workflows.search_keyword_meaning import search_keyword_meaning
    
    context_dictionary = requests.get(f"http://127.0.0.1:5001/lookup-glossary?keyword={keyword}").json()
    
    keyword = list(context_dictionary['monlam'].keys())[0]

    context_dictionary = context_dictionary['monlam'][keyword]

    if len(context_dictionary) > dictionary_window:
        dictionary_window = len(context_dictionary)

    context['dictionary'] = context_dictionary[:dictionary_window]
    
    messages = prepare_messages_for_translate([keyword])
    
    reply = search_keyword_meaning(api_key, messages, context)

    return reply.content[0].text
 