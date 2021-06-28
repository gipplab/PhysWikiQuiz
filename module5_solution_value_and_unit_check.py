import sympy

def get_lhs_identifier_properties(formula_rearrangement,formula_identifiers):
    """Get left-hand side identifier name and symbol."""
    identifier_name = formula_identifiers[0][1]
    identifier_symbol = formula_identifiers[0][0]
    return identifier_name, identifier_symbol

def get_answer_value_and_unit(answer_input):
    """Get answer value and unit from parsing user answer input."""
    try:
        answer_value_unit = answer_input.split()
        answer_value = answer_value_unit[0]
        answer_unit = answer_value_unit[1]
    except:
        print("Please input value AND unit!")
        return None,None

    return answer_value,answer_unit

def check_value(identifier_values,answer_value):
    """Check if input value corresponds to formula value."""
    answer_value = sympy.Rational(answer_value)
    value_correct = answer_value == identifier_values[0]

    #TODO: allow for float tolerance of +- x %

    return value_correct

def check_unit(formula_unit_dimension,answer_unit):
    """Check if input unit corresponds to formula unit."""
    unit_correct = answer_unit == formula_unit_dimension

    return unit_correct