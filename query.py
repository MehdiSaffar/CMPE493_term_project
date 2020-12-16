# Imports
import sys
import json
from tokenizer import Tokenizer
import itertools as it
import sys

def pairwise(iterable):
    it = iter(iterable)
    a = next(it, None)

    for b in it:
        yield (a, b)
        a = b

class QueryEngine:
    def __init__():
        super().__init__()
        self.inverted_index = None
        self.tokenizer = Tokenizer()

    def load_inverted_index(self, inverted_index_filename: str):
        with open(inverted_index_filename) as file:
            self.inverted_index = json.load(inverted_index_filename)
        
    @staticmethod
    def merge_by_and(posting_list_a: list, posting_list_b: list)
        a = iter(posting_list_a)
        b = iter(posting_list_b)
        while True:
            if a < b:
                next(a)
            next(it_a)
            next(it_b)
            
        pass


    def query(self, query: str):
        tokens = self.tokenizer.tokenize(query)

        lists = [self.inverted_index.get(token) or [] for token in tokens]
        final_list = it.reduce(lists, QueryEngine.merge_by_and)
        return final_list

    
    def print(self, documents: list):
        print("Your documents: ")
        for document in documents:
            print(document, end=" ")

if __name__ == '__main__':
    # init Query Engine
    query_engine = QueryEngine()

    # Load inverted index
    query_engine.load_inverted_index('./data/inverted_index.json')

    # Parse user input
    query = sys.argv[1]

    # Run the query
    doc_list = query_engine.query(query)
    
    # Show outputs
    self.print(doc_list)
    