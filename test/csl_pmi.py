import csv
import math
import itertools
from ke_logic.terminology_extraction import TerminologyExtraction
from textolitica_utils.text_utils import TextUtils
from textolitica_utils.file_etl import FileETL
from ke_root import ROOT_OUTPUT, ROOT_INPUT

def pmi(word1, word2, unigram_freq, bigram_freq):
    pmi_value = 0.0
    prob_word1_word2 = 0.0
    if word1 in unigram_freq and word2 in unigram_freq:
        bigram = ' '.join([word1, word2])
        prob_word1 = unigram_freq[word1] / float(sum(unigram_freq.values()))
        prob_word2 = unigram_freq[word2] / float(sum(unigram_freq.values()))
        if bigram in bigram_freq:
            prob_word1_word2 = bigram_freq[bigram] / float(sum(bigram_freq.values()))
            pmi_value = math.log(prob_word1_word2/float(prob_word1*prob_word2), 2)
            print(prob_word1_word2)
            print(bigram_freq[bigram])
        return [word1, round(prob_word1,6), word2, round(prob_word2,6), bigram, round(prob_word1_word2, 6), round(pmi_value, 6)]

dict_terms = {}
te = TerminologyExtraction()
# Cargar el Lexicon
vocabularyA = []
vocabularyB = []
path_lexicon= ROOT_INPUT + 'TerminosCSLRecalificados.csv'
#path_lexicon= ROOT_INPUT + 'lexicon_tmp.csv'
file = open(path_lexicon)
lines = csv.reader(file, dialect='excel', delimiter=';')
lines = list(lines)
for item in lines:
    if item[1] == '1':
        vocabularyA.append(item[0].strip())
    elif item[1] == '-1':
        vocabularyB.append(item[0].strip())

print(vocabularyA)
print(vocabularyB)

# Cargar Corpus
corpus = []
corpus_raw= ROOT_INPUT + 'tweets_sample.csv'
file = open(corpus_raw)
lines = csv.reader(file, dialect='excel', delimiter=';')
lines = list(lines)
for item in lines:
    corpus.append({'title': item[0], 'content': TextUtils.clean_text(item[2])})

#Corpus CCD
#Consumer Complaint Database (Spanish)_16072018
# corpus_raw= FileETL.import_cvs_dict(ROOT_INPUT,'Consumer Complaint Database (Spanish)_Test',';')
# corpus = []
# for k, v in corpus_raw.items():
#     if v[1] !=  :
#         corpus.append({'title': v[0], 'content': TextUtils.clean_text(v[1])})



dict_terms = te.get_terminology(corpus, 2)
dic_terms_frecuency = te.calulated_frecuency(dict_terms)

unigram_freq = {}
bigram_freq = {}
for key, value in dic_terms_frecuency.items():
    if len(value['words']) == 1:
        unigram_freq[key] = value['freq']
    elif len(value['words']) == 2:
        bigram_freq[key] = value['freq']

print('unigram_freq {0}'.format(unigram_freq))
print('bigram_freq {0}'.format(bigram_freq))

title = ['Word1 ', 'ProbWord1', 'Word2 ', 'ProbWord2', 'Word1Word2','PorbWord1Word2', 'PMI']
print(title)
print('='*70)
dict_pmi = {}
file_output = ROOT_OUTPUT + 'PMI_lexicon.csv'
with open(file_output, 'w', newline='', ) as output:
     w = csv.DictWriter(output, dict_pmi.keys(), dialect='excel', delimiter=';')
     w.writeheader()
     for word1, word2 in itertools.product(vocabularyA, vocabularyB):
         value = pmi(word1, word2, unigram_freq, bigram_freq)
         if value is not None:
             dict_pmi['Word1'] = value[0]
             dict_pmi['ProbWord1'] = value[1]
             dict_pmi['Word2'] = value[2]
             dict_pmi['ProbWord2'] = value[3]
             dict_pmi['Word1Word2'] = value[4]
             dict_pmi['PorbWord1Word2'] = value[5]
             dict_pmi['PMI'] = value[6]
             w.writerow(dict_pmi)
             print(value)
