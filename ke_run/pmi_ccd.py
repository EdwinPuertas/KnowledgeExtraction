from ke_logic.pmi_unsupervised import PMIUnsupervised
from ke_logic.support import Support

pmi = PMIUnsupervised()
support = Support()

corpus_raw = support.import_corpus('CCD_Test',1)
corpus = [i[1] for i in corpus_raw]
seeds = support.import_crea('CSLRecalificados')
seeds_pos = []
seeds_neg = []
for k,v in seeds.items():
    if v == '1':
        seeds_pos.append(k)
    else:
        seeds_neg.append(k)

result_pmi, terms = pmi.calculated_pmi(corpus)
pmi.export_matrix(result_pmi,terms, 'PMI_CorpusCCD')
result_pmi_filtro = pmi.calculated_pmi_seeds(terms, corpus) # importancia de los terminos en el corpus CCD_Test
Support.export_cvs2('TopTerms_CorpusCCD', result_pmi_filtro)

# Top de términos con positivos y negativos
result_pmi_csl = pmi.calculated_pmi_seeds(seeds.keys(), corpus)
Support.export_cvs2('TopTerms_CSLRecalificados', result_pmi_csl) # importancia de los terminos con las semillas
# Top de términos positivos
result_pmi_csl_pos = pmi.calculated_pmi_seeds(seeds_pos, corpus)
Support.export_cvs2('TopTerms_CSLRecalificadosPos', result_pmi_csl_pos)
# Top de términos negativos
result_pmi_csl_neg = pmi.calculated_pmi_seeds(seeds_neg, corpus)
Support.export_cvs2('TopTerms_CSLRecalificadosNeg', result_pmi_csl_neg)