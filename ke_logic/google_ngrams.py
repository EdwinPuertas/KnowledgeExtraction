import csv
import os
import string
from google_ngram_downloader import readline_google_store,util
list_not = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_ADJ_', '_ADP_', '_ADV_', '_CONJ_', '_DET_', '_NOUN_',
            '_NUM_', '_PRON_', '_PRT_', '_VERB_']
ngrams = 3
result = {}
list_indices = util.get_indices(ngrams)
dict_ngram = {}
for item in list_indices:
    if not (item in list_not):
        list_tmp = []
        list_tmp.append(item)
        try:
            fnames, urls, records = next(readline_google_store(ngram_len=ngrams, indices=list_tmp, lang='spa'))
            for i in records:
                try:
                    ngram = str(i.ngram).lower()
                    # print(i)
                    if ngram.find('_') == -1:
                        if ngram in dict_ngram:
                            temp = dict_ngram.get(ngram)
                            freq = float(temp['freq'] + i.match_count)
                            count = temp['count'] + 1
                            dict_ngram[ngram] = {'freq': freq, 'count': count}
                        else:
                            freq = 1 if str(i.match_count) == '' else float(i.match_count)
                            count = 1
                            dict_ngram[ngram] = {'freq': freq, 'count': count}
                            print('Calulated valued to ngram = {0}'.format(ngram))
                except Exception as e:
                    print("\t ERROR generated ngrams:{0} error: {1}".format(ngram, e))
                    next(i)
        except Exception as e:
            print("\t ERROR downloader Google ngrams:{0} error: {1}".format(item, e))
            continue


try:
    for k, v in dict_ngram.items():
        relative_freq = round(float(v['freq'] / v['count']), 4)
        result[k] = relative_freq
        print('ngrams = {0}, relative_freq = {1}'.format(k, relative_freq))
except Exception as e:
    print("\t ERROR calculated frequency: {0}".format(e))

try:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_OUTPUT = ROOT_DIR + os.sep + 'data'+ os.sep
    file_output = ROOT_OUTPUT + 'GoogleNgrams3.csv'
    with open(file_output, 'w', newline='\n', encoding='utf-8') as output:
         writer = csv.writer(output, delimiter=';')
         for k, v in result.items():
             value = str(v).lower()
             value.rstrip(string.whitespace)
             writer.writerow([str(k).lower(), value])

    print('CSV file successfully exported!')
except Exception as e:
    print("\t ERROR Exported file: {}".format(e))
