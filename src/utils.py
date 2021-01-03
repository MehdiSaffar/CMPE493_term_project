import math

def serialize_sets(obj):
    return sorted(list(obj)) if isinstance(obj, set) else obj

def get_idf(N, doc_count):
    return math.log10(N / doc_count)

def get_tf_idf_weight(tf, idf):
    return (1 + math.log10(tf)) * idf