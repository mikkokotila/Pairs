context = {

  "role": "system",
  "content": {
    "role_description": "Master translator and pandita",
    "job": "Translate Tibetan keyword into English from Dzogchen texts",
    "output_format": {
      "structure": "Valid JSON object with kv-pair. No ```json or ``` at the beginning or end.",
      "required_sections": [
        "Keyword",
        "Definition",
        "Part-of-Speech",
        "Tenses (if applicable)",
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


def keyword_research(keyword, context=context, dictionary_window=1000, corpus_window=10):

    text = open('../../Boco/texts/Seven-Treasures/ཚིག་དོན་རིན་པོ་ཆེའི་མཛོད.txt', 'r').read()

    import re
    import random
    import requests

    from utils.get_env_vars import get_env_vars

    from bokit.workflows.prepare_messages_for_translate import prepare_messages_for_translate
    from bokit.workflows.search_keyword_meaning import search_keyword_meaning

    def normalize_spaces(text):
        return re.sub(r'\s+', ' ', text).strip()

    text = normalize_spaces(text).split(' ')

    result = []

    for segment in text:
        if keyword in segment:
            result.append(segment)

    result = list(set(result))

    # Check if result list is empty to avoid IndexError
    if not result:
        context['examples'] = ''
    else:
        context['examples'] = ';'.join(random.choices(result, k=min(corpus_window, len(result))))

    try:
        context_dictionary = requests.get(f"http://127.0.0.1:5001/lookup-glossary?keyword={keyword}").json()
        keyword = list(context_dictionary['monlam'].keys())[0]
        context_dictionary = context_dictionary['monlam'][keyword]

        if len(context_dictionary) > dictionary_window:
            dictionary_window = len(context_dictionary)

        context['dictionary'] = context_dictionary[:dictionary_window]
    except (requests.exceptions.ConnectionError, KeyError, IndexError) as e:
        # Handle the case where the dictionary server is not running or returns unexpected data
        print(f"Error connecting to dictionary server: {e}")
        context['dictionary'] = []
    
    messages = prepare_messages_for_translate([keyword])

    api_key = get_env_vars(keys=['claude_api_key'],
                           file_name='.env',
                           relative_to_pwd='../../../')['claude_api_key']

    reply = search_keyword_meaning(api_key, messages, context)

    return reply.content[0].text
