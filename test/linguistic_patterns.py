from nltk import tokenize
from nltk import tag
import nltk
# JJ is adjetivo
# NN es suntantivo

text2 = "I am going to the marke to buy vegetables and some fruits."
text = "En este trabajo presentamos una nueva estrategia para crear treebanks de lenguas con pocos recursos para el análisis sintáctico. El método consiste en la adaptación y combinación de diferentes treebanks anotados con dependencias universales de variedades lingüísticas próximas, con el objetivo de entrenar un analizador sintáctico para la lengua elegida, en nuestro caso el gallego. "
grammar = r"""
     NP: {<JJ><N.*> | <N.*><JJ> | <N.*><N.*> | <DT>*<N.*>}   # noun phrase chunks """
cp = nltk.RegexpParser(grammar)
sents = tokenize.sent_tokenize(text.lower())
result = {}
for sent in sents:
    clause = tokenize.word_tokenize(sent)
    tagged_sent = tag.pos_tag(clause)
    chunked_tree = cp.parse(tagged_sent)
    #print(chunked_tree)

    for subtree in chunked_tree.subtrees():
        if subtree.label() == "NP":
            size = len(subtree.leaves())
            if size == 1:
                term = subtree.leaves()[0][0]
                result[term] = subtree.leaves()
                print('{0}: {1}'.format(term, subtree.leaves()))
            elif size == 2:
                term = subtree.leaves()[0][0] + ' ' + subtree.leaves()[1][0]
                result[term] = subtree.leaves()
                print('{0}: {1}'.format(term, subtree.leaves()))




