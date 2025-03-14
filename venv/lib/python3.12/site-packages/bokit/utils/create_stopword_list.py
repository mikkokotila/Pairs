def create_stopword_list():

    '''Returns a list of stopwords in Tibetan language 
    by combining the lists of punctuation, particles,
    and special characters.'''

    from bokit.utils.create_punctuation_list import create_punctuation_list
    from bokit.utils.create_particles_list import create_particles_list
    from bokit.utils.create_special_char_list import create_special_char_list

    return list(set(create_punctuation_list() + create_particles_list() + create_special_char_list()))
