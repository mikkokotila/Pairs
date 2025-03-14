class OCR: 

    '''Converts images to text using Google Cloud Vision API.'''

    def __init__(self):

        '''Initialize the OCR class'''

        from google.cloud import vision
        self._vision = vision

        _ = ''

    def query(self, image, lang_hint=None):

        '''Converts images to text using Google Cloud Vision API.
        
        image | str or Path or bytes | path to image file or image bytes
        lang_hint | str | language hint for OCR
        '''

        import io
        import json
        import pathlib

        # initialize the OCR client
        vision_client = self._vision.ImageAnnotatorClient()

        # load the image in the case path is provided
        if isinstance(image, (str, pathlib.Path)):
            with io.open(image, "rb") as image_file:
                content = image_file.read()
        
        # load the image in the case bytes are provided
        else:
            content = image
        
        # create the OCR image object
        ocr_image = self._vision.Image(content=content)

        # set the features
        features_config = {"type_": self._vision.Feature.Type.DOCUMENT_TEXT_DETECTION, "model": "builtin/weekly"}
        features = [features_config]

        # set the image context
        image_context = {}
        
        # set the language hint if one is provided and otherwise use default None
        if lang_hint:
            image_context["language_hints"] = [lang_hint]

        # process the image
        annotate_conf = {"image": ocr_image, "features": features, "image_context": image_context}
        response = vision_client.annotate_image(annotate_conf)
        response_json = self._vision.AnnotateImageResponse.to_json(response)
        response = json.loads(response_json)
        
        # return the text
        try:
            return response['textAnnotations'][0]['description']
        
        # or return the response if there is no text
        except:
            return 'The response was : ' + str(response)
    