def tibetan_to_wylie(string):

    '''Takes in string, and converts to Wylie following Wylie rules.
    
    string | str | Tibetan string to be converted to Wylie.
    '''

    import pyewts

    converter = pyewts.pyewts()

    return converter.toWylie(string)
