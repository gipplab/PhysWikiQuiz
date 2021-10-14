import csv
import string
import requests
import pywikibot
import SPARQLWrapper

# load cleanings
cleanings_simple = []
with open('latex_cleanings_simple.csv') as f:
    for row in csv.reader(f):
        cleanings_simple.append((row[0],row[1]))
with open('latex_cleanings_argument.txt') as f:
    cleanings_argument = f.readlines()

def derivative_to_division(latex_string):
    deriv_start_str = '\\frac{d'
    deriv_middle_str = '}{d'
    deriv_end_str = '}'
    if deriv_start_str in latex_string and deriv_end_str in latex_string:
        start_idx = latex_string.find(deriv_start_str) + len(deriv_start_str)
        deriv_content = latex_string[start_idx:]
        deriv_content = deriv_content.replace(deriv_middle_str,'/')
        try:
            end_idx = deriv_content.find(deriv_end_str)[0]
        except:
            end_idx = deriv_content.find(deriv_end_str)
        deriv_content = deriv_content[0:end_idx].strip('}')
        if '=' in latex_string:
            equal_sign_idx = latex_string.find('=')
            latex_string = latex_string[:equal_sign_idx+1] + deriv_content
        else:
            latex_string = deriv_content
    return latex_string

def clean_latex(latex_string):
    """Clean LaTeX formula for converter."""

    # argument cleanings
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    for cleaning in cleanings_argument:
        for letter in alphabet:
            clean = cleaning.strip('\n').replace('x', letter)
            latex_string = latex_string.replace(clean, letter)

    # derivative cleanings
    #latex_string = derivative_to_division(latex_string)

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

def convert_unit_dimensions(ISQ_dimensions):
    """Convert unit from ISQ dimensions to SI units."""

    unit_dimensions = ISQ_dimensions
    # Translate into SI standard form
    # mathsf_content = re.search(r'mathsf{(.*?)}', identifier_unit_dimension)
    for expression in ['\mathsf', '{', '}']:
        unit_dimensions = unit_dimensions.replace(expression, '')

    # Map Symbol for dimension to SI unit symbol
    # See https://en.wikipedia.org/wiki/International_System_of_Quantities
    mapping = {'L': 'm', 'M': 'kg', 'T': 's', 'I': 'A', '\Theta': 'K', 'N': 'mol', 'J': 'cd'}
    for k,v in mapping.items():
        try:
            unit_dimensions = unit_dimensions.replace(k,v)
        except:
            pass
    SI_dimensions = unit_dimensions

    return SI_dimensions

def get_formula_unit_dimension(Wikidata_item):
    """Get ISQ unit dimensions of formula."""

    formula_unit_dimensions = Wikidata_item['claims']['P4020'][0]['mainsnak']['datavalue']['value'] # 'ISQ dimension'
    print('Formula_unit_available: ',formula_unit_dimensions)
    # Convert from ISQ to SI
    formula_unit_dimensions = convert_unit_dimensions(formula_unit_dimensions)

    return formula_unit_dimensions

def get_identifier_properties(Wikidata_item):

    # Populate identifier properties list of (name, symbol, unit) triples
    identifier_properties = []

    # Get identifier property claims
    property_claims = {}
    for identifier_property_key in ['P527', 'P4934', 'P7235']:  # 'has part', 'calculated from', 'in defining formula'
        try:
            property_claim = Wikidata_item['claims'][identifier_property_key]
            property_claims[identifier_property_key] = property_claim
        except:
            pass

    # Exploit identifier property claims
    for property_claim in property_claims.items():

        P = property_claim[0]
        print('Identifier properties in: ',P)
        for identifier in property_claim[1]:

            # Identifier QID
            identifier_qid = ''
            if P == 'P7235': # 'in defining formula'
                property = 'P9758' # 'symbol represents'
                try:
                    identifier_qid = identifier['qualifiers'][property][0]['datavalue']['value']['id']
                except:
                    pass
            elif P in ['P527', 'P4934']:  # 'has part', 'calculated from'
                try:
                    identifier_qid = identifier['mainsnak']['datavalue']['value']['id']
                except:
                    pass
            if identifier_qid == '':
                identifier_qid = Wikidata_item['id']

            # Identifier item
            identifier_item = get_Wikidata_item(identifier_qid)

            # Identifier name
            identifier_name = get_concept_name(identifier_item)

            # Identifier symbol
            if P == 'P7235': # 'in defining formula'
                identifier_symbol = identifier['mainsnak']['datavalue']['value']
            elif P in ['P527', 'P4934']:  # 'has part', 'calculated from'
                for property in ['P416', '7973', '2534', 'P7235']:
                # 'quantity symbol (string)', 'quantity symbol (LaTeX)', 'defining formula', 'in defining formula'
                    try:
                        identifier_symbol = identifier['qualifiers'][property][0]['datavalue']['value']
                    except:
                        pass
            # Clean LaTeX
            identifier_symbol = clean_latex(identifier_symbol)

            # Identifier unit
            identifier_unit_property = identifier_item['claims']['P4020'] # 'ISQ dimension'
            identifier_unit_dimension = identifier_unit_property[0]['mainsnak']['datavalue']['value']
            # Convert from ISQ to SI
            identifier_unit = convert_unit_dimensions(identifier_unit_dimension)

            print('Identifier property: ',(identifier_name,identifier_symbol,identifier_unit))
            identifier_properties.append((identifier_name,identifier_symbol,identifier_unit))

    return identifier_properties