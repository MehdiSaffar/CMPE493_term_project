# CMPE 493 - Term Project 2020

Using Python 3.8.6

## Members

- Mehdi Saffar
- Hüseyin Can Bölükbaş
- Burak Berk Özer

## How to Run

### Requirements
There are multiple libraries that we've used in this project. These libraries with their versions are listed in `./requirements.txt` file. Don't forget to install these libraries into your virtual environment.

### Preprocessing
Normally for the preprocessing we would use `./data/metadata.csv` but we found that reading csv file is too slow. We decided to use `feather` file format instead which is much faster and helps us iterate quickly.

Make sure the following files exist inside `./data` folder:
- Faster-loading metadata file: `metadata.feather`
- File containing evaluations of queries: `eval.txt`
- File containing topics: `topics-rnd5.xml`

To preprocess the documents run the following command:
```bash
$ python prep.py
```

### Query

To query the documents run the following command:
```bash
$ python query.py [INSERT_YOUR_QUERY_HERE]
```

Example:

```bash
$ python query.py "coronavirus"
$ python query.py "virus origin"
```

### Evaluation

Make sure `./trec_eval` executable exists in the current directory folder. We've automated the evaluation by using that executable file.

For odd topics use:
```bash
$ python eval.py odd
```

For even topics use:
```bash
$ python eval.py even
```

After above command "mAP", "ndcg" and "P.10" metrics will be outputted to the terminal.
