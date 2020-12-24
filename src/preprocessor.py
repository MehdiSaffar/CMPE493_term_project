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

# pandarallel.initialize(progress_bar=True)

def serialize_sets(obj):
    return sorted(list(obj)) if isinstance(obj, set) else obj

class Preprocessor:
    def __init__(self) -> None:
        super().__init__()
        self.tf = defaultdict(lambda: defaultdict(int))

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

        print(len(doc_df))
        # return

        doc_df = doc_df.convert_dtypes()
        # doc_df = doc_df.head(37924)
        doc_df = doc_df.head(5_000)
        print('=> Tokenizing documents...')
        doc_df['tokens'] = self.tokenize(doc_df, 'text')
        print('Tokenized documents')

        print('=> Building idf index...')
        
        
        # tf(t, d) number of times t occurs in d
        # mapping from t => d

        # df(t): number of docs that contain t (at least once)

        ['token1', 'token2'] <-- query

        tf[token][doc_id] = 343232 <-- 
        tf[doc_id][token] = 343232

        df[token] = 312
        idf[token] = 3123

        # idf(t): log_10(N/df(t)) where N is total number of documents in the collection

        def add_to_tf_apply(row: pd.Series):
            for token in row['tokens']:    
                self.tf[token][row['id']] += 1

        doc_df[['id', 'tokens']].apply(add_to_tf_apply, axis=1)

        for token, docs in self.tf.items():
            self.idf[token] = math.log10(len(doc_df) / len(docs))

        print('Built inverted index')

    def save(self, inverted_index_filename: str):
        print('=> Saving inverted index...')
        # Save inverted index in JSON format.
        with open(inverted_index_filename, "w") as file:
            json.dump(self.inverted_index, file, default=serialize_sets, indent=2)
        print('Saved inverted index')

        print('=> Saving idf...')
        # Save inverted document frequency in JSON format.
        with open(inverted_index_filename, "w") as file:
            json.dump(self.inverted_index, file, default=serialize_sets, indent=2)
        print('Saved idf')

        print('=> Saving tf...')
        # Save term frequency in JSON format.
        with open(inverted_index_filename, "w") as file:
            json.dump(self.inverted_index, file, default=serialize_sets, indent=2)
        print('Saved tf')
        # Save term frequency in JSON format.
        with open(inverted_index_filename, "w") as file:
            json.dump(self.inverted_index, file, default=serialize_sets, indent=2)
        print('Saved tf')

