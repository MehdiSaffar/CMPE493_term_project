# Imports
from collections import Counter, defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from numpy.core.fromnumeric import sort
from src import preprocessor
from src.preprocessor import get_tf_idf_weight
import sys
import json
from .tokenizer import Tokenizer
import itertools as it
import functools as ft
import sys
from .utils import get_tf_idf_weight, get_idf
import numpy as np


class QueryEngine:
    def __init__(self):
        super().__init__()
        self.tfidf_weight = None
        self.idf = None
        self.tokenizer = Tokenizer()

    def load_tf_idf_index(self, tf_idf_index_filename: str):
        with open(tf_idf_index_filename) as file:
            self.tfidf_weight = json.load(file)

    def load_idf_index(self, idf_filename: str):
        with open(idf_filename) as file:
            self.idf = json.load(file)
        
    def get_tf_idf_score(self, tokens):
        # calculate query vector
        tokens = list(sorted(set(tokens)))
        query_vec = [0] * len(tokens)
        for token_index, token in enumerate(tokens):
            query_vec[token_index] += 1

        for token_index, token in enumerate(tokens):
            token_idf = self.idf.get(token)
            if token_idf is None: # not sure what to do here
                query_vec[token_index] = 0
            else:
                query_vec[token_index] = get_tf_idf_weight(query_vec[token_index], token_idf)
        
        # calculate vector of each doc
        docs_vec = defaultdict(lambda: [0] * len(query_vec)) # {doc_id: [vector of the doc]}
        for token_index, token in enumerate(tokens):
            docs_containing_token = self.tfidf_weight.get(token)
            if not docs_containing_token:
                continue
        
            for doc_id, doc_tfidf in docs_containing_token.items():
                docs_vec[doc_id][token_index] = doc_tfidf

        # calculate cos similarity of query to each document
        doc_similarity = defaultdict(int)

        for doc_id, doc_vec in docs_vec.items():
            doc_similarity[doc_id] = cosine_similarity([query_vec], [doc_vec])[0][0]
        
        return doc_similarity

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

    