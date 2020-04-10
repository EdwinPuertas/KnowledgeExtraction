import sys
from nltk.corpus import wordnet
from event_logging import EventLogging
from file_etl import FileETL
from ke_root import ROOT_OUTPUT,ROOT_INPUT


class ExtractionSynoyms:
    """
    :Date: 2018-02-06
    :Version: 0.1
    :Author: Edwin Puestas - Pontificia Universidad Javeriana, Bogotá
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
    This class has static methods
    """
    def __init__(self):
        """
        :Date: 2018-02-06
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        Constructor for the class
        :rtype: object
        :return: Utils object
        """

        self.list_synonyms_UNESCO = FileETL.import_csv(ROOT_INPUT,'SinonimosUNESCO')
        self.dict_synonyms_UNESCO = FileETL.import_cvs_dict(ROOT_INPUT,'ListaAntonimos', ';')
        self.list_antonyms = FileETL.import_csv(ROOT_INPUT,'ListaAntonimos')
        self.list_adjetive = FileETL.import_csv(ROOT_INPUT, 'BusinessAdjective')
        self.list_Wikipedia = FileETL.import_csv(ROOT_INPUT, 'TerminosBancosWikipedia')


    def generate_synonyms(self):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method builds a thesaurus using a set of word lists in Spanish.
        :param self: None
        :type None: None
        :rtype: Dictionary
        :return: Dictionary of synonyms
        """
        
        try:
            dict_synonyms = {}
            dict_synonyms_UNESCO_WORDNET = self.get_synonyms_wordnet(self.list_synonyms_UNESCO)
            dict_antonyms_WORDNET = self.get_synonyms_wordnet(self.list_antonyms)
            dict_adjetive_WORDNET = self.get_synonyms_wordnet(self.list_adjetive)
            dict_synonyms_Wikipedia = self.get_synonyms_wordnet(self.list_Wikipedia)

            dict_synonyms.update(self.dict_synonyms_UNESCO)
            dict_synonyms.update(dict_synonyms_UNESCO_WORDNET)
            dict_synonyms.update(dict_antonyms_WORDNET)
            dict_synonyms.update(dict_adjetive_WORDNET)
            dict_synonyms.update(dict_synonyms_Wikipedia)

            dict_tmp = {}
            for k,v in dict_synonyms.items():
                k = str(k)
                v = list(v)
                if k in v :
                    v.remove(k)

                if len(v) > 0:
                    dict_tmp[k] = v
            return dict_tmp
        except:
            EventLogging.write_standard_error(sys.exc_info())


    @staticmethod
    def get_synonyms_wordnet(list_words):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method provides an interface with WordNet and extracts the synonyms of a word in Spanish.
        :param list_words: list of words
        :type list_words: list
        :return: Dictionary of synonyms
        """

        try:
            dict_synonyms = {}
            for word in list_words:
                list_synonyms = []
                for syn in wordnet.synsets(word, lang='spa'):
                    for l in syn.lemmas(lang='spa'):
                        list_synonyms.append(l.name().lower().replace('_', ' '))
                    if len(list_synonyms) > 1:
                        word = word.lower().replace('_', ' ')
                        d = {}
                        list_output = [d.setdefault(x, x) for x in list_synonyms if x not in d]
                        if len(list_output) >= 1:
                            if word in list_output:
                                list_synonyms.remove(word)
                                dict_synonyms[word] = list_synonyms
                            else:
                                dict_synonyms[word] = list_synonyms
            return dict_synonyms
        except:
            EventLogging.write_standard_error(sys.exc_info())

if __name__ == '__main__':
    es = ExtractionSynoyms()
    synonyms = es.generate_synonyms()
    #util.export_cvs('SinonimosCAOBA', synonyms)
    FileETL.export_xml(ROOT_OUTPUT,'SinonimosCAOBA',synonyms)
    for val in synonyms.items():
        print(val)

    print(len(synonyms))
