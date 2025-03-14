def image_to_translation(images, debug=False):

    '''Converts images to translation using Google Cloud Vision API and Mitra Translation API.
    images | list of str or Path or bytes | path to image file or image bytes
    debug | bool | if set to True, will print the OCR output
    '''

    import bokit

    ocr = bokit.OCR()

    translate = bokit.Translate()

    out = []

    import tqdm

    for i in tqdm.tqdm(range(len(images))):
        
        data = ocr.query(images[i])

        if debug:
            out.append([data, translate.query(data)])
        else:
            out.append(translate.query(data))
                       
    return out
