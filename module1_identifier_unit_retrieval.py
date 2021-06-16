from module0_formula_and_identifier_retrieval import get_Wikidata_item

def get_formula_unit_dimensions(Wikidata_item):
    """Get ISQ unit dimensions of formula."""

    unit_property_key = 'P4020'
    formula_unit_dimensions = Wikidata_item['claims'][unit_property_key][0]['mainsnak']['datavalue']['value']

    return formula_unit_dimensions

def get_identifier_unit_dimensions(defining_formula,formula_identifiers,formula_unit_dimensions):
    """Get ISQ unit dimensions of identifiers."""
    identifier_unit_dimensions = []
    for formula_identifier in formula_identifiers:
        # TODO: how to retrieve identifier unit from identifier (symbol,name)
        #  and formula unit dimensions
        identifier_unit_dimension = None
        identifier_unit_dimensions.append(identifier_unit_dimension)

    return identifier_unit_dimensions