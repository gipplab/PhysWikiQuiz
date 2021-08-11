import itertools
import random
#import latex2sympy
from latex2sympy2 import latex2sympy
import sympy

def get_random_identifier_values(formula_identifiers,defining_formula):
    """Generate random identifier integer values."""

    rhs_identifier_values = []

    # define limit for right-hand side integer value
    lower_val_limit = 1
    upper_val_limit = 10

    # generate random integers for right-hand side identifiers
    for _ in itertools.repeat(None, len(formula_identifiers)-1):
        rhs_identifier_values.append(random.randint(lower_val_limit,upper_val_limit))

    # generate resulting value for left-hand side identifier
    #defining_formula = 'x = y'
    # TODO: generalize
    identifiers_sympy = sympy.symbols(' '.join([identifier[1] for identifier in formula_identifiers]))
    #identifiers_sympy = sympy.symbols('a v t')

    # convert LaTeX to Sympy format
    # formula_sympy = latex2sympy.strToSympy(defining_formula)
    formula_sympy = latex2sympy(defining_formula)

    # substitute generated random values to calculate left-hand side
    identifier_index = 0
    for identifier_sympy in identifiers_sympy:
        if identifier_index != 0:#lhs identifier
            formula_sympy = formula_sympy.subs(identifier_sympy,rhs_identifier_values[identifier_index-1])
        identifier_index += 1
    try:
        lhs_identifier_value = formula_sympy.rhs
    except:
        lhs_identifier_value = formula_sympy

    identifier_values = [str(lhs_identifier_value)]
    identifier_values.extend(rhs_identifier_values)

    return identifier_values