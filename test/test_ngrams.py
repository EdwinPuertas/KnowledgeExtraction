from ke_logic.terminology_extraction import TerminologyExtraction


te = TerminologyExtraction()

value = te.generate_ngrams('Esto es una prueba de ngrmas', 1, 4)
print(value)

nlp  = te.get_nlp('una prueba')
print(nlp)