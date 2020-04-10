import csv
import os
import string
from ke_root import ROOT_OUTPUT
from google_ngram_downloader import readline_google_store

list_word = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z', 'ch']
dict_ngram = {}
for word in list_word:
    fnames, urls, records = next(readline_google_store(ngram_len=1, indices=word, lang='spa'))
    for i in records.__iter__():
        ngram = str(i.ngram).lower()
        if ngram.find('_') == -1:
            if ngram in dict_ngram:
                temp = dict_ngram.get(ngram)
                freq = temp['freq'] + i.match_count
                count = temp['count'] + 1
                dict_ngram[ngram] = {'freq': freq,'count': count}
            else:
                freq = i.match_count
                count = 1
                dict_ngram[ngram] = {'freq':freq,'count': count}
                print('Calulated valued to ngram = {0}'.format(ngram))

result = {}
for k, v in dict_ngram.items():
    relative_freq = round(float(v['freq'] / v['count']), 2)
    result[k] = relative_freq
    print('ngrams = {0}, relative_freq = {1}'.format(k, relative_freq))

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_OUTPUT = ROOT_DIR + os.sep + 'data'+ os.sep
file_output = ROOT_OUTPUT + 'GoogleNgrams1.csv'
with open(file_output, 'w', newline='\n', encoding='utf-8') as output:
    writer = csv.writer(output, delimiter=';')
    for k, v in result.items():
        value = str(v).lower()
        value.rstrip(string.whitespace)
        writer.writerow([str(k).lower(), value])

print('CSV file successfully exported!')

