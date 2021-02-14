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

    def get_bm25_score(self, tokens):

        with open("./data/tf.json") as file:
            tf = json.load(file)
        
        with open("./data/doc_lengths_normalized.json") as file:
            normalized_doc_lengths = json.load(file)
        
        
        # scores will be stored in a dictionary. e.g. key: doc-id, value: bm25_score
        scores = dict()
        
        # open for experimentation.
        k = 1.5
        b = 0.75

        for doc_id, normalized_doc_length in normalized_doc_lengths.items():
            sum_of_query_word_scores = 0

            for query_word in tokens:
                idf = self.idf.get(query_word)
                if idf is None:
                    # this means, query word does not exist in vocabulary.
                    idf = get_idf(len(normalized_doc_lengths), 0)
                
                temp = tf.get(query_word)
                if temp is None:
                    # if query word does not appear in the corpus, tf value will be 0.
                    continue
                
                tf_val = temp.get(doc_id, 0) # if query word does not appear in that doc, tf will be 0
                if tf_val == 0:
                    continue
                
                '''
                #BM25 - robertson
                # check the denominator if it becomes zero
                # if it becomes zero, continue with the next query word
                denominator = tf_val + (k * ( 1 - b + b * normalized_doc_length))
                if denominator == 0:
                    continue

                # perform the summation of this query word
                sum_of_query_word_scores += idf * ( (tf_val * (k+1)) / denominator)
                '''

                # Bm25+ 
                # check the denominator if it becomes zero
                # if it becomes zero, continue with the next query word
                denominator = tf_val + (k * ( 1 - b + b * normalized_doc_length))
                if denominator == 0:
                    continue

                # perform the summation of this query word
                # alpha value is special for bm25+ model. default value is suggested to be 1.
                alpha = 1
                sum_of_query_word_scores += idf * ( (tf_val * (k+1)) / denominator + alpha)

                '''
                # bm25L
                alpha = 0.5
                c = tf_val / ( 1 - b + b * normalized_doc_length)
                sum_of_query_word_scores += idf * ( (k + 1) * (c + alpha) / (k + c + alpha) )
                '''
                
            # update that documents score
            scores[doc_id] = sum_of_query_word_scores
        
        return scores

    def query(self, query: str):
        tokens = self.tokenizer.tokenize(query)
        score = self.get_bm25_score(tokens)

        # get a list of (doc_id, score) tuples sorted by score in descending order
        docs = sorted(score.items(), key=lambda pair: pair[1], reverse=True)

        return docs

    def print(self, documents: list):
        # query-id Q0 document-id rank score STANDARD
        # print("Your documents: ")
        for document in documents:
            print(document, end=" ")
