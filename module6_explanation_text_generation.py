def generate_explanation_text(concept_qid,defining_formula,
                              identifier_properties,identifier_values,):

    #url = "https://www.wikidata.org/wiki/" + concept_qid
    url = "www.wikidata.org/wiki/" + concept_qid
    # insert values

    symbol_value_unit = {}
    try:
        for idx in range(len(identifier_properties)):
            symbol_value_unit[identifier_properties[idx][1]] = " " + str(identifier_values[idx]) + " " + identifier_properties[idx][2] + " "

        values_inserted = ""
        for character in defining_formula:
            try:
                character = character.replace(character,symbol_value_unit[character])
            except:
                pass
            values_inserted += character

        explanation_text = "Solution from " + url + " formula " + defining_formula + " with " + values_inserted + "."

    except:
        try:
            explanation_text = "Solution from " + url + " formula " + defining_formula + " ."
        except:
            explanation_text = ""

    return explanation_text