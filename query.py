from src.query import QueryEngine
import sys

if __name__ == '__main__':
    # init Query Engine
    query_engine = QueryEngine()

    # Load inverted index
    query_engine.load_inverted_index('./data/inverted_index.json')

    # Parse user input
    query = sys.argv[1]

    # Run the query
    doc_list = query_engine.query(query)
    
    # Show outputs
    query_engine.print(doc_list)