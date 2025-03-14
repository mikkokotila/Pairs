def is_partly_tibetan(string, percentage=0.5):

    '''Returns True if more than percentage of characters in the string are Tibetan.
    
    string | str | string to check if Tibetan or not
    percentage | float | percentage of Tibetan characters required to return True
    '''

    tibetan_chars = sum('\u0F00' <= ch <= '\u0FFF' for ch in string)
    total_chars = len(string)
    
    return tibetan_chars / total_chars > percentage