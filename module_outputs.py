#TODO: slow down print out process
#TODO: print out ALL retrieved variables

# ISSUES:
#TODO: module3.get_random_identifier_values
    # strToSympy parsing \frac, etc.
#TODO: module5.check_value:
    # allow percentage float tolerance for answer value

import benchmark_cache
import module1_formula_and_identifier_retrieval as module1
import module2_formula_rearrangement as module2
import module3_identifier_value_generation as module3
import module4_question_text_generation as module4
import module5_solution_value_and_unit_check as module5
import module6_explanation_text_generation as module6

def generate_question(name):

    ##############################################
    # Module 1: Formula and Identifier Retrieval #
    ##############################################

    # INSTRUCTOR INPUT

    # Input Formula Concept name
    print('\nInput Formula Concept name: ',name)

    # If not QID, get QID from name
    print('\nRetrieving Wikidata item qid...\n')
    if name.startswith('Q') and name[1:].isnumeric():
        qid = name
    else:
        qid = module1.get_qid_sparql_with_defining_formula(name)
    print(f'Retrieving formula concept for qid >>{qid}<<...\n')

    # Get item from QID
    print('\nRetrieving Wikidata item...\n')
    # Check if in benchmark sample dataset
    try:
        sample_items = benchmark_cache.load_benchmark_dump()
        item = sample_items[qid]
    except:
        item = None
    # Load item (json) data
    try:
        if item is None:
            item = module1.get_Wikidata_item(qid)
    except:
        return 'No Wikidata item with formula found', None, None, ''

    # Get concept name from item
    #concept_name = module1.get_concept_name(item)
    #print(f'Retrieving formula concept name: >>{concept_name}<<\n')

    # System output for processing question
    print(f'Generating physics formula question for >>{name}<<...\n')

    # Get defining formula
    try:
        defining_formula = module1.get_defining_formula(item)
    except:
        return 'Defining formula retrieval unsuccessful', None, None, ''
    print(f'Retrieved defining formula: >>{defining_formula}<<\n')

    # Get formula unit dimension
    #formula_unit_dimension = module1.get_formula_unit_dimension(item)

    # Get formula identifier property (name, symbol, unit) triples
    print('Retrieving formula identifier properties...\n')
    try:
        formula_identifiers = module1.get_identifier_properties(item)
    except:
        return 'Identifier property retrieval unsuccessful', None, None, ''
    if len(formula_identifiers) == 0:
        return 'Identifier property retrieval unsuccessful', None, None, ''

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
    try:
        identifier_values = module3.get_random_identifier_values(formula_identifiers,defining_formula)
    except:
        return 'Identifier value generation unsuccessful', None, None, ''
    if len(identifier_values) == 0:
        return 'Identifier value generation unsuccessful', None, None, ''

    ######################################
    # Module 4: Question Text Generation #
    ######################################

    print('Generating formula question text...\n')
    question_text = module4.get_question_text(formula_identifiers,identifier_values)
    print(question_text)

    #########################################
    # Module 6: Explanation Text Generation #
    #########################################

    explanation_text = module6.generate_explanation_text(qid,defining_formula,formula_identifiers,identifier_values)

    return question_text,identifier_values,formula_unit_dimension,explanation_text

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