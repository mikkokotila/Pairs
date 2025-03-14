def remove_non_tibetan(string):

    '''Removes all non-Tibetan characters from a string.

    string | str | string to remove non-Tibetan characters from
    '''

    return ''.join(ch for ch in string if '\u0F00' <= ch <= '\u0FFF' or ch.isspace())
