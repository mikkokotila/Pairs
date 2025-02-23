def build_corpus():

    import sys
    sys.path.insert(0, '../Bokit/')
    
    import bokit
    import os
    
    collections = ['Seventeen-Tantras',
                   'Seven-Treasures',
                   'Lama-Yangthig',
                   'Miscellaneous',
                   'Key-Instruction-Treasury']
    
    texts = {}
    
    for collection in collections:
    
        collection += '/'
    
        file_paths = os.listdir('../Boco/texts/' + collection)
        file_paths = [collection + i for i in file_paths]
    
        for file_path in file_paths:
        
            f = open('../Boco/texts/' + file_path , 'r')
            text = f.readlines()
            
            # remove lines with nothing but \n
            text = [i for i in text if i != '\n']
            
            # remove \n all together
            text = [i.replace('\n', '') for i in text]
            
            # remove lines with just a number
            text = [i for i in text if bokit.utils.is_tibetan_number(i) is False]
            
            # remove all lines with non-Tibetan text
            text = [i for i in text if bokit.utils.is_all_latin(i) is False]
        
            texts[file_path.split('/')[-1].split('.')[0]] = text

        return texts