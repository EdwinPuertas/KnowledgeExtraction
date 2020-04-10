import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_OUTPUT = ROOT_DIR + os.sep + 'ke_data' + os.sep + 'output' + os.sep
ROOT_INPUT = ROOT_DIR + os.sep + 'ke_data' + os.sep + 'input' + os.sep
ROOT_DIR_CONFIG = "{0}{1}ke_configuration{1}".format(ROOT_DIR, os.sep)
GENERAL_CORPUS = ROOT_DIR + os.sep + 'ke_data' + os.sep + 'input' + os.sep + 'raw.es'+ os.sep
