from ke_logic.terminology_extraction import TerminologyExtraction
from ke_logic.support import Support
from ke_root import ROOT_OUTPUT, ROOT_INPUT

dict_corpus_terms = {}
te = TerminologyExtraction()
support = Support()
raw_corpusCCD = support.import_corpus('CCD_Test', id=False, key=0,content=1, encoding='latin-1')
raw_corpus_bank = support.import_xml('CorpusBancos','row')

corpus_raw_Wikipedia = []
corpus_raw_Webpage = []
for item in raw_corpus_bank:
    if item['resource'] == 'Wikipedia':
        corpus_raw_Wikipedia.append([item['title'], str(item['content']).strip()])
    elif item['resource'] == 'webpage':
        list_content = str(item['content'][1:len(item['content'])-1]).replace("'", '').split(',')
        content = ''
        for i in list_content:
            content += i + ' '
        corpus_raw_Webpage.append([item['title'],content])

corpusCCD = te.extracting_sentences(raw_corpusCCD)
corpusWikipedia = te.extracting_sentences(corpus_raw_Wikipedia)
corpusWebpage= te.extracting_sentences(corpus_raw_Webpage)
dict_corpus_terms = te.get_terminology([corpusCCD, corpusWikipedia, corpusWebpage],['NOUN'])
dict_corpus_terms_frequency = te.calulated_frecuency(dict_corpus_terms, False)
#Normaliza los corpus
dict_normalized_corpus = te.normalized_corpus(dict_corpus_terms_frequency)
support.export_corpus_cvs('TerminologyNCorpusNormalizedAll',dict_normalized_corpus)

corpus_cut_off = te.corpus_cut_off(dict_normalized_corpus, 100)

for corpus, dict_terms in corpus_cut_off.items():
    print('Corpus {0}'.format(corpus))
    for term, freq in dict_terms.items():
         print('Termino: {0}, Freq: {1}'.format(term,freq))

support.export_corpus_cvs('TerminologyNCorpusAll',corpus_cut_off)
#corpus_union = te.union(corpus_cut_off)
#support.export_corpus_cvs('TerminologyNCorpusUnion',corpus_cut_off)


