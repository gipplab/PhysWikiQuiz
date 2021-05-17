import requests

def get_concept_name(qid):
    """Description."""
    item = requests.get("https://wikidata.org/entity/" + qid)
    item = item.json()['entities'][qid]
    name = item['labels']['en']['value']
    return name

def get_defining_formula(qid):
    """Description."""
    return defining_formula

def get_formula_identifiers(qid):
    """Description."""
    return formula_identifiers