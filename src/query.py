# Imports
from collections import defaultdict

from numpy.core.fromnumeric import sort
from src.preprocessor import get_tf_idf_weight
import sys
import json
from .tokenizer import Tokenizer
import itertools as it
import functools as ft
import sys


class QueryEngine:
    def __init__(self):
        super().__init__()
        self.tfidf_weight = None
        self.tokenizer = Tokenizer()

    def load_tf_idf_index(self, tf_idf_index_filename: str):
        with open(tf_idf_index_filename) as file:
            self.tfidf_weight = json.load(file)
        
    def get_tf_idf_score(self, tokens):
        score = defaultdict(int)
        for token in tokens:
            for doc in self.tfidf_weight[token]:
                tfidf = self.tfidf_weight[token][doc]
                score[doc] += tfidf
        return score

    def query(self, query: str):
        tokens = self.tokenizer.tokenize(query)
        score = self.get_tf_idf_score(tokens)

        # get a list of (doc_id, score) tuples sorted by score in descending order
        docs = sorted(score.items(), key=lambda pair: pair[1], reverse=True)

        return docs

    def print(self, documents: list):
        # query-id Q0 document-id rank score STANDARD
        # print("Your documents: ")
        for document in documents:
            print(document, end=" ")

    