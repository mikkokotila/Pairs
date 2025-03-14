class Tokenize:

    '''Tokenization pipeline for Tibetan text'''
    
    def __init__(self):

        from botok import WordTokenizer
        from botok.config import Config
        from pathlib import Path
        
        # initialize the tokenizer
        config = Config(dialect_name="general", base_path=Path.home())
        self._wt = WordTokenizer(config=config)

    def query(self, text, split_affixes=False, tokenizer_object=False):

        '''Takes in Tibetan string and returns list of tokens.
        
        text | str | Tibetan string to tokenize
        split_affixes | bool | if True, returns list of tokens with affixes
        tokenizer_object | bool | if True, returns tokenizer object with more data
        '''

        # initialize the list of tokens to be returned
        tokens = []

        # tokenize the input text
        tokenizer_output = self._wt.tokenize(text, split_affixes=split_affixes)
        
        if tokenizer_object is True:
            return tokenizer_output
        
        for token in tokenizer_output:
            
            if split_affixes is True:
                tokens.append(token['text'])
            elif split_affixes is False:
                tokens.append(token['text_unaffixed'])

        return tokens