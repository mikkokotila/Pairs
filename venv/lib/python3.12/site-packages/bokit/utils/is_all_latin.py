def is_all_latin(word):

    '''Takes in a word and returns True if it is Latin, False otherwise.
    
    word | str | word to check
    '''
    
    import unicodedata as ud
    
    return all(['LATIN' in ud.name(c) for c in word])
