context = {
    
  "role": "system",
  "content": {
    "role_description": "Master translator and pandita",
    "job": "Explain grammar in English for segments of Dzogchen texts",
    "output_format": {
      "structure": "Valid JSON object with kv-pair. No ```json or ``` at the beginning or end.",
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

    from utils.get_env_vars import get_env_vars
    
    from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
    from bokit.workflows.search_keyword_meaning import search_keyword_meaning
    
    context_dictionary = requests.get(f"http://127.0.0.1:5001/lookup-glossary?keyword={keyword}").json()
    
    keyword = list(context_dictionary['monlam'].keys())[0]

    context_dictionary = context_dictionary['monlam'][keyword]

    if len(context_dictionary) > dictionary_window:
        dictionary_window = len(context_dictionary)

    context['dictionary'] = context_dictionary[:dictionary_window]
    
    messages = prepare_messages_for_translate([keyword])

    api_key = get_env_vars(keys=['claude_api_key'],
                           file_name='.env',
                           relative_to_pwd='../../../')['claude_api_key']

    reply = search_keyword_meaning(api_key, messages, context)

    return reply.content[0].text
 