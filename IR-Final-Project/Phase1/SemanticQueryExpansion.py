from collections import OrderedDict
import nltk as nltk
nltk.download('wordnet')
from nltk.corpus import wordnet


class SemanticQueryExpansion():

    def fetch_input_queries(self, file_name):
        '''
        This method will fetch the queries from the file name entered as input and reutrn a dictionary.
        :param file_name: the file from which qeuries are read
        :return: the dictionary of queries with key as query id and value as query.
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

    def get_all_expansion_queries(self, sqe_file_name, inverted_index):
        '''
        This methof will fetch all the queries, froim the queries file and add write the expanded queries to file.
        :param sqe_file_name: the file where new expanded queires will be added.
        :return:
        '''
        queries = self.fetch_input_queries("../queries_clean.txt")
        n = 0
        new_queries = {}
        f = open(sqe_file_name, "w")
        for queryId, query in queries.items():
            new_querie = self.expand_query(query, queryId, inverted_index)
            # print(new_querie)
            new_queries[queryId] = new_querie
        sorted_queries = OrderedDict((k, v) for k, v in sorted(new_queries.items(), key=lambda x: int(x[0])))
        for k, v in sorted_queries.items():
            f.write(str(k) + ' ' + v + '\n')
        f.close()

    def getsynonymsandanonyms(self,que):
        '''
        This method will get synonyms and anotonyms for a given word. 
        :param que: the query word.
        :return: 
        '''
        synonyms = []
        antonyms = []
        derivations = []
        for syn in wordnet.synsets(que):
            for l in syn.lemmas():
                if l.name() not in synonyms:
                    synonyms.append(l.name())
                if l.antonyms() and l.antonyms()[0].name() not in antonyms:
                    antonyms.append(l.antonyms()[0].name())
                if l.derivationally_related_forms():
                    derivations.append(l.derivationally_related_forms()[0].name())
        return synonyms, antonyms, derivations

    def expand_query(self, query, queryId, inverted_index):
        '''
        This method will expand the query and output the new query/
        :param query: the actual query
        :param queryId: the id of the query
        :param inverted_index: the inverted index
        :return: new expanded query
        '''
        queries = query.split()
        list_res = []
        for que in queries:
            syns, ants, deris = self.getsynonymsandanonyms(que)
            wrds = inverted_index.keys()
            new_words = []
            scnt = 0
            acnt = 0
            dcnt = 0
            for s in syns:
                if s in inverted_index and len(inverted_index[s]) > 800 and scnt < 2:
                    new_words.append(s)
                    scnt += 1
            for a in ants:
                if a in inverted_index and len(inverted_index[a]) > 800 and acnt < 2:
                    new_words.append(a)
                    acnt = 1
            for d in deris:
                if d in inverted_index and len(inverted_index[d]) > 800 and dcnt < 2:
                    new_words.append(d)
                    dcnt = 1
            list_res.extend(new_words)
        list_res = list(set(list_res))
        new_query = ' '.join(list_res)
        new_querie = query + " " + new_query
        print(query, '------>', new_querie)
        return new_querie