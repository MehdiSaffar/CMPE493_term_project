import json
import string
from collections import defaultdict

import contractions
import nltk
import nltk.tokenize
import pandas as pd
from nltk.corpus import wordnet as wn
from pandarallel import pandarallel
from .tokenizer import Tokenizer
import math
import copy
from .utils import serialize_sets, get_tf_idf_weight, get_idf

# pandarallel.initialize(progress_bar=True)


class Preprocessor:
    def __init__(self) -> None:
        super().__init__()
        self.tf = defaultdict(lambda: defaultdict(int))
        self.idf = defaultdict(lambda: defaultdict(int))
        self.tfidf_weight = defaultdict(lambda: defaultdict(int))

    def parse_eval_file(self, eval_filename: str):
        df = pd.read_csv(eval_filename, delim_whitespace=True, names="topic_id iteration_id doc_id relevance".split())
        df = df.convert_dtypes()
        return df
    
    def tokenize(self, df: pd.DataFrame, col: str):
        tokenizer = Tokenizer()
        def tokenize_apply(value: str):
            return tokenizer.tokenize(value)

        return df[col].apply(tokenize_apply)


    def run(self, metadata_filename: str):
        # print('=> Loading metadata file...')
        # doc_df = pd.read_csv(metadata_filename)
        # doc_df = doc_df[['cord_uid', 'title', 'abstract']]
        # doc_df = doc_df.rename({'cord_uid': 'id'}, axis=1)
        # print('Loaded metadata file')

        # print('=> Saving metadata feather file...')
        # doc_df.to_feather('./data/metadata.feather')
        # print('Saved metadata feather file...')
        # return 

        print('=> Loading metadata feather file...')
        doc_df = pd.read_feather(metadata_filename)
        print('Loaded metadata feather file...')

        eval_df = self.parse_eval_file('./data/eval.txt')

        doc_df = pd.merge(doc_df, eval_df['doc_id'], how='inner', left_on='id', right_on='doc_id')
        doc_df = doc_df.drop('doc_id', axis=1, errors='ignore')
        doc_df = doc_df.fillna('')
        doc_df = doc_df.drop_duplicates(subset=['id'])
        doc_df = doc_df.reset_index(drop=True)

        doc_df['text'] = doc_df['title'] + ' ' + doc_df['abstract']

        # print(len(doc_df))
        # return

        doc_df = doc_df.convert_dtypes()
        # doc_df = doc_df.head(37924)
        #doc_df = doc_df.head(5_000)
        print('=> Tokenizing documents...')
        doc_df['tokens'] = self.tokenize(doc_df, 'text')
        print('Tokenized documents')

        
        print('=> Building tf-idf index...')
        # tf(t, d) number of times t occurs in d, mapping from t => d
        # df(t): number of docs that contain t (at least once)
        # idf(t): log_10(N/df(t)) where N is total number of documents in the collection
        # tf-idf_weight(t,d): (1 + log_10(tf(t,d))) * log_10(N / df(t))
        #                     (1 + log_10(tf(t,d))) * idf(t)

        def add_to_tf_apply(row: pd.Series):
            for token in row['tokens']:    
                self.tf[token][row['id']] += 1

        doc_df[['id', 'tokens']].apply(add_to_tf_apply, axis=1)

        self.idf = defaultdict(float)
        self.tfidf_weight = copy.deepcopy(self.tf)
        for token, docs in self.tf.items():
            self.idf[token] = get_idf(len(doc_df), len(docs))
            for doc, tf in docs.items():
                self.tfidf_weight[token][doc] = get_tf_idf_weight(tf, self.idf[token])

        print('Built tf-idf index')

    def save(self, tfidf_weight_filename: str, idf_filename: str):
        print('=> Saving tfidf weights...')
        # Save term frequency in JSON format.
        with open(tfidf_weight_filename, "w") as file:
            json.dump(self.tfidf_weight, file, indent=2)
        print('Saved tfidf weights')

        print('=> Saving idf...')
        # Save inverse document frequency in JSON format.
        with open(idf_filename, "w") as file:
            json.dump(self.idf, file, indent=2)
        print('Saved idf')
