def get_lhs_identifier_properties(formula_rearrangement,formula_identifiers):
    """Get left-hand side identifier name and symbol."""
    identifier_name = formula_identifiers[0][1]
    identifier_symbol = formula_identifiers[0][0]
    return identifier_name, identifier_symbol

def get_answer_value_and_unit(answer_input):
    """Get answer value and unit from parsing user answer input."""
    answer_value_unit = answer_input.split()
    answer_value = answer_value_unit[0]
    answer_unit = answer_value_unit[1]
    return answer_value,answer_unit

def check_value(formula_rearrangement,answer_value):
    """Description."""
    return value_correct

def check_unit(formula_rearrangement,answer_value):
    """Description"""
    return unit_correct