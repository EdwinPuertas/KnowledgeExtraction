import csv
import datetime
import math
import operator
import sys
import spacy
import nltk
import numpy as np
import logging.config
from tp_logic.text_analysis import TextAnalysis
from sklearn.feature_extraction.text import TfidfVectorizer
from textolitica_utils.util import Util
from ke_logic.support import Support
from ke_root import ROOT_DIR_CONFIG, ROOT_INPUT
from sklearn.metrics import precision_recall_fscore_support
logging.config.fileConfig(ROOT_DIR_CONFIG + 'logging.conf')


class TextAnalysisWeirdnessError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = 'TextAnalysisWeirdnessError: {0}-{1}'.format(str(datetime), message)


class TerminologyExtractionWeirdness:
    """
    :Date: 2018-03-12
    :Version: 1.0
    :Author: Edwin Puertas - Pontificia Universidad Javeriana
    :Copyright: Por definir
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
    This class extracts terminology from corpus specific.
    """

    def __init__(self):
        """
        :Date: 2018-03-12
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Copyright: Por definir
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function return inicialized Terminology extraction object
        :return: None
        """

        self.nlp = spacy.load('es')
        self.support = Support()
        self.corpus_crea = self.support.import_crea('CREA')
        self.log_file = logging.getLogger('terminologyExtraction')
        self.service_text = TextAnalysis('es', ['tagger', 'parser', 'ner', 'stemmer', 'caoba_recognizer', 'spell_text',
                                  'polarity_text_bow'])



    def extracting_sentences(self, corpus, key=0, content=1):
        try:
            list_output = []
            print('Extracting sentences, please wait a moment!!!!')
            for item in corpus:
                list_tmp = []
                text = str(item[content]).lower().strip()
                if content != ' ':
                    doc = self.nlp(text)
                    for span in doc.sents:
                        list_tmp.append(span)
                list_output.append([item[key], list_tmp])

            return list_output
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error extracting_sentences')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))

    def get_terminology(self, list_corpus, list_patterns = ['NOUN']):
        """
        :Date: 2018-03-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function create a corpus by articles in Wikipedia by seed words.
        :param list_doc: list of documents (corpus)
        :type list: Text
        :rtype: dict
        :return: terms by documents
        """
        try:
            dict_corpus = {}
            id_corpus = 1
            print('Extracting terms from the corpus, wait a moment!!!!')
            for corpus in list_corpus:
                dict_document = {}
                i = 0
                for item in corpus:
                    dict_content = {}
                    for text in item[1]:
                        content = str(text).replace('\n', ' ')
                        dict_chunk = self.service_text.syntax_patterns(content)
                        if dict_chunk is not None:
                            for k, v in dict_chunk.items():
                                if k in list_patterns and v is not None:
                                    for key, value in v.items():
                                        chunk = self.support.clean_text(str(key))
                                        dict_content[chunk] = value

                    if len(dict_content) > 0:
                        i += 1
                        dict_document[i] = dict_content
                        print('Document {0}: Terms:{1}'.format(i, dict_content))
                dict_corpus[id_corpus] = dict_document
                print('Terminology Extraction from corpus {0} successful.'.format(id_corpus))
                id_corpus += 1
            return dict_corpus
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error get_terminology')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))

    def get_pos(self, statement):
        try:
            list_output = []
            doc = self.nlp(statement)
            for token in doc:
                pos = token.pos_
                list_output.append([token.text, pos])
            return list_output
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error get_pos')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))

    def calulated_frecuency(self, dict_corpus_terms, stopword = True):
        try:
            dict_corpus = {}
            print('Calculated frequency in {0} corpus '.format(len(dict_corpus_terms)))
            for id_corpus, dict_terms in dict_corpus_terms.items():
                dict_terms_frecuency = {}
                print('Calculated frequency of terms in corpus {0}, please wait a moment........'.format(id_corpus))
                for doc, value in dict_terms.items():
                    for key, pos in value.items():
                        term = str(key)
                        if stopword:
                            if not self.support.stop_word(term):
                                if term in dict_terms_frecuency:
                                    temp = dict_terms_frecuency.get(term)
                                    freq = temp['freq'] + 1
                                    dict_terms_frecuency[term] = {'freq': freq, 'pos': temp['pos']}
                                else:
                                    dict_terms_frecuency[term] = {'freq': 1, 'pos': pos}
                        else:
                            if term in dict_terms_frecuency:
                                temp = dict_terms_frecuency.get(term)
                                freq = temp['freq'] + 1
                                dict_terms_frecuency[term] = {'freq': freq, 'pos': temp['pos']}
                            else:
                                dict_terms_frecuency[term] = {'freq': 1, 'pos': pos}
                dict_corpus[id_corpus] = dict_terms_frecuency
            return dict_corpus
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error calulated_frecuency')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))

    def normalized_uni_grams(self, corpus_terms_frequency):
        try:
            corpus_normalized = {}
            total_freq = 0.0
            for k, v in corpus_terms_frequency.items():
                total_freq += float(str(v['freq']).strip())

            for key, value in corpus_terms_frequency.items():
                freq = float(str(value['freq']).strip())
                size_term = len(str(key).split(' '))
                if size_term == 1:
                    corpus_normalized[key] = float((freq / total_freq) * 1000000)
                else:
                    corpus_normalized[key] = freq

            return corpus_normalized
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error normalized_rae')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))

    def normalized_c_value(self, term, corpus_normalized):
        try:
            result = 1.0
            #Calculo de los términos de mayor tamaño
            N = 0
            for k, v in corpus_normalized.items():
                size_tmp = len(str(k).split(' '))
                if size_tmp > N:
                    N = size_tmp

            size_term = len(str(term).split(' '))
            if term in corpus_normalized and size_term > 1:
                f_a = float(corpus_normalized[term])
                ta = 1
                f_b = 0.0
                for term_tmp in corpus_normalized:
                    term_tmp = str(term_tmp)
                    if term_tmp.find(term) > -1:
                        ta += 1
                        freq_fb = float(corpus_normalized[term_tmp])
                        f_b += freq_fb

                if size_term <= N -1:
                    result = round((math.log(size_term, 2) * f_a), 4)
                else:
                    g_a = (f_b / ta)
                    result = round((math.log(size_term, 2) * (f_a - g_a)), 4)

            print('Term: {0} Freq_Normalized: {1:.2f}'.format(term, result))
            return result
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error normalized_c_value')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))
            return None

    def normalized_corpus(self, dict_corpus_terms_frequency):
        try:
            result = {}
            dict_rae = self.corpus_crea
            for id_corpus, corpus_value in dict_corpus_terms_frequency.items():
                corpus_normalized = self.normalized_uni_grams(corpus_value)
                dict_normalized = {}
                for term, value in corpus_normalized.items():
                    if term in dict_rae:
                        freq = float(value)
                        freq_rae = float(dict_rae[term])
                        if freq_rae > 0.0:
                            freq_normalized = round(float(freq_rae / freq), 4)
                            if freq_normalized < 1.0 and freq_normalized > 0.0:
                                dict_normalized[term] = freq_normalized
                    else:
                        freq_normalized = self.normalized_c_value(term, corpus_normalized)
                        if freq_normalized > 0.0:
                            dict_normalized[term] = freq_normalized

                result[id_corpus] = dict_normalized
            return result
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error normalized_corpus')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))

    def tfidf(self, corpus):
        try:
            tfidf = TfidfVectorizer(analyzer = 'word', max_features = 10000, ngram_range=(1,4))
            tfs = tfidf.fit_transform(corpus.values())
            feature_names = tfidf.get_feature_names()
            corpus_index = [n for n in corpus]
            rows, cols = tfs.nonzero()
            list_tfidf = []
            for row, col in zip(rows, cols):
                term = self.support.clean_text(feature_names[col])
                term = self.ngrams_rules(term)
                if term != 'None' and not self.support.stop_word(term):
                    list_tfidf.append([term, corpus_index[row], tfs[row, col]])
                    print('Term: {0}, Document: {1}, TF-IDF: {2}, '.format(term, corpus_index[row], tfs[row, col]))
            return list_tfidf
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error tfidf')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))


    def corpus_cut_off(self, dict_corpus_terms_frequency, cut_off = 20):
        try:
            result = {}
            for id_corpus, corpus_value in dict_corpus_terms_frequency.items():
                corpus_unigram = {}
                corpus_ngrams = {}
                for term, freq in corpus_value.items():
                    size_term = len(str(term).split(' '))
                    if size_term == 1:
                        corpus_unigram[term] = freq
                    else:
                        corpus_ngrams[term] = freq

                corpus_unigram = sorted(corpus_unigram.items(), key=operator.itemgetter(1), reverse=True)
                corpus_ngrams = sorted(corpus_ngrams.items(), key=operator.itemgetter(1), reverse=True)
                cut_off_uni = int(len(corpus_unigram) * (cut_off/100))
                cut_off_n = int(len(corpus_ngrams) * (cut_off / 100))
                corpus_cut_off_uni = {}
                corpus_cut_off_n = {}

                for item in corpus_unigram[0:cut_off_uni]:
                    corpus_cut_off_uni[item[0]] = item[1]

                for item in corpus_ngrams[0:cut_off_n]:
                    corpus_cut_off_n[item[0]] = item[1]

                id_uni = str(id_corpus) + ' - 1'
                id_n = str(id_corpus) + ' - N'
                result[id_uni] = corpus_cut_off_uni
                result[id_n] = corpus_cut_off_n

            return result
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error corpus_cut_off')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))
            return None


    def union(self, dict_corpus_terms_frequency):
        try:
            result = {}
            dict_pivot = dict_corpus_terms_frequency[1]
            for i in range(1,len(dict_corpus_terms_frequency)):
                corpus_tmp = dict_corpus_terms_frequency[i]
                for key_pivot, value_pivot in dict_pivot.items():
                        if key_pivot in corpus_tmp:
                            if value_pivot != 0.0:
                                result[key_pivot] = value_pivot
                            else:
                                result[key_pivot] = corpus_tmp[key_pivot]

            return result
        except Exception as e:
            self.log_file.error('\t** TerminologyExtraction:error corpus_cut_off')
            self.log_file.error(Util.write_standard_error(sys.exc_info()))
            return None


    def statistical_measures(self):
        path = ROOT_INPUT + 'GoldStandarBank.csv'
        file = open(path)
        list_pred = []
        list_true = []
        lines = csv.reader(file, dialect='excel', delimiter=';')
        lines = list(lines)
        for item in lines:
            list_true.append(item[0])

        y_true = np.array(list_true)
        y_pred = np.array(list_pred)

        prf = precision_recall_fscore_support(y_true, y_pred, None)
