import pandas as pd

import itertools
import random

import sympy
from latex2sympy2 import latex2sympy

import requests

import module1_formula_and_identifier_retrieval as module1
import module3_identifier_value_generation as module3
import module6_explanation_text_generation as module6

filename = 'unit_test_module_workflow_empty.csv'

modes = ['latex2sympy','vmext']
mode = modes[0]

def write_cell(col_name,row_idx,content):
    table.loc[table.index[row_idx],col_name] = str(content)

table = pd.read_csv(filename,delimiter=';')
qids = table['QID']

for idx in range(len(qids)):

    # QID
    qid = qids[idx]
    print(qid)
    write_cell('QID',idx,qid)

    # Item
    try:
        item = module1.get_Wikidata_item(qid)
    except:
        pass

    # Name
    try:
        name = module1.get_concept_name(item)
        print(name)
    except:
        name = 'N/A'
    write_cell('Name', idx, name)

    # Formula
    try:
        defining_formula = module1.get_defining_formula(item)
        print(defining_formula)
    except:
        defining_formula = 'N/A'
    write_cell('Formula', idx, defining_formula)

    # Properties
    def get_identifier_property_keys(item):

        keys = ''
        for identifier_property_key in ['P527', 'P4934', 'P7235']:
            try:
                item['claims'][identifier_property_key] is not None
                keys += identifier_property_key + ', '
            except:
                pass

        return keys[:-2]
    try:
        identifier_property_keys = get_identifier_property_keys(item)
        print(identifier_property_keys)
    except:
        identifier_property_keys = 'N/A'
    write_cell('Properties', idx, identifier_property_keys)

    # Formula unit
    try:
        formula_unit = module1.get_formula_unit_dimension(item)
        print(formula_unit)
    except:
        formula_unit = 'N/A'
    write_cell('Formula unit', idx, formula_unit)

    # Formula sympy
    try:
        if mode == 'latex2sympy':
            formula_sympy = latex2sympy(defining_formula)
        elif mode == 'vmext':
            formula_sympy = module3.get_sympy_from_latex_using_vmext_api(defining_formula)
        print(formula_sympy)
    except:
        formula_sympy = 'N/A'
    write_cell('Formula sympy', idx, formula_sympy)

    # Identifiers
    try:
        formula_identifiers = module1.get_identifier_properties(item)
        print(formula_identifiers)
    except:
        formula_identifiers = 'N/A'
    write_cell('Identifiers', idx, str(formula_identifiers))

    # Identifiers sympy
    try:
        identifiers_sympy = sympy.symbols(' '.join([identifier[1] for identifier in formula_identifiers]))
        print(identifiers_sympy)
    except:
        identifiers_sympy = 'N/A'
    write_cell('Identifiers sympy', idx, identifiers_sympy)

    # Sympy solve
    def get_sympy_solve(defining_formula,identifiers_sympy):

        formula_rearrangements = []
        # Transform LaTeX to Sympy
        url = "https://vmext-demo.formulasearchengine.com/math/translation"
        params = {'cas': 'SymPy', 'genericExperimentalFeatures': 'true', 'latex': defining_formula}
        response = requests.post(url, params=params)
        formula_string = response.json()['result']
        # translate formula lhs and rhs
        formula_lhs_sympy = sympy.sympify(formula_string.split("==")[0])
        formula_rhs_sympy = sympy.sympify(formula_string.split("==")[1])

        # Solve equation for different identifiers
        for identifier in identifiers_sympy:
            eq = sympy.Eq(lhs=formula_lhs_sympy, rhs=formula_rhs_sympy)
            formula_rearrangements.append((identifier, sympy.solve(eq, identifier)))

        return formula_rearrangements
    try:
        sympy_solve = get_sympy_solve(defining_formula,identifiers_sympy)
        print(sympy_solve)
    except:
        sympy_solve = 'N/A'
    write_cell('Sympy solve', idx, sympy_solve)

    # Sympy rhs
    def get_sympy_rhs(formula_sympy,formula_identifiers):

        rhs_identifier_values = []

        # define limit for right-hand side integer value
        lower_val_limit = 1
        upper_val_limit = 10

        # generate random integers for right-hand side identifiers
        for _ in itertools.repeat(None, len(formula_identifiers) - 1):
            rhs_identifier_values.append(random.randint(lower_val_limit, upper_val_limit))

        # substitute generated random values to calculate left-hand side
        identifier_index = 0
        for identifier_sympy in identifiers_sympy:
            if identifier_index != 0:  # lhs identifier
                formula_sympy = formula_sympy.subs(identifier_sympy, rhs_identifier_values[identifier_index - 1])
            identifier_index += 1
        try:
            lhs_identifier_value = formula_sympy.rhs
        except:
            lhs_identifier_value = formula_sympy

        return lhs_identifier_value
    try:
        sympy_rhs = get_sympy_rhs(formula_sympy,formula_identifiers)
        print(sympy_rhs)
    except:
        sympy_rhs = 'N/A'
    write_cell('Sympy rhs',idx,sympy_rhs)

    # Explanation
    try:
        identifier_values = module3.get_random_identifier_values(formula_identifiers, defining_formula)
        explanation_text = module6.generate_explanation_text(qid,defining_formula,formula_identifiers,identifier_values)
        print(explanation_text)
    except:
        explanation_text = 'N/A'
    write_cell('Explanation', idx, explanation_text)

    # Empty line
    print()

table.to_csv('unit_test_module_workflow_explanation_generated_' + mode + '.csv')

print('end')