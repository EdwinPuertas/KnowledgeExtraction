from ke_logic.terminology_extraction import TerminologyExtraction
from ke_logic.support import Support

dict_corpus_terms = {}
te = TerminologyExtraction()
support = Support()
#raw_corpusA = support.import_corpus('CCD_v7_esp', id=True, key=0, content=2)
raw_corpusG  =  support.import_general_corpus()
# corpus_ccd = te.extracting_sentences(raw_corpusA)
# dict_corpus_terms = te.get_terminology([corpus_ccd],list_patterns=['NOUN'])
# dict_corpus_terms_frequency = te.calulated_frecuency(dict_corpus_terms, False)
# support.export_corpus_cvs('TerminologyCCDv7Freq',dict_corpus_terms_frequency)


