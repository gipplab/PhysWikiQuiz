#import latex2sympy
#from process_latex import process_sympy
from latex2sympy2 import latex2sympy

defining_formula = input('Enter defining formula: ')

try:
    formula_sympy = latex2sympy(defining_formula)
    #formula_sympy = latex2sympy.strToSympy(defining_formula)
    #formula_sympy = process_sympy(defining_formula)
    print('\nSympy format is')
    print(str(formula_sympy))
except:
    print('\nFormula could not be parsed from LaTeX to Sympy')

print('\nend')