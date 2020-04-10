import numpy as np
from operator import itemgetter
from collections import defaultdict
import xlsxwriter as xlsxwriter
from ke_logic.support import Support
from sklearn.feature_extraction.text import CountVectorizer
from ke_root import ROOT_OUTPUT


class PMIUnsupervised():

    def __init__(self):
        self.support = Support()
        print('Get PMI....')

    def getcollocations(self, w, PMI_MATRIX, TERMS):
        if w not in TERMS:
            return []
        idx = TERMS.index(w)
        col = PMI_MATRIX[:, idx].ravel().tolist()
        #
        # for i in range(0, idx):
        #      val = PMI_MATRIX[i, idx].ravel().tolist()
        #      print(TERMS[i], TERMS[idx], val)

        return sorted([(TERMS[i], val) for i, val in enumerate(col)], key=itemgetter(1), reverse=True)

    def seed_score(self, seed_list, PMI_MATRIX, TERMS):
        score = defaultdict(int)
        for seed in seed_list:
            c = dict(self.getcollocations(seed, PMI_MATRIX, TERMS))
            for w in c:
                score[w] += c[w]
        return score

    # PMI type measure via matrix multiplication
    def getcollocations_matrix(self, X, terms):
        XX = X.T.dot(X)  ## multiply X with it's transpose to get number docs in which both w1 (row) and w2 (column) occur
        term_freqs = np.asarray(X.sum(axis=0))  ## number of docs in which a word occurs
        pmi = XX.toarray() * 1.0  ## Casting to float, making it an array to use simple operations
        self.export_matrix(pmi,terms,'MatrixFreq')
        pmi /= term_freqs.T     ## dividing by the number of documents in which w1 occurs
        pmi /= term_freqs        ## dividing by the number of documents in which w2 occurs
        return pmi  ## this is not technically PMI beacuse we are ignoring some normalization factor and not taking the log
        # but it's sufficient for ranking

    def calculated_pmi(self, corpus):
        vec = CountVectorizer(min_df=50)
        X = vec.fit_transform(corpus)
        terms = vec.get_feature_names()
        pmi_matrix = self.getcollocations_matrix(X, terms)
        return pmi_matrix, terms


    def calculated_pmi_seeds(self, seed_list, corpus):
        vec = CountVectorizer(min_df=50)
        X = vec.fit_transform(corpus)
        terms = vec.get_feature_names()
        pmi_matrix = self.getcollocations_matrix(X, terms)
        pmi_value = sorted(self.seed_score(seed_list, pmi_matrix, terms).items(), key=itemgetter(1), reverse=True)
        return pmi_value

    def export_matrix(self, matrix_pmi, term, file_output):
        path = ROOT_OUTPUT + file_output + '.xlsx'
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()
        for i in range(0, len(term)):
            worksheet.write(i+1, 0, term[i]) # Imprime en la primera fila
            worksheet.write(0, i+1, term[i]) # Imprime en la primera columna
        row = 1
        for col, data in enumerate(matrix_pmi):
            worksheet.write_column(row, col+1, data)
        workbook.close()