import sympy
import re

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

def clean_unit_answer(answer_unit):
    # find '/', only clean/works if single occurrence
    if len(answer_unit.count('/')) == 1:
        for delimiter in ['/(.*)', '/(.*) ', ' /(.*)', ' /(.*) ']:
            try:
                match = re.search(delimiter,answer_unit)
                if match is not None:
                    match = match.group(0)
                    if not '^' in match:
                        # exponent is (-)1
                        replacement = match.replace('/','') + '^-1'
                    else:
                        # other exponents
                        # remove '/'
                        replacement = match.replace('/','')
                        # switch exponent sign
                        if '-' in replacement:
                            replacement = replacement.replace('-', '')
                        elif '+' in replacement:
                            replacement = replacement.replace('+', '-')
                        else:
                            replacement = replacement.replace('^', '^-')
                    answer_unit = answer_unit.replace(match, ' ' + replacement)
            except:
                pass

    return answer_unit

def check_unit(formula_unit_dimension,answer_unit):
    """Check if input unit corresponds to formula unit."""
    #unit_correct = answer_unit == formula_unit_dimension
    try:
        # clean
        #answer_unit = clean_unit_answer(answer_unit)
        # sets (for unit sequence invariance)
        answer_units = set(answer_unit.split())
        correct_units = set(formula_unit_dimension.split())
        # check
        unit_correct = answer_units == correct_units

    except:
        unit_correct = False

    if not unit_correct:
        try:
            # check sympy unit rearrangements
            unit_correct =\
                sympy.sympify(answer_unit.replace(' ','*'))\
                           == sympy.sympify(formula_unit_dimension.replace(' ','*'))
        except:
            pass

    return unit_correct