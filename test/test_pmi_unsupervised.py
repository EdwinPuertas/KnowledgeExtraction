#http://www.cs.cornell.edu/courses/cs4300/2018sp/Demos/demo-sentiment-unsupervised.html
from __future__ import print_function

import csv
import json
import os
from operator import itemgetter
from collections import defaultdict
from textolitica_utils.text_utils import TextUtils

from matplotlib import pyplot as plt
import numpy as np

from nltk.tokenize import TweetTokenizer
from nltk import FreqDist,pos_tag
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import load_files
from sklearn.naive_bayes import MultinomialNB
from ke_root import ROOT_INPUT
ROOT_INPUT = ROOT_INPUT + os.sep + 'txt_sentoken'
tokenizer = TweetTokenizer()


# PMI type measure via matrix multiplication
def getcollocations_matrix(X):
    XX = X.T.dot(X)  ## multiply X with it's transpose to get number docs in which both w1 (row) and w2 (column) occur
    term_freqs = np.asarray(X.sum(axis=0))  ## number of docs in which a word occurs
    pmi = XX.toarray() * 1.0  ## Casting to float, making it an array to use simple operations
    pmi /= term_freqs.T  ## dividing by the number of documents in which w1 occurs
    pmi /= term_freqs  ## dividing by the number of documents in which w2 occurs

    return pmi  # this is not technically PMI beacuse we are ignoring some normalization factor and not taking the log
    # but it's sufficient for ranking

# corpus = []
# corpus_raw= ROOT_INPUT + 'tweets_sample.csv'
# file = open(corpus_raw)
# lines = csv.reader(file, dialect='excel', delimiter=';')
# lines = list(lines)
# for item in lines:
#     corpus.append(TextUtils.clean_text(item[1]))

data = load_files(ROOT_INPUT)
print(data.data[0])



vec = CountVectorizer(min_df = 50)
X = vec.fit_transform(data.data)
print(X)
terms = vec.get_feature_names()
print(terms)
print(len(terms))

pmi_matrix = getcollocations_matrix(X)
print(pmi_matrix)
pmi_matrix.shape
print(pmi_matrix.shape)

def getcollocations(w,PMI_MATRIX=pmi_matrix,TERMS=terms):
    if w not in TERMS:
        return []
    idx = TERMS.index(w)
    col = PMI_MATRIX[:,idx].ravel().tolist()
    return sorted([(TERMS[i],val) for i,val in enumerate(col)], key=itemgetter(1),reverse=True)

def seed_score(pos_seed,PMI_MATRIX=pmi_matrix,TERMS=terms):
    score=defaultdict(int)
    for seed in pos_seed:
        c=dict(getcollocations(seed,PMI_MATRIX,TERMS))
        for w in c:
            score[w]+=c[w]
    return score


print(sorted(seed_score(['bueno','gracias']).items(),key=itemgetter(1),reverse=True))