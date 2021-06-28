from module0_formula_and_identifier_retrieval import get_Wikidata_item

unit_property_key = 'P4020'

def convert_unit_dimensions(ISQ_dimensions):
    """Convert unit from ISQ dimensions to SI units."""

    return SI_units

def get_formula_unit_dimension(Wikidata_item):
    """Get ISQ unit dimensions of formula."""

    formula_unit_dimensions = Wikidata_item['claims'][unit_property_key][0]['mainsnak']['datavalue']['value']

    return formula_unit_dimensions

def get_identifier_unit_dimensions(Wikidata_item):
    """Get ISQ unit dimensions of identifiers."""

    identifier_unit_dimensions = []

    # Retrieve right-hand side identifiers
    identifier_property_keys = ['P527', 'P4934']  # 'has part', 'calculated from'
    for property in identifier_property_keys:
        try:
            properties_object = Wikidata_item['claims'][property]
        except:
            pass

    for identifier_propery in properties_object:

        # get identifier unit
        identifier_item_qid = identifier_propery['mainsnak']['datavalue']['value']['id']
        identifier_item = get_Wikidata_item(identifier_item_qid)
        identifier_unit_property = identifier_item['claims'][unit_property_key]
        identifier_unit_dimension = identifier_unit_property[0]['mainsnak']['datavalue']['value']
        identifier_unit_dimensions.append(identifier_unit_dimension)

    return identifier_unit_dimensions

def update_identifiers_dict(formula_identifiers,formula_unit_dimension,identifier_unit_dimensions):
    """Update identifiers dict with units."""

    updated_formula_identifiers = []
    unit_dimensions = [formula_unit_dimension]
    unit_dimensions.extend(identifier_unit_dimensions)
    identifier_index = 0
    for identifier_tuple in formula_identifiers:
        identifier_triple = (identifier_tuple[0],identifier_tuple[1],unit_dimensions[identifier_index])
        updated_formula_identifiers.append(identifier_triple)
        identifier_index += 1

    return updated_formula_identifiers