from typing import NamedTuple
from src.query import QueryEngine
import xml.etree.ElementTree as ET
import sys
from collections import namedtuple

from src.utils import serialize_sets, get_tf_idf_weight, get_idf

Topic = namedtuple('Topic', 'number query question narrative')

class Evaluator:
    def __init__(self, inverted_index_filename: str, idf_filename: str, topic_filename: str) -> None:
        super().__init__()
        self.inverted_index_filename = inverted_index_filename
        self.idf_filename = idf_filename
        self.topic_filename = topic_filename
        self.init_query_engine()
    
    def init_query_engine(self):
        self.query_engine = QueryEngine()
        self.query_engine.load_tf_idf_index(self.inverted_index_filename)
        self.query_engine.load_idf_index(self.idf_filename)
    
    def iter_topics(self):
        """
        Iterate over all topics
        """
        tree = ET.parse(self.topic_filename)
        root = tree.getroot()
        for topic in root:
            number = int(topic.attrib['number'])
            query = topic.find('query').text
            question = topic.find('question').text
            narrative = topic.find('narrative').text
            yield Topic(number, query, question, narrative)

    def iter_dev_topics(self):
        """
        Iterate over development (odd numbered) topics only
        """
        for topic in self.iter_topics():
            if topic.number % 2 == 1:
                yield topic
                break
    
    @staticmethod
    def format_eval_line(topic, doc_rank, doc_id, doc_score):
        # query-id Q0 document-id rank score STANDARD
        # TODO: not sure what to put for score here
        # As stated in the lecture, our score function will be put to the score.
        return f"{topic.number} Q0 {doc_id} {doc_rank} {doc_score} STANDARD\n"   

    def run(self):
        results = ""
        for topic in self.iter_dev_topics():
            # print(topic.number, topic.query)
            doc_ids = self.query_engine.query(topic.query)
            for doc_rank, (doc_id, score) in enumerate(doc_ids, start=1):
                # doc_id is a tuple of (doc_id, score)
                results += Evaluator.format_eval_line(topic, doc_rank, doc_id, score)
        return results

if __name__ == '__main__':
    evaluator = Evaluator(
        inverted_index_filename='./data/tfidf.json',
        idf_filename='./data/idf.json',
        topic_filename='./data/topics-rnd5.xml'
    )
    results = evaluator.run()
    print(results)
