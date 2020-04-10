from ke_logic.terminology_extraction import TerminologyExtraction
from ke_logic.support import Support
from ke_root import ROOT_OUTPUT, ROOT_INPUT

dict_corpus_terms = {}
te = TerminologyExtraction()
support = Support()
raw_corpusA = support.import_corpus('CCD_Test',id= True,content=1)
corpusA = te.extracting_sentences(raw_corpusA)
dict_corpus_terms = te.get_terminology([corpusA],list_patterns=['NOUN','VERB','ADV'])
dict_corpus_terms_frequency = te.calulated_frecuency(dict_corpus_terms, False)

support.export_corpus_cvs('TerminologyCCDFreq',dict_corpus_terms_frequency)

dict_normalized_corpus = te.normalized_corpus(dict_corpus_terms_frequency)
support.export_corpus_cvs('TerminologyCCDNormalized',dict_normalized_corpus)
corpus_cut_off = te.corpus_cut_off(dict_normalized_corpus, 20)

for corpus, dict_terms in corpus_cut_off.items():
    print('Corpus {0}'.format(corpus))
    for term, value in dict_terms.items():
        print('Termino: {0}, Values: {1}'.format(term,value))

print('Corpus Normalized: {0}'.format(len(dict_normalized_corpus.keys())))
print('Corpus CutOff 20: {0}'.format(len(corpus_cut_off.keys())))
support.export_corpus_cvs('TerminologyCCDCutOff',corpus_cut_off)


