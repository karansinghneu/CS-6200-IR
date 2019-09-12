from collections import OrderedDict
import math
from Phase1.Common_Models import Commmon


class DMSmoothing():

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



    def get_all_scores(self,query_file,queryFolder, queryFile):
        '''
        This method will get all the scores for each query.
        :param query_file: the file from where we read the quires and query ids
        :param queryFolder: the destination folder where we put our ranked docuemnts for each query
        :param queryFile: append to each query file and to results in the query.
        :return: None
        '''
        print("in ", queryFolder)
        queries = self.common.fetch_input_queries("../"+query_file)
        n = 0
        for queryId, query in queries.items():
            target_dict, query_term_frequency = self.common.fetch_inverted_index(query)
            self.calculate_dmSmoothing(target_dict, queryId, query_term_frequency,queryFolder, queryFile)
            n = n+1
            print(" query", n, queryId)



    def calculate_dmSmoothing(self,target_dict, queryId, query_term_frequency,queryFolder, queryFile):
        """
        This method will calculate BM25 scores for all the documents wrt the query.
        :param target_dict: It has query words and documents
        :param doc_counts: the document and number of words in it.
        :param query_term_frequency: the word frequency of query
        :param queryId: the id of the query entered by the input.
        :return: sorted dictionary with document id nd score in descending order.
        """
        mu = 2000
        C = 0
        doc_res = {}
        for doc_id, dl in self.number_of_terms.items():
            C = C + dl
        for doc_id, dl in self.number_of_terms.items():
            res = 0
            for q_word, qf in query_term_frequency.items():
                try:
                    list_docs = target_dict[q_word]
                except:
                    list_docs = []
                f = 0
                cqi = 0
                dll = 0
                for doc in list_docs:
                    cqi = cqi + float(doc[1])
                    if doc[0] == doc_id:
                        f = float(doc[1])
                        dll = dl
                        pass
                try:
                    total = math.log((f + mu*(cqi/C))/(dll+mu))
                except:
                    total = 0
                res += total
            doc_res[doc_id] = res
        sorted_term_freq = OrderedDict((k, v) for k, v in sorted(doc_res.items(), key=lambda x: x[1], reverse=True))
        self.common.write_to_file(sorted_term_freq, queryId,queryFolder, queryFile)
        return sorted_term_freq



