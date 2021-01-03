from src.query import QueryEngine
import sys

if __name__ == '__main__':
    # init Query Engine
    query_engine = QueryEngine()

    # Load inverted index
    query_engine.load_tf_idf_index('./data/tfidf.json')

    # Load idf
    query_engine.load_idf_index('./data/idf.json')

    # Parse user input
    query = sys.argv[1]

    # Run the query
    doc_list = query_engine.query(query)
    
    # Show outputs
    for doc_id, doc_score in doc_list:
        print(doc_id, doc_score)
        # query_engine.print(doc_list)