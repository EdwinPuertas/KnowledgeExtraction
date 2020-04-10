import csv
import os
from ke_logic.support import Support
from ke_root import ROOT_OUTPUT, ROOT_INPUT
support = Support()
input_file = ROOT_INPUT + os.sep + 'GoogleNgrams' + os.sep + 'GoogleNgrams2.csv'

output = {}
with open(input_file, newline='', encoding='utf-8') as f:
    lines = csv.reader(f, delimiter=';', dialect='excel', )
    lines = list(lines)
    for item in lines:
        freq = float(item[1])
        output[item[0]] = freq
        print('Terms: {0}, Freq: {1}'.format(item[0],freq))

print(len(output))


