from wikipedia import wikipedia
from ke_logic.support import Support
from collections import Counter
from textblob import TextBlob as tb
import wikipediaapi
import sys
from _logging import Logging


class WikipediaScraping:
    """
    :Date: 2018-02-16
    :Version: 1.2
    :Author: Edwin Puertas - Pontificia Universidad Javeriana
    :Copyright: Por definir
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
    This class extracts wikipedia content.
    """

    wikipedia.set_lang('es')

    def __init__(self):
        """
        :Date: 2017-02-08
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Copyright: Por definir
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

        This function return inicialized wikipedia object article

        :return: Wikipedia object
        """

        self.support = Support()
        self.media_wiki = wikipediaapi.Wikipedia('es')
        print('WikipediaScraping')

    def search_articles(self, list_word):
        art_list = []
        try:
            for word in list_word:
                art_list += wikipedia.search(word)

            art_list = self.support.normalized_list(art_list)
            return art_list
        except:
            Logging.write_standard_error(sys.exc_info())

    def get_content(self, word):
        try:
            wiki = wikipediaapi.Wikipedia(language='es', extract_format=wikipediaapi.ExtractFormat.WIKI)
            article = wiki.page(word)
            list_tmp = ['Historia','Véase también','Referencias', 'Enlaces externos']
            text = ''
            list_subtitle = []
            if article.exists():
                text = article.summary
                for s in article.sections:
                    if not(s.title in list_tmp):
                        text += s.title + '\n' + s.text
                        list_subtitle.append(s.title)
            text = self.support.clean_text(text)
            return list_subtitle, text
        except:
            Logging.write_standard_error(sys.exc_info())

    def get_article(self, word):
        """
        :Date: 2017-05-09
        :Version: 1.2
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function return wikipedia object article with sets values
        :param word: Name of the wikipedia article to extract
        :type word: Text
        :rtype: Dictionary
        :return: Dictionary of synonyms
        """
        art = {}
        result = None
        try:
            article = self.media_wiki.page(word)
            if article.exists():
                art['Id'] = article.pageid  # Id
                art['Title'] = article.title #Title
                art['SubTitle'] = self.get_content(art['Title'])[0] #SubTitle
                art['Summary'] = article.summary #Summary
                art['Content'] = self.get_content(art['Title'])[1] #Content
                art['Links'] = self.normalized_links(article.links) #Links
                art['Categories'] = self.get_categories(art['Title']) #Categories
                art['URL'] = article.canonicalurl #URL
                art['Weight'] = len(art['Links'])  # Peso del Artículos
                art['Frequency'] = Counter(tb(article.summary + art['Content']))
                result = art
            return result
        except:
            Logging.write_standard_error(sys.exc_info())


    def get_nearby_articles(self,list_articles):
        """
        :Date: 2017-05-09
        :Version: 1.2
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function return list of wikipedia article nearby to seed words
        :param list_articles: List of the wikipedia article
        :type list_articles: List
        :rtype: Dictionary
        :return: Dictionary of nearby articles
        """
        try:
            dic_temp = {}
            for art in list_articles:
                key = self.media_wiki.page(art)
                if key.exists():
                    dic_temp[str(key.title).lower()] = self.get_categories(key.title)
            return dic_temp
        except:
            Logging.write_standard_error(sys.exc_info())

    def get_categories(self,word):
        """
        :Date: 2017-05-09
        :Version: 1.2
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function return list of wikipedia article nearby to seed words
        :param word: Name of the wikipedia article to extract
        :type word: Text
        :rtype: List
        :return: List of categories by article
        """
        try:
            list_categories = self.media_wiki.page(word).categories
            new_list = []
            for item in list_categories:
                item = str(item).lower()
                item = self.support.clean_text(item)
                if not('wiki' in item) and item != '':
                    item = item[10:len(item)]
                    item = item.strip()
                    new_list.append(item)
            new_list = self.support.normalized_list(new_list)
            return new_list
        except:
            Logging.write_standard_error(sys.exc_info())


    def normalized_links(self, list_links):
        """
        :Date: 2017-05-09
        :Version: 1.2
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function return list of wikipedia article nearby to seed words
        :param list_links: list of word
        :type list: Text
        :rtype: List
        :return: List any repeats words
        """
        list_tmp = []
        try:
            for item in list_links:
                text = self.support.clean_text(item).strip()
                if text != '':
                    list_tmp.append(text)

            list_tmp = self.support.normalized_list(list_tmp)
            return list_tmp
        except:
            Logging.write_standard_error(sys.exc_info())

    def compare_categories(self, main_categories, second_categories):
        """
        :Date: 2017-05-09
        :Version: 1.2
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function return True or False if the words in main_categories exist in second_categories.
        :param main_categories: list of words by main categories
        :type list: Text
        :param second_categories: list of words by second categories
        :type list: Text
        :rtype: Boolean
        :return: True or False
        """

        try:
            val = False
            list_tmp = []
            for i in main_categories:
                if (i not in list_tmp) and (i in second_categories):
                    list_tmp.append(i)

            if len(list_tmp) > 0:
                val = True

            return val
        except:
            Logging.write_standard_error(sys.exc_info())

    def creted_corpus_wikipedia(self, seed_words):
        """
        :Date: 2017-05-09
        :Version: 1.2
        :Author: Edwin Puertas - Pontificia Universidad Javeriana
        :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
        This function create a corpus by articles in Wikipedia by seed words.
        :param seed_words: list of seed words
        :type list: Text
        :rtype: XML
        :return: Corpus of Wikipedia Articles
        """

        parent_categories = []
        list_article_invalid = []
        try:
            print('Searching Wikipedia with the seed {0}'.format(str(seed_words)))
            print('Searching Articles in Wikipedia, wait a moment please.')
            list_nearby_parent_articles = self.search_articles(seed_words)
            print('Found articles:{0}'.format(list_nearby_parent_articles))
            print('Building main domain region, wait a moment please.')

            #Saved articles seed words
            list_articles = []
            list_titles = []
            for word in seed_words:
                art = self.get_article(word)
                if art is not None:
                    list_articles.append({'resource': 'Wikipedia', 'title': art['Title'], 'subtitle': art['SubTitle'],
                                      'content': art['Content']})
                    list_titles.append(art['Title'])
                    parent_categories += self.get_categories(str(word))

            parent_categories = self.support.normalized_list(parent_categories)
            print('Main domain region {0}'.format(parent_categories))

            for art in list_nearby_parent_articles:
                child = self.get_article(art)
                child_categories = child['Categories']
                if self.compare_categories(parent_categories, child_categories):
                    if (art is not None) and not (child['Title'] in list_titles):
                        print('Retrieving Information from [{0}], [{1}]'.format(child['Title'],
                                                                                child['URL']))
                        list_articles.append(
                            {'resource': 'Wikipedia', 'title': child['Title'], 'subtitle': child['SubTitle'],
                             'content': child['Content']})
                        list_titles.append(child['Title'])
                        dict_grand_child = {}
                        print('Validating articles children of {0}'.format(str(child['Title'])))
                        print('Validating domain region for articles {0}, wait a moment please.'.format(len(child['Links'])))
                        dict_grand_child = self.get_nearby_articles(child['Links'])
                        for k,v in dict_grand_child.items():
                            grand_child_categories = v
                            if self.compare_categories(parent_categories, grand_child_categories):
                                grand_child = self.get_article(k)
                                if grand_child is not None:
                                    if not (grand_child['Title'] in list_titles):
                                        print('Retrieving Information from [{0}], [{1}]'.format(grand_child['Title'],
                                                                                                              grand_child['URL']))
                                        list_articles.append(
                                            {'resource': 'Wikipedia', 'title': grand_child['Title'], 'subtitle': grand_child['SubTitle'],
                                            'content': grand_child['Content']})
                                        list_titles.append(grand_child['Title'])
                                    else:
                                        print('Article [{0}] excluded!'.format(grand_child['Title']))
                                        if grand_child['Title'] != '':
                                            list_article_invalid.append(grand_child['Title'])

            excluded_items = len(list_article_invalid)
            recovered_items = len(list_articles)
            total_items = excluded_items + recovered_items
            print('\n# Article excluded: [{0}] \n# Articles recovered: [{1}] \nTotal Articles: [{2}]'.format(excluded_items,recovered_items,total_items))
            return list_articles
        except:
            Logging.write_standard_error(sys.exc_info())



if __name__ =='__main__':
    corpus = []
    seed_words = ['Banco', 'Cuentas', 'Cuenta de Ahorros', 'Crédito', 'Inversión', 'Deuda', 'Bancolombia' ]
    ws = WikipediaScraping()
    corpus = ws.creted_corpus_wikipedia(seed_words)
    Support.export_xml('CorpusGeneralWikipedia', corpus)
    print('Process Completed Successfully ')
    for k in corpus:
        print(k)

