# CMPE 493 - Term Project 2020

Using Python 3.8.6

## Members

- Mehdi Saffar
- Hüseyin Can Bölükbaş
- Burak Berk Özer

## How to Run

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
For odd topics use:
```bash
$ python eval.py odd
```

For even topics use:
```bash
$ python eval.py even
```

After above command, evaluation result will be outputted to the terminal in the below format:

```
<query-id> Q0 <document-id> <rank> <score> STANDARD
```
