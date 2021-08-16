#TODO: slow down print out process
#TODO: print out ALL retrieved variables

# ISSUES:
#TODO: module3.get_random_identifier_values
    # strToSympy parsing \frac, etc.
#TODO: module5.check_value:
    # allow percentage float tolerance for answer value

import module1_formula_and_identifier_retrieval as module1
import module2_formula_rearrangement as module2
import module3_identifier_value_generation as module3
import module4_question_text_generation as module4
import module5_solution_value_and_unit_check as module5

def generate_question(name):

    ##############################################
    # Module 1: Formula and Identifier Retrieval #
    ##############################################

    # INSTRUCTOR INPUT

    # Input Formula Concept name
    print('\nInput Formula Concept name: ',name)

    # Get QID from name
    print('\nRetrieving Wikidata item qid...\n')
    qid = module1.get_qid_sparql_with_defining_formula(name)
    print(f'Retrieving formula concept for qid >>{qid}<<...\n')

    # Get item from QID
    print('\nRetrieving Wikidata item...\n')
    item = module1.get_Wikidata_item(qid)

    # Get concept name from item
    concept_name = module1.get_concept_name(item)
    print(f'Retrieving formula concept name: >>{concept_name}<<\n')

    # System output for processing question
    print(f'Generating physics formula question for >>{concept_name}<<...\n')

    # Get defining formula
    defining_formula = module1.get_defining_formula(item)
    print(f'Retrieving defining formula: >>{defining_formula}<<\n')

    # Get formula unit dimension
    formula_unit_dimension = module1.get_formula_unit_dimension(item)

    # Get formula identifier property (name, symbol, unit) triples
    print('Retrieving formula identifier properties...\n')
    formula_identifiers = module1.get_identifier_properties(item)

    ###################################
    # Module 2: Formula Rearrangement #
    ###################################

    print('Generating formula rearrangements...\n')
    # Get formula rearrangements using Computer Algebra Systems (CAS), SymPy
    defining_formula,formula_identifiers,formula_unit_dimension = module2.get_random_formula_rearrangements(defining_formula,formula_identifiers)

    #########################################
    # Module 3: Identifier Value Generation #
    #########################################

    print('Generating random identifier values...\n')
    identifier_values = module3.get_random_identifier_values(formula_identifiers,defining_formula)

    ######################################
    # Module 4: Question Text Generation #
    ######################################

    print('Generating formula question text...\n')
    question_text = module4.get_question_text(formula_identifiers,identifier_values)
    print(question_text)

    return question_text,identifier_values,formula_unit_dimension

def correct_answer(correct_value,correct_unit,answer_input):

    # STUDENT INPUT

    print('Get student answer input...\n')
    answer_value, answer_unit = module5.get_answer_value_and_unit(answer_input)
    print(f'Answer value: {answer_value}')
    print(f'Answer unit: {answer_unit}\n')

    ###########################################
    # Module 5: Solution Value and Unit Check #
    ###########################################

    print('Check answer value and unit...\n')
    # check solution value
    value_correct = module5.check_value(correct_value,answer_value)
    print(f'Solution value: {correct_value}')
    print(f'Answer value: {answer_value}')
    if value_correct:
        print('Value answer correct!')
    else:
        print('Value answer incorrect!')

    print()
    # check solution unit
    unit_correct = module5.check_unit(correct_unit,answer_unit)
    print(f'Solution unit: {correct_unit}')
    print(f'Answer unit: {answer_unit}')
    if unit_correct:
        print('Unit answer correct!')
    else:
        print('Unit answer incorrect!')

    return value_correct,unit_correct