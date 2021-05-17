import module0_formula_and_identifier_retrieval as module0
import module1_identifier_unit_retrieval as module1
import module2_formula_rearrangement as module2
import module3_identifier_value_generation as module3
import module4_question_text_generation as module4
import module5_solution_value_and_unit_check as module5

# Instructor input
qid = input("Input formula question QID")
# Formula question QID: 'Q11376'
concept_name = module0.get_concept_name(qid)
print('Generating physics formula question for >>{}<<...'.format(concept_name))
# System output: 'Generating physics formula question for >>acceleration<<...'

# Module 0: Formula and Identifier Retrieval
defining_formula = module0.get_defining_formula(qid)
# 'defining formula' (P2534)
# -> 'a = dv/dt'
formula_identifiers = module0.get_formula_identifiers(qid)
# a: 'acceleration' (Q11376)
# v: 'velocity' (Q11465)
# t: 'duration' (Q2199864)

# Module 1: Identifier unit retrieval
unit_dimensions = module1.get_unit_dimensions(qid)
# 'ISQ dimension' property (P4020)
# -> '\mathsf{L} \mathsf{T}^{-2}''

# Module 2: Fomula rearrangement
formula_rearrangement = module2.get_random_formula_rearrangement(defining_formula)
# CAS formula rearrangements
# ->
# 'F = m a'
# 'm = F/a'
# 'a = F/m'

# Module 3: Identifier value generation
identifier_values = module3.get_random_identifier_values(formula_rearrangement)
# {F,m,a} = {6,2,3}; {6,3,2}, ...
# (randomize)

# Module 4: Question text generation
question_text = module4.get_question_text(formula_identifiers,identifier_values,unit_dimensions)
# a) 'What is the force F given mass m = 2 kg and acceleration a = 3 m/s^2 ?'
# b) 'What is the mass m given force F = 6 N and acceleration a = 3 m/s^2 ?'
# c) 'What is the acceleration a given Force F = 6 N and mass m = 2 kg ?'
# (randomize)

# Student input
identifier_name, identifier_symbol = module4.get_lhs_identifier_properties(formula_rearrangement,formula_identifiers)
answer_input = input(f'{identifier_name} {identifier_symbol} = ?')
answer_value = module4.get_answer_value(answer_input)
answer_unit = module4.get_answer_unit(answer_input)
# a) 'Force F = 6 N'
# b) c) ...

# Module 5: Solution value and unit check
# check solution value
value_correct = module5.check_value(formula_rearrangement,answer_value)
if value_correct:
    print("Value correct")
else:
    print("Value incorrect")
# 'correct'
# check solution unit
unit_correct = module5.check_unit(formula_rearrangement,answer_value)
if unit_correct:
    print("Unit correct")
else:
    print("Unit incorrect")
# 'correct'

print("end")