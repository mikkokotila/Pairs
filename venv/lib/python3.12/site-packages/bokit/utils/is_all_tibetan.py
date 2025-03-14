def is_all_tibetan(string):

    '''Returns True if all characters in the string are Tibetan.
    
    string | str | string to check if Tibetan or not
    '''

    return all('\u0F00' <= char <= '\u0FFF' for char in string)
