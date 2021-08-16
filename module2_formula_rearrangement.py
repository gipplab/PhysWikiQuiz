import requests
import sympy
import random

def get_random_formula_rearrangements(defining_formula,formula_identifiers):
    """Generate random formula rearrangements using Sympy."""

    formula_rearrangements = []
    try:
        # Transform LaTeX to Sympy
        url = "https://vmext-demo.formulasearchengine.com/math/translation"
        params = {'cas': 'SymPy', 'genericExperimentalFeatures': 'true', 'latex': defining_formula}
        response = requests.post(url, params=params)
        formula_string = response.json()['result']
        # translate formula lhs and rhs
        formula_lhs_sympy = sympy.sympify(formula_string.split("==")[0])
        formula_rhs_sympy = sympy.sympify(formula_string.split("==")[1])
        # translate identifiers
        identifiers_sympy = sympy.symbols(' '.join([identifier[1] for identifier in formula_identifiers]))

        # Solve equation for different identifiers
        for identifier in identifiers_sympy:
            eq = sympy.Eq(lhs=formula_lhs_sympy,rhs=formula_rhs_sympy)
            formula_rearrangements.append((identifier,sympy.solve(eq,identifier)))

        # select random rearrangement
        selected = random.choice(formula_rearrangements)
        # update defining formula
        defining_formula_rearranged = str(selected[0]) + " = " + str(selected[1][0])
        # rearrange identifier
        lhs_identifier = []
        rhs_identifier = []
        for identifier in formula_identifiers:
            if identifier[1] == str(selected[0]):
                lhs_identifier.append(identifier)
                formula_unit_dimension = identifier[2]
            else:
                rhs_identifier.append(identifier)
        formula_identifiers_rearranged = lhs_identifier + rhs_identifier

    except:
        pass

    return defining_formula_rearranged,formula_identifiers_rearranged,formula_unit_dimension