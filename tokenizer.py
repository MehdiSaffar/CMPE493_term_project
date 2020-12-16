import string
from collections import defaultdict

import contractions
import nltk.tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

class Tokenizer:
    def __init__(self):
        super().__init__()
        self.lemmatizer = WordNetLemmatizer()

    def tokenize(self, text: str):
        stopwords = "'s".split()

        for sentence in nltk.tokenize.sent_tokenize(text):
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

                lemmatized_word = self.lemmatizer.lemmatize(word, pos=wn_pos)
                lemmatized_words.append(lemmatized_word)
            return lemmatized_words
        return []
