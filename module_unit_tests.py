import unittest

from old import module0_formula_and_identifier_retrieval

import pandas as pd

# Python Tutorial: Unit Testing Your Code with the unittest Module:
#https://www.youtube.com/watch?v=6tNS--WetLI

# Retrieve sample QIDs
sample_IDs_filepath = r'evaluation\sample_IDs.csv'
QIDs_column_name = 'QID'

def get_sample_QIDs():
    sample_IDs_table = pd.read_csv(sample_IDs_filepath,delimiter=';')
    sample_QIDs = list(sample_IDs_table[QIDs_column_name])
    return sample_QIDs

class TestModules(unittest.TestCase):

    # TEST MODULE0
    def test_module0(self):
        #qid = 'Q11376'
        #sample_QIDs = [qid]
        sample_QIDs = get_sample_QIDs()
        for qid in sample_QIDs:
            Wikidata_item = module0_formula_and_identifier_retrieval \
                .get_Wikidata_item(qid)

            self.assertIsNotNone(Wikidata_item)
            #self.assertIsNotNone(module0_formula_and_identifier_retrieval
            #             .get_concept_name(Wikidata_item))

    # TEST MODULE1
    def test_module1(self):
        # TODO: insert code for unit test of module1 here
        pass

if __name__ == '__main__':
    unittest.main()