def clean_tibetan_string(string,
                         suppress_extra_whitespace=True, 
                         remove_line_breaks=True,
                         add_space_after_tsad=True):
    
    '''For loading texts into corpus with add_text_to_corpus().
    
    file_path | str | path to text file
    supress_extra_whitespace | bool | if True, removes extra whitespace
    remove_line_breaks | bool | if True, removes line breaks from text
    add_space_after_tsad | bool | if True, adds space after tsad
    '''
    
    import re

    if add_space_after_tsad:

        # add space after tsad but only the last one in a sequence
        string = re.sub(r'(།+)', r'\1 ', string)
        
    if suppress_extra_whitespace:

        # remove tabs
        string = string.replace('\t', ' ')
        
        # remove whitespace when more than one in a sequence
        string = re.sub(' +', ' ', string)

        # remove non-breaking space
        string = ' '.join([i.replace('\xa0', '') for i in string.split(' ')])

    if remove_line_breaks:

        # remove all newlines
        string = string.replace('\n', '')
  
    return string