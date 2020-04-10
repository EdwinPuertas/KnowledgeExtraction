from ke_logic.terminology_extraction import TerminologyExtraction
from file_etl import FileETL
from ke_root import ROOT_OUTPUT, ROOT_INPUT

dict_terms = {}
te = TerminologyExtraction()

articles_bancos = FileETL.import_xml(ROOT_INPUT,'CorpusGeneralWikipedia')

corpus = {}
print('Get Corpus')
for item in articles_bancos:
    if item['content'] != '' and item['title'] !='':
        corpus[item['title']] = str(item['content'])
        print('Title: {0}\nContent:{1}'.format(item['title'], item['content']))

print('Calculando TFIDF, Espere un Momento')
list_tfidf = []
list_tfidf = te.tfidf(corpus)
i=0
dict_tfidf = {}
for item in list_tfidf:
    dict_tfidf[i+1] = item
    i = i + 1
    print(item)

FileETL.export_cvs(ROOT_OUTPUT, 'TerminosGeneralTFIDF',dict_tfidf)