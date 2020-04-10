from ke_logic.terminology_extraction import TerminologyExtraction
from ke_logic.support import Support
from ke_root import ROOT_OUTPUT, ROOT_INPUT

dict_corpus_terms = {}
support = Support()
raw_corpus_bank = support.import_xml('CorpusBancos','row')

corpus_raw_Wikipedia = []
corpus_raw_Webpage = []
for item in raw_corpus_bank:
    if item['resource'] == 'Wikipedia':
        corpus_raw_Wikipedia.append([item['title'], str(item['content']).strip()])
    elif item['resource'] == 'webpage':
        list_content = str(item['content'][1:len(item['content'])-1]).replace("'", '').split(',')
        content = ''
        for i in list_content:
            content += i + ' '
        corpus_raw_Webpage.append([item['title'],content])


for i in corpus_raw_Webpage:
    print('Title: {0} \nContent: {1}'.format(i[0], i[1]))