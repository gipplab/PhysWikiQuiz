import pandas as pd
import json
import module1_formula_and_identifier_retrieval as module1

sample_IDs_path = "evaluation/sample_IDs.csv"
benchmark_dump_path = "evaluation/benchmark_dump/sample_items.json"

def get_sample_qids():
    sample_IDs = pd.read_csv(sample_IDs_path,sep=';')
    QIDs = list(sample_IDs['QID'])
    return QIDs

def save_benchmark_dump():
    errors = []
    QIDs = get_sample_qids()
    sample_items = {}
    for QID in QIDs:
        print(QID)
        item = module1.get_Wikidata_item(QID)
        sample_items[QID] = item
    with open(benchmark_dump_path,'w') as f:
        json.dump(sample_items,f)
    print(errors)
    return 0

def load_benchmark_dump():
    with open(benchmark_dump_path,'r') as f:
        sample_items = json.load(f)
    return sample_items

#save_benchmark_dump()
#load_benchmark_dump()

#print()