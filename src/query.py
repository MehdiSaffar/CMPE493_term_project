# Imports
from collections import Counter, defaultdict
from sklearn.metrics.pairwise import cosine_similarity
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
        # calculate query vector
        tokens = list(sorted(set(tokens)))
        query_vec = [1] * len(tokens)

        # calculate vector of each doc
        docs_vec = defaultdict(lambda _: [0] * len(query_vec)) # {doc_id: [vector of the doc]}
        for token_index, token in enumerate(tokens):
            docs_containing_token = self.tfidf_weight.get(token)
            if not docs_containing_token:
                continue
        
            for doc_id, doc_tfidf in docs_containing_token.items():
                docs_vec[doc_id][token_index] = doc_tfidf

        # calculate cos similarity of query to each document
        doc_similarity = defaultdict(int)

        for doc_id, doc_vec in docs_vec.items():
            doc_similarity[doc_id] = cosine_similarity([query_vec], [doc_vec])
        
        return doc_similarity

        # a b c -> 1 1 1
        # a b c -> 1 1 1 değil!




            










        ########
        # [a, a, b, c, b, a, b, c] -> [a, b, c] <-- index should be sorted alphabetically

        #                             [3, 2, 2] <-- query vector
        #                             [3, 2, 2] <-- doc 1 vector
        #                             [x, y, z] <-- doc 2 vector
        #                             [3, 2, 2]
        #                             [3, 2, 2]
        #                             [3, 2, 2]
        
        # tokens = [a, a, b, c, b, a, b, c]
        # sorted(tokens) = [a, a, a, b, b, b, c, c]
        # Counter(sorted(tokens)) = {a:3, b: 3, c:2}
        # Counter(sorted(tokens)).values() = [3, 3, 2]

        # query_vec = list(Counter(sorted(tokens)).values())

        # docs_vec = []

        # for doc in docs:
        #     doc = dict.fromkeys(tokens_vec.keys())
        #     for token in tokens:
                
        # 
# {a: 0 b:0 c:0} doc1_init
# {a: 5 b:3 c:0} doc1_finished
# {a: 1.3, b: 2.4, c: 3.0} 
# [doc1, doc2, doc3, ]
# {a: 0, b:5, c:7}

        # tokens = [a, a, b, c, b, a, b, c]
        # sorted(tokens) = [a, a, a, b, b, b, c, c]
        # Counter(sorted(tokens)) = {a:3, b: 3, c:2}
        # Counter(sorted(tokens)).values() = [3, 3, 2]

        # query_vec = list(Counter(sorted(tokens)).values())

       
        # docs_vec = defaultdict(list)
        # for token in tokens:
        #     # assume token is 'post-infection'
        #     # it may not appear in our tf-idf dictionary as a key
        #     # if that's the case, score of will not be incremented.
        #     if token not in self.tfidf_weight:
        #         continue

        #     for doc in self.tfidf_weight[token]:
        #         tfidf = self.tfidf_weight[token][doc]
        #         docs_vec[doc].append(tfidf)



            # query [hello, there, how, are, you,  general, kenobi]
            # query [1,     1,     1,   1,    52,  96,       4    ]
            # doc1: [1,     0,     4,   0,    31,  69,       4    ]
            # doc1: [2,     1,     0,   1,     3,  696,      4    ]
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

    