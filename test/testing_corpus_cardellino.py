import os

from ke_logic.terminology_extraction import TerminologyExtraction
from ke_logic.support import Support
from ke_root import ROOT_OUTPUT, ROOT_INPUT


ROOT_INPUT =  ROOT_INPUT + '/spanish_billion_words/'
def import_corpus(ruta = ROOT_INPUT):
    result = []
    i = 0
    contenido = os.listdir(ruta)
    for elemento in contenido:
        archivo = ruta + os.sep + elemento
        texto = ''
        if os.path.isfile(archivo):
            with open(archivo, 'r', encoding='ascii', errors='ignore') as archivo:
                for linea in archivo:
                    texto += linea
            result.append([i, texto])
            i += 1
            archivo.close()
    return result

#dict_corpus_terms = {}
#te = TerminologyExtraction()
#support = Support()

print(import_corpus())



# raw_corpusA = support.import_corpus('TASS2018',key=0, content=2,encoding='utf-8')
# corpusA = te.extracting_sentences(raw_corpusA)
# dict_corpus_terms = te.get_terminology([corpusA],list_patterns=['NOUN'])
# dict_corpus_terms_frequency = te.calulated_frecuency(dict_corpus_terms, False)
# dict_normalized_corpus = te.normalized_corpus(dict_corpus_terms_frequency)
# corpus_cut_off = te.corpus_cut_off(dict_normalized_corpus, 100)
# support.export_corpus_cvs('TerminologyTASS',corpus_cut_off)