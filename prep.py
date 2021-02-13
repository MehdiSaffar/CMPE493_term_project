from src.preprocessor import Preprocessor

if __name__ == '__main__':
    preprocessor = Preprocessor()
    preprocessor.run(metadata_filename='./data/metadata.feather')
    # preprocessor.run(metadata_filename='./data/metadata.csv')
    preprocessor.save(tfidf_weight_filename='./data/tfidf.json', idf_filename='./data/idf.json')
