def get_question_text(formula_identifiers,identifier_values,identifier_unit_dimensions):
    """Get question text from identifier names, symbols, and units."""

    # Get identifier information (name,symbol,value,unit)
    identifier_information = []

    for identifier_index in range(len(formula_identifiers)):
        identifier_name = formula_identifiers[identifier_index][1]
        identifier_symbol = formula_identifiers[identifier_index][0]
        identifier_unit = formula_identifiers[identifier_index][2]
        #identifier_unit = identifier_unit_dimensions[identifier_index]
        identifier_value = str(identifier_values[identifier_index])
        identifier_information.append((identifier_name,identifier_symbol,identifier_value,identifier_unit))

    # Generate question text

    # Left-hand side identifiers
    left_hand_side_identifier = identifier_information[0]
    question_text = 'What is the '
    question_text += ' '.join([left_hand_side_identifier[0],left_hand_side_identifier[1]]) + ', given '

    # Right-hand side identifiers
    right_hand_side_identifiers = identifier_information[1:]
    for right_hand_side_identifier in right_hand_side_identifiers:
        question_text += right_hand_side_identifier[0] + ' ' + right_hand_side_identifier[1] + ' = ' + str(right_hand_side_identifier[2]) + ' ' + right_hand_side_identifier[3] + ', '

    # Finalize
    question_text = question_text[:-2] + ' ?\n'

    return question_text