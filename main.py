import string
from collections import defaultdict
import json

import contractions
import nltk
import nltk.tokenize
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from pandarallel import pandarallel

# pandarallel.initialize(progress_bar=True)

def serialize_sets(obj):
    return sorted(list(obj)) if isinstance(obj, set) else obj

class Preprocessor:

    def __init__(self) -> None:
        super().__init__()
        self.inverted_index = defaultdict(set)

    def parse_eval_file(self, eval_filename: str):
        df = pd.read_csv(eval_filename, delim_whitespace=True, names="topic_id iteration_id doc_id relevance".split())
        df = df.convert_dtypes()
        return df
    
    def tokenize(self, df: pd.DataFrame, col: str):
        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV

        lemmatizer = WordNetLemmatizer()
        def tokenize_apply(value: str):
            stopwords = "'s".split()

            # if '`' in value:
            #     print( value)

            for sentence in nltk.tokenize.sent_tokenize(value):
                sentence = contractions.fix(sentence, slang=False)
                words = nltk.tokenize.word_tokenize(sentence)
                lemmatized_words = []
                for word, pos in  nltk.pos_tag(words):
                    wn_pos = tag_map[pos[0]]

                    word = word.lower()

                    if word in stopwords:
                        continue

                    if word in string.punctuation:
                        continue

                    lemmatized_word = lemmatizer.lemmatize(word, pos=wn_pos)
                    lemmatized_words.append(lemmatized_word)
                return lemmatized_words

        result = df[col].apply(tokenize_apply)
        # print(result)
        return result


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
        print('=> Tokenizing documents...')
        doc_df['tokens'] = self.tokenize(doc_df, 'text')
        print('Tokenized documents')

        print('=> Building inverted index...')
        def add_to_inverted_index_apply(row: pd.Series):
            for token in row['tokens']:
                self.inverted_index[token].add(row['id'])

        doc_df[['id', 'tokens']].apply(add_to_inverted_index_apply, axis=1)
        print('Built inverted index')

    def save(self, inverted_index_filename: str):
        print('=> Saving inverted index...')
        # Save inverted index in JSON format.
        with open("data/inverted_index.json", "w") as file:
            json.dump(self.inverted_index, file, default=serialize_sets, indent=2)
        print('Saved inverted index')

if __name__ == '__main__':
    preprocessor = Preprocessor()
    preprocessor.run(metadata_filename='./data/metadata.feather')
    preprocessor.save(inverted_index_filename='./data/inverted_index.json')
