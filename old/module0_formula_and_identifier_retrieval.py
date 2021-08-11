import csv
import string
import requests
import pywikibot
import SPARQLWrapper

# load cleanings
cleanings_simple = []
with open('../latex_cleanings_simple.csv') as f:
    for row in csv.reader(f):
        cleanings_simple.append((row[0],row[1]))
with open('../latex_cleanings_argument.txt') as f:
    cleanings_argument = f.readlines()

def clean_latex(latex_string):
    """Clean LaTeX formula for converter."""

    # argument cleanings
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    for cleaning in cleanings_argument:
        for letter in alphabet:
            clean = cleaning.strip('\n').replace('x', letter)
            latex_string = latex_string.replace(clean, letter)

    # simple cleanings
    for cleaning in cleanings_simple:
        latex_string = latex_string.replace(cleaning[0],cleaning[1])

    return latex_string

# get Wikidata qid from name using pywikibot
def get_qid_pywikibot(name):
    try:
        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, name)
        item = pywikibot.ItemPage.fromPage(page)
        qid = item.id
    except:
        qid = 'N/A'
    return qid

def get_sparql_results(sparql_query_string):
    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query_string)
    try:
        # stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
        sparql.setReturnFormat(SPARQLWrapper.JSON)
        result = sparql.query().convert()
    except:
        result = None
    return result

def get_sparql_query_string(name):

    sparql_query_string = """SELECT distinct ?item ?itemLabel ?itemDescription WHERE{  
            ?item ?label "%s"@en. 
            ?article schema:about ?item .
            ?article schema:inLanguage "en" .
            ?article schema:isPartOf <https://en.wikipedia.org/>. 
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }    
            }""" % name

    return sparql_query_string

def get_qid_sparql(name):

    sparql_query_string = get_sparql_query_string(name)
    sparql_results = get_sparql_results(sparql_query_string)

    qid_results = []
    try:
        for result in sparql_results['results']['bindings']:
            try:
                desc = result['itemDescription']['value']
                if desc != 'Wikimedia disambiguation page':
                    url = result['item']['value']
                    qid = url.split("/")[-1]
                    qid_results.append(qid)
            except:
                pass
    except:
        pass

    if len(qid_results) > 0:
        qid = qid_results[0]  # take first result
    else:
        qid = 'N/A'

    return qid

def get_qid_sparql_with_defining_formula(name):

    sparql_query_string = get_sparql_query_string(name)
    sparql_results = get_sparql_results(sparql_query_string)

    qid_results = []
    try:
        for result in sparql_results['results']['bindings']:
            try:
                url = result['item']['value']
                qid = url.split("/")[-1]
                item = get_Wikidata_item(qid)
                try:
                    defining_formula = item['claims']['P2534']
                except:
                    defining_formula = 'N/A'
                if defining_formula != 'N/A':
                    qid_results.append(qid)
            except:
                pass
    except:
        pass

    if len(qid_results) > 0:
        qid = qid_results[0]  # take first result
    else:
        qid = 'N/A'

    return qid

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
    for property in ['P527','P4934','P9758']: # 'has part', 'calculated from', 'symbol represents'
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