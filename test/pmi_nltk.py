import csv
import nltk
from ke_logic.terminology_extraction import TerminologyExtraction
from textolitica_utils.text_utils import TextUtils
from ke_root import ROOT_OUTPUT, ROOT_INPUT


te = TerminologyExtraction()

# Cargar Corpus
corpus = []
corpus_raw= ROOT_INPUT + 'tweets_sample.csv'
file = open(corpus_raw)
lines = csv.reader(file, dialect='excel', delimiter=';')
lines = list(lines)
for item in lines:
    corpus.append({'title': item[0], 'content': TextUtils.clean_text(item[2])})

dict_terms = te.get_terminology(corpus, 2)
dic_terms_frecuency = te.calulated_frecuency(dict_terms)

unigram = []
bigram = []
for key, value in dic_terms_frecuency.items():
    if len(value['words']) == 1:
        unigram.append(key)
    elif len(value['words']) == 2:
        bigram.append(key)


bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = nltk.BigramCollocationFinder.from_words(unigram, window_size = 10)
list_pmi = finder.score_ngrams(bigram_measures.pmi)

dict_pmi = {}
file_output = ROOT_OUTPUT + 'pmi_tweets_sample.csv'
with open(file_output, 'w', newline='', ) as output:
    w = csv.DictWriter(output, fieldnames = ['Word1_Word2','PMI'], dialect='excel', delimiter=';')
    w.writeheader()
    for k, v in list_pmi:
        bigram = ' '.join([k[0], k[1]])
        term_nlp = te.get_pos(bigram)
        terrm = te.applying_rules(term_nlp, 2)
        if terrm is not None:
            dict_pmi['Word1_Word2'] = terrm[0]
            dict_pmi['PMI'] =  round(v,4)
            w.writerow(dict_pmi)
            print(terrm[0], round(v,4))

