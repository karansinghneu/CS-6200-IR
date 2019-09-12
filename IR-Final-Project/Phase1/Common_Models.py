import os


class Commmon:
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

    def write_to_file(self, sorted_term_freq, queryId, queryFolder, queryFile):
        """
        This method is to write into the document and scores into file in the required format
        :param sorted_term_freq: the documment and score to be written into the file.
        :param queryId: the Id of the query.
        :return: None
        """
        print("in run file")
        if not os.path.exists(queryFolder):
            os.makedirs(queryFolder)
        filename = os.path.join(queryFolder + "/" + str(queryId) + " " + queryFile + ".txt")
        with open(filename, 'w', encoding="utf-8") as file_data:
            count = 0
            for myKey, myVal in sorted_term_freq.items():
                if count == 100:
                    pass
                else:
                    file_data.write(
                        str(queryId) + " Q0 " + str(myKey) + " " + str(count) + " " + str(myVal) + " " + queryFile)
                    file_data.write("\n")
                    count = count + 1
        file_data.close()

    def fetch_input_queries(self, file_name):
        '''
        This method will fetch the input queries from the file and create a dictionary with key as query Id an value as query.
        :param file_name:  name of the queries file from which dictionary has to be created.
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

    def fetch_inverted_index(self, query_line):
        """
        Method to fetch inverted indexes of the certain input query terms only.
        :param inverted_index: the dictionary with all query terms
        :return: target_dict with inverted indexes of only query terms, query_term_freq term frequency of each word in query.
        """
        query_term_freq = {}
        words = query_line.split()
        target_dict = {}
        for word in words:
            if word in self.inverted_index:
                target_dict[word] = self.inverted_index[word]
        for word in words:
            if word in query_term_freq:
                query_term_freq[word] = query_term_freq[word] + 1
            else:
                query_term_freq[word] = 1
        return target_dict, query_term_freq

    def get_all_cacm_stem_scores(self, query_file, queryFolder, queryFile):
        '''
        This method will specifically work for getting the scores for cacm stem queries.
        :param query_file: the file from which we will get the stemmed queries
        :param queryFolder:
        :param queryFile:
        :return:
        '''
        queries_dict = {}
        with open("../" + query_file) as file_data:
            count = 1
            each_line = file_data.readline()
            while each_line:
                each_line.strip()
                query_id = count
                query = ' '.join(each_line.split())
                # print("Line {}: {}".format(query_id, query))
                queries_dict[query_id] = query
                each_line = file_data.readline()
                count += 1
        n = 0
        for queryId, query in queries_dict.items():
            target_dict, query_term_frequency = self.fetch_inverted_index(query)
            self.calculate_bm25(target_dict, queryId, query_term_frequency, queryFolder, queryFile)
            n = n + 1
            print(" query", n, queryId)
