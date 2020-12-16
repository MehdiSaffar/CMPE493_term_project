from src.preprocessor import Preprocessor

if __name__ == '__main__':
    preprocessor = Preprocessor()
    preprocessor.run(metadata_filename='./data/metadata.feather')
    preprocessor.save(inverted_index_filename='./data/inverted_index.json')