from collections import OrderedDict
import math
from Phase1.Common_Models import Commmon


class BM25():
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

    def get_all_scores(self, query_file, queryFolder, queryFile):
        '''
        This method will get all the scores for each query.
        :param query_file: the file from where we read the quires and query ids
        :param queryFolder: the destination folder where we put our ranked docuemnts for each query
        :param queryFile: append to each query file and to results in the query.
        :return: None
        '''
        queries = self.common.fetch_input_queries("../" + query_file)
        n = 0
        for queryId, query in queries.items():
            target_dict, query_term_frequency = self.common.fetch_inverted_index(query)
            self.calculate_bm25(target_dict, queryId, query_term_frequency, queryFolder, queryFile)
            n = n + 1
            print(" query", n, queryId)

    def calculate_bm25(self, target_dict, queryId, query_term_frequency, queryFolder, queryFile):
        """
        This method will calculate BM25 scores for all the documents wrt the query.
        :param target_dict: It has query words and documents
        :param doc_counts: the document and number of words in it.
        :param query_term_frequency: the word frequency of query
        :param queryId: the id of the query entered by the input.
        :return: sorted dictionary with document id nd score in descending order.
        """
        sum1 = sum(self.number_of_terms.values())
        avdl = sum1 / len(self.number_of_terms)
        N = 3204
        k1 = 1.2
        k2 = 100
        b = 0.75
        doc_res = {}
        for doc_id, dl in self.number_of_terms.items():
            K = k1 * ((1 - b) + (b * (dl / avdl)))
            res = 0
            for q_word, qf in query_term_frequency.items():
                try:
                    ni = len(target_dict[q_word])
                    list_docs = target_dict[q_word]
                except:
                    ni = 0
                    list_docs = []
                fii = 0
                for doc in list_docs:
                    if doc[0] == doc_id:
                        fii = float(doc[1])
                        pass
                try:
                    qw = math.log((N - ni + 0.5) / (ni + 0.5))
                except:
                    qw = 0
                nw = ((k1 + 1) * fii) / (K + fii)
                qqw = ((k2 + 1) * qf) / (k2 + qf)
                total = qw * nw * qqw
                res += total
            doc_res[doc_id] = res
        sorted_term_freq = OrderedDict((k, v) for k, v in sorted(doc_res.items(), key=lambda x: x[1], reverse=True))
        self.common.write_to_file(sorted_term_freq, queryId, queryFolder, queryFile)
        return sorted_term_freq
