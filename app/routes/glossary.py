def glossary(self):

    from flask import request, jsonify, render_template
    from tinydb import TinyDB, Query
    import os

    # Ensure glossary database exists
    glossary_db_path = os.path.join(self.db_path, 'glossary.json')
    db = TinyDB(glossary_db_path)
    Term = Query()

    # Sufficient for lookup
    search_term = request.form.get('search_term').strip()

    # Needed for the case where new entry is added
    if search_term.startswith('+'):
        content = search_term.split('+')[-1].strip().split(' ')
        source_language = content[0]
        target_language = content[-1]

        # Insert new term into TinyDB
        db.insert({
            'source_string': source_language,
            'target_string': target_language
        })

        return jsonify(result=render_template("context_template.html",
                                              data={source_language: target_language}))
    
    # Handle the case where keyword lookup is made
    results = db.search(Term.source_string == search_term)
    
    if results:
        # Return the first matching result
        result = results[0]
        return jsonify(result=render_template("context_template.html", 
                                              data={search_term: result['target_string']}))
    
    return jsonify(result=render_template("context_template.html",
                                          data={search_term: 'No results found'}))