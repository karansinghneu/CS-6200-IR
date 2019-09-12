
from Phase1.Cleaner import Cleaner

class CacmStemmer:

    def index_corpus(self):
        '''
        This method will clean the cacm - stem corpus.
        :return:
        '''
        cleaner = Cleaner()
        cleaner.clean_file_stem()
