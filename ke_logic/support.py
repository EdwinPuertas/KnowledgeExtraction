import csv
import os
import re
import string
from ke_root import ROOT_OUTPUT, ROOT_INPUT, GENERAL_CORPUS
from xml.etree import ElementTree as ET



class Support:
    """
    :Date: 2018-02-06
    :Version: 0.1
    :Author: Edwin Puestas - Pontificia Universidad Javeriana, Bogotá
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA
    This class has static methods
    """
    def __init__(self):
        """
        :Date: 2018-02-06
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        Constructor for the class
        :rtype: object
        :return: Utils object
        """

    @staticmethod
    def clean_text(text):
        """
        :Date: 2017-04-05
        :Version: 0.1
        :Author: Jan Medina - Pontificia Universidad Javeriana, Cali
        This function deletes all the words that are matching with the regex
        :param tokenized_text:
        :return: text cleaner by pattern
        """
        try:
            text = re.sub(r'((http|https|ftp|smtp).\/\/\d*|w{3}\..)|w{3}.', '', text) # Cleaning all the urls in the text
            text = re.sub(r'\w\d+|\d+\w|\d+|\d+\\|\/|\-|\s\d+|\w{22}', '', text)# Elimina número y númeron con letra
            text = re.sub(r'\©|\×|\⇔|\_|\»|\«|\~|\!|\@|\#|\$|\€|\&|\(|\)', '', text)# Elimina caracteres especilaes
            text = re.sub(r'\-|\/|\;|\:|\’|\‘|\Â|\�|\”|\“|\"|\'|\`|\}|\{', '', text)# Elimina caracteres especilaes
            text = re.sub(r'[\+\*\<\>\=\^\%]', '', text)  # Elimina operadores
            text = re.sub(r'\s[ \t]|\n\W', '', text)  # Eliminamos los espacios en blanco y tabuladores al comienzo de cada línea
            text = re.sub(r'"]+', '', text) # Elimina comillas dobles
            text = re.sub(r'(.)\1{2,}', '', text)  # Elimina caracteres que se repiten mas de dos veces
            text = re.sub(r'\Bltr|\bltr', '', text)  # Elimina ltr de caualquier texto
            return text
        except Exception as e:
            print("\t ERROR clean_text: ", e)
            return None

    def normalized_list(self, list):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method exports the contents of a dictionary to a CSV file.
        :param list: list of words
        :type list: list
        :rtype: list
        :return: list normalized
        """
        try:
            new_list = []
            for i in list:
                text = self.clean_text(i)
                if text is not None or text != '':
                    new_list.append(text.lower())

            d = {}
            new_list = [d.setdefault(x, x) for x in list if x not in d]
            return new_list
        except Exception as e:
            print("\t ERROR normalized_list: ", e)
            return None

    @staticmethod
    def stop_word(term):
        try:
            result = False
            stop_word = []
            stop_word.extend(['estar','dejanos', 'esperandote', 'safari', 'grupo', 'internet'])
            stop_word.extend(['wikipedia','wiki','navegador', 'ltr','ltd', 'aqui', 'traves'])
            stop_word.extend(['vez', 'tener','segun','web','pais','asi', 'aqui','dia','dias', 'ano'])
            stop_word.extend(['bogota','suenos', 'clic', 'ira', 'of', 'bank', 'to','eeuu'])
            stop_word.extend(['medellin', 'by', 's','b', 'd','copyright', 'un clic', 'world', 'wells'])
            stop_word.extend(['the', 'espana','navegadores web','inc','web chrome','los navegadores','app'])

            if term in stop_word:
                result = True

            return result
        except Exception as e:
            print("\t ERROR stop_word: ", e)
            return None

    def import_general_corpus(self):
        try:
            root = GENERAL_CORPUS
            output = {}
            list_file = os.listdir(root)
            text = ''
            doc = 1
            for item in list_file:
                path_file = root + item
                file = open(path_file, mode='r', encoding="latin-1")
                lines = file.readlines()
                for i in lines:
                    line = str(i).strip()
                    if line != '':
                        if line == 'ENDOFARTICLE':
                            output[doc] = text
                            doc += 1
                            text = ''
                        else:

                            text += line
                            print(line)
                file.close()
            print('Corpus [{0}] import general corpus successful')

        except Exception as e:
            print("\t ERROR import general corpus: ", e)
        return output

    def import_corpus(self, file_input, id=True , key=0, content=1, encoding='utf-8'):
        try:
            i = 0
            output = []
            file = ROOT_INPUT + str(file_input) + '.csv'
            with open(file, newline='', encoding=encoding) as f:
                lines = csv.reader(f, delimiter=';', dialect='excel', )
                lines = list(lines)
                for item in lines:
                    text = str(item[content]).strip()
                    if text != '':
                        text = text.lower()
                        if id:
                            i += 1
                            output.append([i, self.clean_text(text)])
                        else:
                            output.append([item[key], self.clean_text(text)])

            print('Corpus [{0}] import successful'.format(file_input+'.csv'))
        except Exception as e:
            print("\t ERROR import_corpus: ", e)
        return output

    def import_crea(self, file_input):
        try:
            output = {}
            path = ROOT_INPUT + str(file_input) + '.csv'
            file = open(path, encoding='utf-8')
            lines = csv.reader(file, dialect='excel', delimiter=';')
            lines = list(lines)
            for item in lines:
                output[item[0].lower()] = float(item[2])
            return output
        except Exception as e:
            print("\t ERROR import_corpus: ", e)
            return None

    def import_cvs_list(self, input_file, delimiter, cols):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method translates the contents of a CSV file into a list.
        :param input_file: name of the intput file
        :type input_file: text
        :param delimiter: delimiter
        :type delimiter: Character of delimiter
        :param cols: Number of columns in the CSV file
        :type cols:  Numeric
        :rtype: List
        :return: List of words
        """
        try:
            cols = int(cols)
            path = ROOT_INPUT + input_file + '.csv'
            file = open(path, encoding='utf-8')
            lines = csv.reader(file, dialect='excel', delimiter=delimiter)
            list_output = []
            for item in lines:
                list_row = []
                for row in range(0, cols):
                    list_row.append(item[row].strip())
                list_output.append(list_row)

            return list_output
        except Exception as e:
            print("\t ERROR import_cvs_list: ", e)
            return None

    def import_cvs_dict(self, input_file, delimiter):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method translates the contents of a CSV file into a dictionary.
        :param input_file: name of the intput file
        :type input_file: text
        :param delimiter: delimiter
        :type delimiter: Character of delimiter
        :rtype: Dictionary
        :return: Dictionary
        """
        try:
            dict_temp = {}
            path = ROOT_INPUT + input_file + '.csv'
            file = open(path, encoding='utf-8')
            lines = csv.reader(file, dialect='excel', delimiter=delimiter)
            lines = list(lines)
            for item in lines:
                list_temp = item[1].split(',')
                dict_temp[item[0].lower()] = list_temp
            return dict_temp
        except Exception as e:
            print("\t ERROR import_cvs_dict: ", e)
            return None

    @staticmethod
    def indent(elem, level=0):
        try:
            i = "\n" + level * "  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
                for elem in elem:
                    Support.indent(elem, level + 1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
        except Exception as e:
            print("\t ERROR indent: ", e)
            return None

    @staticmethod
    def import_xml(input_file, tag='row'):

        try:
            list_dict = []
            path_input = ROOT_INPUT + input_file + '.xml'
            file_input = open(path_input, encoding='utf8')
            tree = ET.parse(file_input)
            root = tree.getroot()
            for rows in root.iter(tag):
                dict_elements = {}
                for row in rows:
                    dict_elements[row.tag] = row.text
                list_dict.append(dict_elements)
            print('Corpus [{0}] import successful'.format(input_file + '.xml'))
            return list_dict
        except Exception as e:
            print("\t ERROR import_xml: ", e)
            return None

    @staticmethod
    def export_xml(output_file, list):
        try:
            path_output = ROOT_OUTPUT + output_file + '.xml'
            doc = ET.Element(output_file)
            rows = ET.SubElement(doc, "rows")
            for item in list:
                row = ET.SubElement(rows, "row")
                for k, v in item.items():
                    ET.SubElement(row, str(k)).text = str(v)

            Support.indent(doc)
            tree = ET.ElementTree(doc)
            tree.write(path_output,xml_declaration=True, encoding='utf-8', method="xml")
            print('XML file successfully exported!')
        except Exception as e:
            print("\t ERROR export_xml: ", e)
            return None

    @staticmethod
    def export_dict_cvs(output_file, dict):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method exports the contents of a dictionary to a CSV file.
        :param file_output: name of the output file
        :type file_output: text
        :param dict: dictionary of words
        :type dict: dictionary
        :rtype:
        :return: None
        """
        try:
            path_output = ROOT_OUTPUT + output_file + '.csv'
            with open(path_output, 'w', newline='\n', encoding='utf-8') as output:
                writer = csv.writer(output, delimiter=';')
                for k, v in dict.items():
                    value = str(v).lower()
                    value.rstrip(string.whitespace)
                    writer.writerow([str(k).lower(), value])

            print('CSV file successfully exported!')
        except Exception as e:
            print("\t ERROR export_cvs: ", e)
            return None

    @staticmethod
    def export_corpus_cvs(output_file, dict):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method exports the contents of a dictionary to a CSV file.
        :param file_output: name of the output file
        :type file_output: text
        :param dict: dictionary of words
        :type dict: dictionary
        :rtype:
        :return: None
        """
        try:
            path_output = ROOT_OUTPUT + output_file + '.csv'
            with open(path_output, 'w', newline='\n', encoding='utf-8') as output:
                writer = csv.writer(output, delimiter=';')
                for k1, v1 in dict.items():
                    dict_tmp = {}
                    dict_tmp.update(v1)
                    for k2, v2 in dict_tmp.items():
                        list_tmp = []
                        list_tmp.append(k1)
                        list_tmp.append(k2)
                        list_tmp.append(v2)
                        writer.writerow(list_tmp)

            print('CSV file successfully exported!')
        except Exception as e:
            print("\t ERROR export_corpus_cvs: ", e)
            return None

    @staticmethod
    def export_corpus_matcher(output_file, dict):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method exports the contents of a dictionary to a CSV file.
        :param file_output: name of the output file
        :type file_output: text
        :param dict: dictionary of words
        :type dict: dictionary
        :rtype:
        :return: None
        """
        try:
            path_output = ROOT_OUTPUT + output_file + '.csv'
            with open(path_output, 'w', newline='\n', encoding='utf-8') as output:
                writer = csv.writer(output, delimiter=';')
                for k1, v1 in dict.items():
                    dict_tmp = {}
                    dict_tmp.update(v1)
                    for k2, v2 in dict_tmp.items():
                        list_tmp = []
                        list_tmp.append(k1)
                        list_tmp.append(k2)
                        dict_tmp2 = {}
                        dict_tmp2.update(v2)
                        for k3, v3 in dict_tmp2.items():
                            list_tmp.append(v3)
                        writer.writerow(list_tmp)

            print('CSV file successfully exported!')
        except Exception as e:
            print("\t ERROR export_corpus_cvs: ", e)
            return None

    @staticmethod
    def export_list_cvs(output_file, list):
        """
        :Date: 2018-02-12
        :Version: 1.0
        :Author: Edwin Puertas - Pontificia Universidad Javeriana, Bogotá
        This method exports the contents of a dictionary to a CSV file.
        :param file_output: name of the output file
        :type file_output: text
        :param dict: dictionary of words
        :type dict: dictionary
        :rtype:
        :return: None
        """
        try:
            path_output = ROOT_OUTPUT + output_file + '.csv'
            with open(path_output, 'w', newline='\n', encoding='UTF-8') as output:
                writer = csv.writer(output, delimiter=';')
                for item in list:
                    writer.writerow(item)

            print('CSV file successfully exported!')
        except Exception as e:
            print("\t ERROR export_cvs2: ", e)
            return None

