import sympy

def get_lhs_identifier_properties(formula_identifiers):
    """Get left-hand side identifier name and symbol."""
    identifier_name = formula_identifiers[0][1]
    identifier_symbol = formula_identifiers[0][0]
    return identifier_name, identifier_symbol

def get_answer_value_and_unit(answer_input):
    """Get answer value and unit from parsing user answer input."""
    answer_value_unit = answer_input.split()
    if len(answer_value_unit) == 1:
        print("Please input value AND unit (space-separated)!")
        answer_value = None
        answer_unit = None
    elif len(answer_value_unit) > 1:
        answer_value = answer_value_unit[0]
        answer_unit = ' '.join(answer_value_unit[1:])

    return answer_value,answer_unit

def check_value(solution_value,answer_value):
    """Check if input value corresponds to formula value."""
    #answer_value = sympy.Rational(answer_value)
    value_correct = answer_value == solution_value

    # allow for float tolerance of +- 1%
    try:
        tolerance = 1/100
        answer_value = sympy.sympify(answer_value.replace(",", "."))
        solution_value = sympy.sympify(solution_value)
        answer_solution_ratio = float(answer_value)/float(solution_value)
        if 1-tolerance < answer_solution_ratio < 1+tolerance:
            value_correct = True
    except:
        pass

    return value_correct

def check_unit(formula_unit_dimension,answer_unit):
    """Check if input unit corresponds to formula unit."""
    #unit_correct = answer_unit == formula_unit_dimension
    try:
        answer_units = set(answer_unit.split())
        correct_units = set(formula_unit_dimension.split())
        unit_correct = answer_units == correct_units

    except:
        unit_correct = False

    return unit_correct