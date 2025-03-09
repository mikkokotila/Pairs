def glossary(self):

    from flask import request, jsonify, render_template

    # Sufficient for lookup
    search_term = request.form.get('search_term').strip()

    # Needed for the case where new entry is added
    if search_term.startswith('+'):

        content = search_term.split('+')[-1].strip().split(' ')
        source_language = content[0]
        target_language = content[-1]

        with open('data/glossary.txt', 'a') as file:
            file.write(f"{source_language}~{target_language}\n")

        return jsonify(result=render_template("context_template.html",
                                                data={source_language: target_language}))
    
    # Handle the case where keyword lookup is made
    with open('data/glossary.txt', 'r') as file:
        glossary = file.readlines()
    
    for line in glossary:
        
        if search_term == line.split('~')[0]:
            return jsonify(result=render_template("context_template.html", data={search_term: line.split('~')[1]}))
        
    return jsonify(result=render_template("context_template.html",
                                                    data={search_term: 'No results found'}))