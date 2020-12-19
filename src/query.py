# Imports
import sys
import json
from .tokenizer import Tokenizer
import itertools as it
import functools as ft
import sys

class QueryEngine:
    def __init__(self):
        super().__init__()
        self.inverted_index = None
        self.tokenizer = Tokenizer()

    def load_inverted_index(self, inverted_index_filename: str):
        with open(inverted_index_filename) as file:
            self.inverted_index = json.load(file)
        
    @staticmethod
    def merge_by_and(posting_list_a: list, posting_list_b: list):
        a_set = set(posting_list_a)
        b_set = set(posting_list_b)
        return list(a_set.intersection(b_set))


    def query(self, query: str):
        tokens = self.tokenizer.tokenize(query)

        lists = [self.inverted_index.get(token) or [] for token in tokens]
        final_list = ft.reduce(QueryEngine.merge_by_and, lists)
        return final_list

    def print(self, documents: list):
        print("Your documents: ")
        for document in documents:
            print(document, end=" ")

    