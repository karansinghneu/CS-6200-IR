import os
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter


class Indexer:
    def generate_corpus(self, n, files, corpusName, case_folding=True, punctuation=True):
        '''
        Generate the corpus.
        :param n: n gram
        :param case_folding: True/False
        :param punctuation: True/False
        :return: corpus dictionary
        '''
        dic = {}
        c = 0
        if files is None:
            files = os.listdir("../"+corpusName)
        for filename in files:
            f = open("../"+corpusName+"/" + filename, 'r', encoding="utf8")
            file_content = f.read()
            ngrams_list = list(ngrams(word_tokenize(file_content), n))
            for t in ngrams_list:
                if t not in dic:
                    dic[t] = 0
                dic[t] += 1
            c += 1
            print("generating corpus " + str(c))
        dic = {k[0]: v for k, v in sorted(dic.items(), key=lambda x: x[1], reverse=True)}
        print("diclen " + str(len(dic)))
        return dic

    def create_inverted_index(self, corpus, files, n, corpusName):
        '''
        Create the inverted index.
        :param corpus: input
        :param n: n grams
        :return: Inverted index, dictionary counts
        '''
        cnt = 0
        inv_index = {}
        counts_dict = {}
        for k, v in corpus.items():
            inv_index[k] = []
        if files is None:
            filess = os.listdir("../"+corpusName)
        else:
            filess = files
        for filename in filess:
            cnt += 1
            print("creating inverted index " + str(cnt))
            f = open("../"+corpusName+"/" + filename, 'r', encoding="utf8")
            file_content = f.read()
            ngrams_list = list(ngrams(word_tokenize(file_content), n))
            counts = Counter(ngrams_list)
            counts_dict[filename.split('.')[0]] = len(ngrams_list)
            for c in counts:
                inv_index[c[0]].append((filename.split('.')[0], counts[c]))
        if corpusName =="cacm_stem_corpus":
            return inv_index,counts_dict
        if files is None:
            return inv_index, counts_dict
        return inv_index,counts

    def write_to_file_unigrams(self, filename, inv_index):
        '''
            Write unigrams to a file.
            :param filename: to write
            :param inv_index: of unigrams
            :return: None
        '''
        f = open(filename, 'w', encoding='utf-8')
        for k, v in inv_index.items():
            f.write(k + ' ')
            for i in v:
                f.write(i[0] + ' ' + str(i[1]) + ' ')
            f.write('\n')
        f.close()

    def indexer(self, inverted_file_name, unigram_count_name, corpusName):
        '''
        This methid will create the inverted index.
        :param inverted_file_name: the file ti which the inverted indexes are written.
        :param unigram_count_name: the unigram counts of each document is written into this file.
        :param corpusName: the name of the corpus from which the create this inverted index
        :return:
        '''
        unigram_corpus = self.generate_corpus(1,None,corpusName)
        unigram_inv_index, counts_dict = self.create_inverted_index(unigram_corpus, None, 1,corpusName)
        self.write_to_file_unigrams(inverted_file_name, unigram_inv_index)
        fl = open(unigram_count_name, 'w', encoding='utf-8')
        for k, v in counts_dict.items():
            fl.write(str(k) + ' ' + str(v) + '\n')
        fl.close()
