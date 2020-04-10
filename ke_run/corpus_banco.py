from ke_logic.terminology_extraction import TerminologyExtraction
from file_etl import FileETL
from ke_root import ROOT_INPUT,ROOT_OUTPUT

dict_terms = {}
te = TerminologyExtraction()

corpus = FileETL.import_xml(ROOT_INPUT,'CorpusBancosWikipedia')
print(corpus)
dict_terms = te.get_terminology(corpus)
dic_terms_frecuency = te.calulated_frecuency(dict_terms)

corpus_document = {}
print('Calculated TF-IDF, wait a moment!')
for item in corpus:
    if item['content'] != '' and item['title'] !='':
        corpus_document[item['title']] = str(item['content'])

tfidf = te.tfidf(corpus_document)

print('Validating TF-IDF, wait a moment!')

dict_tfidf = {}
for term, freq in dic_terms_frecuency.items():
    for item in tfidf:
        if term == item[0]:
            if term in dict_tfidf:
                val = float(dict_tfidf.get(term)[1])
                if item[2] > val:
                    dict_tfidf[term] =[freq, round(item[2], 4)]
            else:
                dict_tfidf[term] = [freq, round(item[2], 4)]

list_tfidf = []
for k, v in dict_tfidf.items():
    list_tfidf.append({'Term': k, 'FreqAbs' : v[0], 'TF-IDF' : v[1]})
    print('Term: {0}, Freq Absoluta: {1}, TF-IDF: {2}, '.format(k, v[0], v[1]))

print('Exporting TF-IDF')
FileETL.export_xml(ROOT_OUTPUT,'TerminosBancosTFIDF', list_tfidf)