def build_text(project,
               resource,
               start_id=None, 
               end_id=None, 
               publish=False):

    from bokit.Transifex import Transifex
    from bokit.Phonetize import Phonetize

    phonetize = Phonetize()

    transifex = Transifex()

    data = transifex.read_text(project=project, resource=resource)

    out = []
    
    data_len = len(data['data'])

    for i in range(data_len):

        # handle source string
        source_string = data['included'][i]['attributes']['key']
        source_string = source_string.replace('་␣', '')
        
        # handle phonetic string
        phonetic_string = ''

        for string in source_string.split(' '):
            phonetic_string = phonetic_string + phonetize.query(string) + ' '

        phonetic_string = phonetic_string.strip()
        
        # handle target string
        target_string = data['data'][i]['attributes']['strings']['other']

        # handle string instructions
        string_instructions = data['included'][i]['attributes']['instructions']

        # add record
        
        segment = [source_string, phonetic_string, target_string, string_instructions]
        
        if start_id is not None:
            
            if end_id is None:
                end_id = data_len
            
            if i >= start_id-1 and i <= end_id-1:
                out.append(segment)
        else:
            out.append(segment)
    
    # make ready for publishing
    if publish is True:
        for i in out:
            tibetan = i[0].replace(' ', '').replace(' ', ' ')
            phonetic = '\n' + i[1]
            english = '\n' + i[2] + '\n'
            print(tibetan, phonetic, english)
    
    # return as as data
    else: 
        return out