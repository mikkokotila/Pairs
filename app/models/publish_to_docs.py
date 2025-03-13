import sys
sys.path.insert(0, '../../bophono')
import bophono

def publish_to_docs(service_account_file,
                    service_account_subject,
                    segments,
                    document_filename,
                    include_phonetics=False,
                    print_url=False):

    '''Publish to Google Docs. The default behavior is
    to take you directly to the ready formatted doc.

    # Parameters

    service_account_file (str): The path to the service account file.
    service_account_subject (str): The email of the service account.
    document_filename (str): The name of the new document.
    include_phonetics (bool): Whether to include phonetics.
    print_url (bool): Whether to print the URL of the document

    # Overview

        The way it works is that you have a project in
    Transifex, for which one translation is taken, and
    then all that is pushed directly into a new document
    on Google docs with whatever formatting you like.

    The formatting is provided by another Google docucment,
    which you can style exactly as you like. The supported
    styles are:

    - Normal
    - Title
    - Subtitle
    - H1
    - H2
    - H3
    - Mantra

    These can be used for example in the following way in 
    sadhana text.

    - Normal is for the non-liturcial text
    - Title is for the main title
    - Subtitle is for any subtitles
    - H1 is for the Tibetan text
    - H2 is for the phonetic text
    - H3 is for the translation
    - Mantra is for mantras

    This requires that in Transifex the segments are created
    with this in mind, so that styles are not mixed into a
    single pair. As the translation takes place, then Normal,
    Title, Subtitle, and Mantra must be added respectively
    to Transifex > Edit Context > String Instructions.
    H1, H2, and H3 are automatically added.

    '''

    import bokit

    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials
    import webbrowser

    # Initialize the pnonetizer
    p = bokit.Phonetize()

    # Add phonetics
    phonetics = []

    for i in range(len(segments)):

        if include_phonetics is True:

            if segments[i][2] is None:

                phonetics_temp = []

                tokens = segments[i][0].split(' ')

                for token in tokens:

                    phonetic = p.query(token)['phonetic']
                    phonetic = phonetic.replace("é", "e").replace("ü", "u")

                    phonetics_temp.append(phonetic)

                phonetics_temp = ' '.join(phonetics_temp).lstrip().rstrip()

            else:
                phonetics_temp = ''

        else:
            phonetics_temp = ''

        phonetics.append(phonetics_temp)

    combined = []

    for i in range(len(segments)):

        string = segments[i][0].replace(' ', '')
        translation = segments[i][1]
        phonetic = phonetics[i]
        style = segments[i][2]

        combined.append([string, translation, phonetic, style])

    # Authenticate with your service account credentials
    scopes = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

    creds = Credentials.from_service_account_file(
        service_account_file,
        scopes=scopes,
        subject=service_account_subject
    )

    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)

    from utils.get_env_vars import get_env_vars

    template_doc_id = get_env_vars(keys=['google_template_doc_id'],
                            file_name='.env',
                            relative_to_pwd='../../../')['google_template_doc_id']

    # Copy the template document
    copied_file = drive_service.files().copy(
        fileId=template_doc_id,
        body={"name": document_filename}
    ).execute()

    # Get the new document ID
    new_doc_id = copied_file.get('id')

    # Insert content into the new document
    def insert_text_with_style(index, text, style):
        return [
            {
                "insertText": {
                    "location": {"index": index},
                    "text": text + "\n"
                }
            },
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": index, "endIndex": index + len(text)},
                    "paragraphStyle": {
                        "namedStyleType": style
                    },
                    "fields": "namedStyleType"
                }
            }
        ]

    # Prepare the requests to add all text
    requests = []
    current_index = 1  # Start inserting after the template's existing content

    for i, block in enumerate(combined):  # Iterate through all blocks in `combined`
        tibetan, translation, phonetic, override_style = block

        # Determine style based on [3] value
        if override_style in ["Normal", "Title", "Subtitle"]:
            # Map to valid Google Docs named styles
            style = {
                "Normal": "NORMAL_TEXT",
                "Title": "TITLE",
                "Subtitle": "SUBTITLE"
            }[override_style]
        else:
            style = None  # No override; use default H1, H3, H2 for Tibetan, Translation, Phonetic

        # Insert Tibetan text
        requests += insert_text_with_style(
            current_index, tibetan, style if style else "HEADING_1"
        )
        current_index += len(tibetan) + 1

        # Insert Phonetic text if not empty
        if phonetic.strip():
            requests += insert_text_with_style(
                current_index, phonetic, style if style else "HEADING_2"
            )
            current_index += len(phonetic) + 1

        # Insert Translation text
        requests += insert_text_with_style(
            current_index, translation, style if style else "HEADING_3"
        )
        current_index += len(translation) + 1

        # Add a line break only if the next block style is Normal
        next_style = (
            combined[i + 1][3] if i + 1 < len(combined) else None
        )  # Get the next block's style if available
        '''
        if next_style == "Normal":
            requests.append({
                "insertText": {
                    "location": {"index": current_index},
                    "text": "\n"
                }
            })
            current_index += 1
        '''
    # Execute the batch update to add content with appropriate styles
    docs_service.documents().batchUpdate(
        documentId=new_doc_id,
        body={"requests": requests}
    ).execute()

    link_to_doc = f"https://docs.google.com/document/d/{new_doc_id}/edit"

    if print_url is True:

        print(f"Document created: {link_to_doc}")

    _ = webbrowser.open(link_to_doc)
