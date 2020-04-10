import ast
from ke_logic.support import Support

support = Support()
#get_tfidf = ut.import_xml('TerminosBancosTFIDF')
crea = support.import_cvs_list('CREA',';',3)

for item in crea:
    print('Term: {0}, Freq Absoluta: {1}, Freq Normalizada: {2}'.format(item[0], item[1], item[2]))









