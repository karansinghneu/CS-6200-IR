
import  os

class Stopper:

    inverted_index = {}

    def __init__(self, inverted_index):
        '''
        This method initialized the inverted index and number of terms read from the file.
        :param inverted_index: a dictionary with key as word and values as tuples with docId and frequency of word in document.
        '''
        self.inverted_index = inverted_index

    def get_stop_words(self):
        '''
        This method will fetch the common words, from the file and add them to a list.
        :return: a list of stop words.
        '''
        liste = []
        f = open("../test-collection/common_words")
        for line in f:
            liste.append(line.strip());
        return liste

    def create_new_index(self):
        '''
        THis method will create a new index with all the stop words removed.
        :return: will return new index with no stop words.
        '''
        stop_words = self.get_stop_words()
        new_index = {}
        for k, v in self.inverted_index.items():
            if k not in stop_words:
                val = []
                for e in v:
                    val.append((e[0], e[1]))
                new_index[k] = val
        return new_index


    def create_new_term(self):
        '''
        This method will update unigram count of each file after removing the stop word.
        :return: new terms with no stop words included.
        '''
        files = os.listdir("../corpus")
        new_terms = {}
        for filename in files:
            f = open("../corpus/" + filename, 'r', encoding="utf8")
            file_content = f.read()
            ngrams_list = file_content.split()
            new_list = []
            for n in ngrams_list:
                if n not in self.get_stop_words():
                    new_list.append(n)
            new_terms[filename.split('.')[0]] = len(new_list)
        return new_terms