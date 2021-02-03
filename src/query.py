# Imports
from collections import Counter, defaultdict
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
import math


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
        # Query vector should contain the number of occurrance of that token.
        unique_tokens = list(sorted(set(tokens)))
        query_vec = [0] * len(unique_tokens)
        for token in tokens:
            token_index = unique_tokens.index(token)
            query_vec[token_index] += 1
        tokens = unique_tokens # since remaining code follows "tokens" name.

        for token_index, token in enumerate(tokens):
            token_idf = self.idf.get(token)
            if token_idf is None:  # not sure what to do here
                query_vec[token_index] = 0
            else:
                if query_vec[token_index] != 0:
                    query_vec[token_index] = get_tf_idf_weight(query_vec[token_index], token_idf)

        # query1 1, 0, 1
        # doc1   2, 5, 0, 0...
        # doc2   2, 0, 3, 0...

        # query 1 1 1 | magnitude of entire vector = sqrt(1 1 1 0 0 0 0 ...)
        # doc1  5 0 3 | magnitude of entire vector = sqrt(5 0 3 5 3 1 9...)
        # doc2  0 2 2 |

        # calculate vector of each doc
        docs_vec_mag = defaultdict(int)
        docs_vec = defaultdict(lambda: [0] * len(query_vec))  # {doc_id: [vector of the doc]}
        for token_index, token in enumerate(tokens):
            docs_containing_token = self.tfidf_weight.get(token)
            if not docs_containing_token:  # not sure
                continue

            for doc_id, doc_tfidf in docs_containing_token.items():
                docs_vec[doc_id][token_index] = doc_tfidf

        for token, token_docs in self.tfidf_weight.items():
            for doc_id, doc_tfidf in token_docs.items():
                docs_vec_mag[doc_id] += doc_tfidf ** 2

        for doc_id, doc_vec_mag in docs_vec_mag.items():
            docs_vec_mag[doc_id] = math.sqrt(doc_vec_mag)

        # calculate cos similarity of query to each document
        doc_similarity = defaultdict(int)

        for doc_id, doc_vec in docs_vec.items():
            doc_similarity[doc_id] = np.dot(doc_vec, query_vec) / (docs_vec_mag[doc_id] * np.linalg.norm(query_vec))
            # if doc_similarity[doc_id] == 1:
            #     print(np.dot(doc_vec, query_vec), docs_vec_mag[doc_id], np.linalg.norm(query_vec))
            # doc_similarity[doc_id] = cosine_similarity([query_vec], [doc_vec])[0][0]

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
