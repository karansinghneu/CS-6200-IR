from collections import OrderedDict
import math
from Phase1.Common_Models import Commmon

class TF_IDF():

    inverted_index = {}
    number_of_terms = {}

    def __init__(self, inverted_index, number_of_terms):
        '''
        This method initialized the inverted index and number of terms read from the file.
        :param inverted_index: a dictionary with key as word and values as tuples with docId and frequency of word in document.
        :param number_of_terms: a dictionary with key as doc id and values as number of words in the document.
        '''
        self.inverted_index = inverted_index
        self.number_of_terms = number_of_terms
        self.common = Commmon(inverted_index, number_of_terms)



    def get_all_scores(self,query_file, queryFolder, queryFile):
        '''
        This method will get all the scores for each query.
        :param query_file: the file from where we read the quires and query ids
        :param queryFolder: the destination folder where we put our ranked docuemnts for each query
        :param queryFile: append to each query file and to results in the query.
        :return: None
        '''
        queries = self.common.fetch_input_queries("../"+query_file)
        n = 0
        for queryId, query in queries.items():
            target_dict, query_term_frequency = self.common.fetch_inverted_index(query)
            self.compute_tf_df_score(target_dict, queryId, query_term_frequency, queryFolder, queryFile)
            n = n+1
            print("query",n, queryId)


    def compute_tf_df_score(self, target_dict, queryId, query_term_frequency, queryFolder, queryFile):
        N = 3024
        dict_tf_idf = {}
        n = 0
        for doc_id, dl in self.number_of_terms.items():
            score = 0
            for q_word, qf in query_term_frequency.items():
                try:
                    list_docs = target_dict[q_word]
                except:
                    list_docs = []
                f = 1
                tf = 0
                for doc in list_docs:
                    if doc[0] == doc_id:
                        f = float(doc[1])
                        tf = f / dl
                        pass
                df = len(list_docs)
                idf = 0
                if df != 0:
                    idf = math.log((N / df), 10)
                score += (tf * idf)
            dict_tf_idf[doc_id] = score
            n = n+1
            #print(n)
        sorted_term_freq = OrderedDict((k, v) for k, v in sorted(dict_tf_idf.items(), key=lambda x: x[1], reverse=True))
        self.common.write_to_file(sorted_term_freq, queryId, queryFolder, queryFile)
        return dict_tf_idf

