import pandas as pd
import requests

# INIT

# set paths
evaluation_path = "Identifier_Unit_Wikidata_Properties_evaluation.csv"
correspondence_path = "GoldID-QID_correspondence.csv"

# open csv tables
evaluation_table = pd.read_csv(evaluation_path,delimiter=";")
correspondence_table = pd.read_csv(correspondence_path,delimiter=";")
new_evaluation_table = evaluation_table

# DEFINE

def get_qid(goldid):
    """Map GoldID to QID."""

    # https://stackoverflow.com/questions/61964973/pandas-get-column-value-where-row-matches-condition
    # https://www.interviewqs.com/ddi-code-snippets/rows-cols-python
    # https://www.geeksforgeeks.org/select-rows-columns-by-name-or-index-in-pandas-dataframe-using-loc-iloc/

    condition = correspondence_table['GoldID'] == goldid
    row = correspondence_table[condition]
    qid = row.values[0][1]
    return qid

# test 'get_qid' function
# qid = get_qid(320)

def write_formula_qid(row):
    """Write QID in 'Formula QID' column."""

    goldid = row[1]['GoldID']
    qid = get_qid(goldid)
    print(qid)

    #TODO:
    # write ...
    # ...

def get_wikidata_item(qid):
    """Return Wikidata item data for QID."""
    # https://www.wikidata.org/wiki/Special:EntityData/QID.json
    item = requests.get("https://wikidata.org/entity/" + qid)
    return item.json()['entities'][qid]

# test 'get_wikidata_item' function
# item = get_wikidata_item("Q11376")

def write_unit_info_Wikidata(row):
    """Write unit infos in respective columns."""

    qid = row[1]['Identifier QID']
    item = get_wikidata_item(qid)
    claims = item['claims']

    def get_value(claims,property):
        try:
            value = claims[property][0]['mainsnak']['datavalue']['value']
        except:
            value = ''
        return value

    # get unit Wikidata infos
    isq_dim = get_value(claims,property='P4020')
    print(isq_dim)
    rec_unit_meas = get_value(claims,property='8111')
    print(rec_unit_meas)
    num_val = get_value(claims,property='P1181')
    print(num_val)

    #TODO:
    # write ...
    # ...

# EXECUTE

# iterate through table rows
for row in evaluation_table.iterrows():
    write_formula_qid(row)
    write_unit_info_Wikidata(row)

pd.write_csv("Identifier_Unit_Wikidata_Properties_evaluation(filled).csv",delimiter=";")

print("end")