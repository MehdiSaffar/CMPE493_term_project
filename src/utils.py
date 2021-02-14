import math

def serialize_sets(obj):
    return sorted(list(obj)) if isinstance(obj, set) else obj

def get_idf(N, doc_count):
    # idf formulation differs from model to model. below formulation is for bm25.
    # return math.log(1 + ( (N - doc_count + 0.5) / (doc_count + 0.5) ) )
    
    # below is for bm25+
    return (N + 1) / doc_count
    
    # below is for bm25L
    # return math.log( ( N + 1 ) / (doc_count + 0.5) )

def get_tf_idf_weight(tf, idf):
    return (1 + math.log10(tf)) * idf