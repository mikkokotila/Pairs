class CreateFlashcards:
    
    def __init__(self, corpus, n=100):

        import tqdm

        from corpus_manager import Tokenizer

        self.final_segments = []

        tokenizer = Tokenizer.Tokenizer()

        self.tokens = list(corpus.counts_by_token(n).keys())

        for i, token in enumerate(self.tokens):
            self.tokens[i] = self.clean_token_for_flashcards(token)

        self.tokens = set(self.tokens)

        segments = []

        for token in self.tokens:

            segments_for_token = corpus.search_token(token)
            segments.append(segments_for_token)

        for token_segments in tqdm.tqdm(segments):

            for segment in token_segments:

                tokens_temp = tokenizer.get_tokens(segment[0])

                temp = []

                for token in tokens_temp:

                    if token['text'] in self.tokens:
                        pass
                    else:
                        continue

                    temp.append(segment[0])

            self.final_segments.append(temp)
            
    def clean_token_for_flashcards(self, token):

        if token.endswith('་') is False:
            return token + '་'
            
        elif token.endswith('འི་'):
            return token[:-3] + '་'

        elif token.endswith('པོར་'):
            return token[:-2] + '་'

        elif token.endswith('པར་'):
            return token[:-2] + '་'

        elif token.endswith('པོས་'):
            return token[:-2] + '་'

        elif token.endswith('པས་'):
            return token[:-2] + '་'

        elif token.endswith('བར་'):
            return token[:-2] + '་'

        elif token.endswith('འོ་'):
            return token[:-3] + '་'

        else:
            return token

def sentences_to_anki(counts, save_to_file=False):

    '''Returns a list of sentences in format that can be imported into Anki.
    
    counts | dict | a dictionary of counts
    save_to_file | str | if set to a string, saves the output to a file
    '''

    out = []
    
    for key in counts.keys():
        if key.endswith('ང'):
            out.append(key + '་།')
        else:
            out.append(key + '།')
            
    if isinstance(save_to_file, str):    
        f = open(save_to_file, 'w')
        f.write('\n'.join(out))
        
    return out