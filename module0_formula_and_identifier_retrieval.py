import requests

def get_Wikidata_item(Wikidata_qid):
    """Retrieve concept name from Wikidata item."""
    item = requests.get("https://wikidata.org/entity/" + Wikidata_qid)
    item = item.json()['entities'][Wikidata_qid]
    return item

def get_concept_name(Wikidata_item):
    name = Wikidata_item['labels']['en']['value']
    return name

def get_defining_formula(Wikidata_item):
    """Retrieve defining formula from Wikidata item."""
    defining_formula_property = 'P2534'
    defining_formula_object = Wikidata_item['claims'][defining_formula_property]
    defining_formula_string = defining_formula_object[0]['mainsnak']['datavalue']['value']
    return defining_formula_string

def get_formula_identifiers(Wikidata_item):
    """Retrieve formula identifiers from Wikidata item."""
    identifier_property_keys = ['P527','P4934'] # 'has part', 'calculated from'
    for property in identifier_property_keys:
        try:
            properties_object = Wikidata_item['claims'][property]
        except:
            pass
    identifier_property_tuples = []
    for identifier_propery in properties_object:
        identifier_symbol = identifier_propery['qualifiers']['P7235'][0]['datavalue']['value']
        # TODO: find name
        identifier_name = None
        identifier_property_tuples.append((identifier_symbol,identifier_name))
    return identifier_property_tuples