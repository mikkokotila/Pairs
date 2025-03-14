def wylie_to_tibetan(string):
    
    '''Takes in string, and converts to Tibetan following Wylie rules.
    Adds Tsek between syllables and after the last syllable.
    
    wylie_string | str | Wylie string to be converted to Tibetan.
    '''

    import pyewts

    converter = pyewts.pyewts()

    return converter.toUnicode(string, [])
