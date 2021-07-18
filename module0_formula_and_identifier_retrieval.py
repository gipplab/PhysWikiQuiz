import csv
import string
import requests

# load cleanings
cleanings_simple = []
with open('latex_cleanings_simple.txt') as f:
    for row in csv.reader(f):
        cleanings_simple.append((row[0],row[1]))
with open('latex_cleanings_argument.txt') as f:
    cleanings_argument = f.readlines()

def clean_latex(latex_string):
    """Clean LaTeX formula for converter."""
    # simple cleanings
    for cleaning in cleanings_simple:
        latex_string = latex_string.replace(cleaning[0],cleaning[1])

    # argument cleanings
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    for cleaning in cleanings_argument:
        for letter in alphabet:
            clean = cleaning.strip('\n').replace('x', letter)
            latex_string = latex_string.replace(clean, letter)

    return latex_string

def get_Wikidata_item(Wikidata_qid):
    """Get Wikidata item from qid using https request."""

    item = requests.get("https://wikidata.org/entity/" + Wikidata_qid)
    item = item.json()['entities'][Wikidata_qid]

    return item

def get_concept_name(Wikidata_item):
    """Retrieve concept name from Wikidata item."""

    name = Wikidata_item['labels']['en']['value']

    return name

def get_defining_formula(Wikidata_item):
    """Retrieve defining formula from Wikidata item."""

    defining_formula_property = 'P2534'
    defining_formula_object = Wikidata_item['claims'][defining_formula_property]
    defining_formula_string = defining_formula_object[0]['mainsnak']['datavalue']['value']

    # clean LaTeX
    defining_formula_string = clean_latex(defining_formula_string)

    return defining_formula_string

def get_formula_identifiers(Wikidata_item):
    """Retrieve formula identifiers from Wikidata item."""

    # Populate identifier tuples list
    identifier_property_tuples = []

    # Retrieve left-hand side identifier
    left_hand_side_symbol_property_key = 'P7235' # 'in defining formula'
    identifier_name = Wikidata_item['labels']['en']['value']
    try:
        identifier_symbol = Wikidata_item['claims'][left_hand_side_symbol_property_key][0]['mainsnak']['datavalue']['value']
    except:
        identifier_symbol = None

    # clean LaTeX
    identifier_symbol = clean_latex(identifier_symbol)

    # Add left-hand side identifier to list
    identifier_property_tuples.append((identifier_symbol, identifier_name))

    # Retrieve right-hand side identifiers
    for property in ['P527','P4934']: # 'has part', 'calculated from'
        try:
            properties_object = Wikidata_item['claims'][property]
        except:
            pass
    for identifier_propery in properties_object:

        # get identifier symbol
        for property in ['P7235','P416']:
            try:
                identifier_symbol = identifier_propery['qualifiers'][property][0]['datavalue']['value']
            except:
                pass

        # get identifier name
        identifier_item_qid = identifier_propery['mainsnak']['datavalue']['value']['id']
        identifier_item = get_Wikidata_item(identifier_item_qid)
        identifier_name = identifier_item['labels']['en']['value']

        # clean LaTeX
        identifier_symbol = clean_latex(identifier_symbol)

        identifier_property_tuples.append((identifier_symbol,identifier_name))

    return identifier_property_tuples