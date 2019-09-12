import os
import nltk as nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from Phase1.Indexer import Indexer
from collections import OrderedDict


class PseudoRelevance():

    def fetch_input_queries(self, file_name):
        '''
        This method will fetch the input queries required to compute the expansions.
        :param file_name: name of the file from which the queries are fetched to be expanded.
        :return:
        '''
        queries_dict = {}
        with open(file_name) as file_data:
            count = 1
            each_line = file_data.readline()
            while each_line:
                each_line.strip()
                query_id = each_line.split(None, 1)[0]
                query = ' '.join(each_line.split()[1:])
                # print("Line {}: {}".format(query_id, query))
                queries_dict[query_id] = query
                each_line = file_data.readline()
                count += 1
        return queries_dict

    def get_all_expansion_queries(self,pseudo_rel_file_name):
        '''
        The queries on which the query expansion has to be done are expanded and written to a file.
        :param pseudo_rel_file_name: name of the file where this expanded queries will be added;.
        '''
        queries = self.fetch_input_queries("../queries_clean.txt")
        f = open(pseudo_rel_file_name, "w")
        new_queries ={}
        for queryId, query in queries.items():
            file_content_lst = self.get_top_docs(queryId)
            new_query = self.query_expansion(query, 10, 5, file_content_lst)
            new_queries[queryId] =  new_query

        sorted_queries = OrderedDict((k, v) for k, v in sorted(new_queries.items(), key=lambda x: int(x[0])))
        for k, v  in sorted_queries.items():
            f.write(str(k) + ' ' + v + '\n')
        f.close()

    def get_top_docs(self, queryId):
        '''
        This method will get top k documents for the respective query.
        :param queryId: the id of the query
        :return: list of top docs.
        '''
        fileName = queryId + " DIRICHLET.txt"
        with open("../dm_smoothing/" + fileName, encoding="utf8") as file_data:
            file_content_lst = file_data.read().split('\n')
        return file_content_lst

    def query_expansion(self, query, k, n, file_content_lst):
        '''
        This method will expand the queriees which top frequenct words from the fetched docuemnts.
        :param query: the input each query
        :param k: the number of docuemnts used to get top frequenct words.
        :param n: the number of words fetched form k top documents.
        :param file_content_lst: the file content with docids
        :return: new expanded query.
        '''
        indexer = Indexer()
        query = query.lower()
        stop_words = set(stopwords.words('english'))

        query_lst = query.split()
        file_list = []
        for i in range(k):
            fname = file_content_lst[i].split(' ')[2]
            file_list.append(fname+".txt")
        corpus = indexer.generate_corpus(1, file_list,"corpus")
        inv_index, counts = indexer.create_inverted_index(corpus, file_list, 1, "corpus")
        freq_counter = {}
        for key, val in counts.items():
            if key[0] not in stop_words:
                freq_counter[key[0]] = val
        freq_counte = OrderedDict((k, v) for k, v in sorted(freq_counter.items(), key=lambda x: x[1], reverse=True))
        # if not os.path.exists("../Frequencies"):
        #     os.makedirs("../Frequencies")
        # f = open("../Frequencies/counts_" + query.split()[0] + '_k' + str(k) + "_n" + str(n) + ".txt", 'w')
        # for key, val in freq_counte.items():
        #     f.write(key + '->' + str(val) + '\n')
        #
        # inv_index = {key: val for key, val in sorted(inv_index.items(), key=lambda x: len(x[1]), reverse=True)}
        expansion_terms = []
        for i in freq_counte:
            if i not in stop_words and i not in query_lst:
                expansion_terms.append(i)

        terms_to_add = expansion_terms[:n]
        print('New terms added are:')
        for t in terms_to_add:
            query_lst.append(t)
            print(t)

        new_query = ''
        for t in query_lst:
            new_query += t + ' '
        return new_query

