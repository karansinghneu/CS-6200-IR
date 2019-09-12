from __future__ import division
from collections import OrderedDict
import os
import sys
from prettytable import PrettyTable


class Evaluation(object):

    def __init__(self):
        '''
        Initialized relevant dictionaries.
        '''
        self.relevance_information = OrderedDict()
        self.retrieval_model_run_information = OrderedDict()
        self.precision_data = OrderedDict()
        self.recall_data = OrderedDict()
        self.average_precision_data = {}
        self.reciprocal_rank_data = {}
        self.precision_at_k_data = {}
        self.retrieval_files = []


    def begin_evaluation(self, file_list, run_name):
        '''
        This method is beginning where all the methoda re computed.
        :param file_list:
        :param run_name:
        :return:
        '''
        self.fetch_retrieval_models(file_list)
        self.precision()
        self.recall()
        self.average_precision()
        self.reciprocal_rank()
        self.precision_at_k()
        self.write_to_file(run_name)

    def write_to_file(self, run_name):
        '''
        This method will write each queries, each document precision and recall values and its average precision and
        average recall in the evaluation folder.
        :param run_name: the name of the model that is being run to compute the map and mrr values.
        :return:
        '''
        map = 0
        mrr = 0
        directory = os.path.dirname(sys.argv[0])
        downloadDir = os.path.join(directory, "../Evaluation/"+run_name)
        if not os.path.exists(downloadDir):
            os.makedirs(downloadDir)
        for queryID in self.retrieval_model_run_information:
            final_file = os.path.join(downloadDir, queryID +run_name)
            file_handler = open(final_file, 'w')
            tableData = PrettyTable(["Query ID", "Document ID", "Precision", "Recall"])
            table_p_at_k = PrettyTable(["Query ID", "Precision @ 5", "Precision @ 20"])
            for docID in self.precision_data[queryID]:
                tableData.add_row([str(queryID), docID, str(self.precision_data[queryID][docID]),
                                   str(self.recall_data[queryID][docID])])

            table_p_at_k.add_row([str(queryID), str(self.precision_at_k_data[queryID]["5"][1]),
                                  str(self.precision_at_k_data[queryID]["20"][1])])

            file_handler.write(tableData.get_string())
            file_handler.write("\n\n")
            file_handler.write(table_p_at_k.get_string())
            file_handler.write("\n\n")

            # write MAP data to the file
            # MAP formula: (Sum of Average Precisions / Number of Vaules)
            file_handler.write("\n\n")
        log = "\n\nMean Average Precision: \n"
        ap = sum(self.average_precision_data.values())
        ap = ap/ len(self.average_precision_data)
        log += str(ap)
        print("map",ap)
        # write MRR data to the file
        # MRR formula: (Sum of Reciprocal Rank Values / Number of Vaules)
        log += "\n\nMean Reciprocal Rank: \n"
        rr = sum(self.reciprocal_rank_data.values()) / len(self.reciprocal_rank_data)
        log += str(rr)
        print("mrr", rr)
        file_handler.write(log)
        file_handler.close()

    def fetch_retrieval_models(self, file_list):
        '''
        This method will fetch all the doc ids and populate them into the dictionary.
        :param file_list:
        :return:
        '''
        for o in os.listdir(file_list):
            if o.endswith(".txt"):
                self.retrieval_files.append(o)
        self.fetch_relevance_data()
        self.populate_model_results(file_list)

    def fetch_relevance_data(self):
        '''
        This method will fetch the relevant files from cacm.rel.txt, to be used to comapre against the document.
        :return:
        '''
        relevance_data_path = "../test-collection/cacm.rel.txt"
        file_handler = open(relevance_data_path, 'r')

        for line in file_handler:
            data_split = line.split(" ")
            query_id = data_split[0]
            doc_id = data_split[2]
            if query_id in self.relevance_information:
                self.relevance_information[query_id].append(doc_id)
            else:
                self.relevance_information[query_id] = []
                self.relevance_information[query_id].append(doc_id)

    def populate_model_results(self,file_list):
        '''
        This method will populate the results for each query into the document along with each documents precision and
        recall, average precision of document and average recall of the document and wrote them into file using pretty tabke.
        :param file_list: the list of files and its data.
        :return:
        '''
        for files in self.retrieval_files:
            path = file_list+"/" + files
            file_handler = open(path, 'r')
            for line in file_handler:
                data_split = line.split(" ")
                # get the query ID
                query_id = data_split[0]
                if query_id in self.relevance_information:
                    # get the Doc ID
                    docID = data_split[2]
                    if query_id in self.retrieval_model_run_information:
                        self.retrieval_model_run_information[query_id].append(docID)
                    else:
                        self.retrieval_model_run_information[query_id] = []
                        self.retrieval_model_run_information[query_id].append(docID)

    def precision(self):
        '''
        This method will compute the precision for each document based on the query id and  puts it into a dictionary.
        :return:
        '''
        for queryID in self.relevance_information:
            if queryID in self.retrieval_model_run_information:
                retrieved_document_count = 0
                relevant_document_count = 0
                for docID in self.retrieval_model_run_information[queryID]:
                    # increment the count whenever a document is encountered
                    retrieved_document_count += 1
                    if queryID in self.relevance_information:
                        if docID in self.relevance_information[queryID]:
                            # increment the count when a relevant document is found
                            relevant_document_count += 1
                    if queryID not in self.precision_data:
                        self.precision_data[queryID] = OrderedDict()
                    self.precision_data[queryID][docID] = relevant_document_count / retrieved_document_count

    def recall(self):
        '''
        This method will compute for each document with respect to the query and puts it into a dictionary.
        :return:
        '''
        for queryID in self.relevance_information:
            if queryID in self.retrieval_model_run_information:
                relevant_document_count = 0

                totalRelevantDocumentCount = len(self.relevance_information[queryID])
                for docID in self.retrieval_model_run_information[queryID]:
                    if queryID in self.relevance_information:
                        if docID in self.relevance_information[queryID]:
                            relevant_document_count += 1
                    if queryID not in self.recall_data:
                        self.recall_data[queryID] = OrderedDict()
                    self.recall_data[queryID][docID] = relevant_document_count / totalRelevantDocumentCount

    def average_precision(self):
        '''
        This method will compute the average percision of each document.
        :return:
        '''
        for queryID in self.relevance_information:
            common_doc_ids = []
            for doc_ids in self.relevance_information[queryID]:
                if doc_ids in self.retrieval_model_run_information[queryID]:
                    common_doc_ids.append(doc_ids)

            if len(common_doc_ids) > 0:
                sum = 0.0
                for docID in common_doc_ids:
                    if docID in self.precision_data[queryID]:
                        sum += self.precision_data[queryID][docID]

                self.average_precision_data[queryID] = sum / len(common_doc_ids)

    def reciprocal_rank(self):
        '''
        This method will compute the rr rank for each document.
        :return:
        '''
        for queryID in self.relevance_information:
            if queryID in self.retrieval_model_run_information:
                doc_list = self.recall_data[queryID]
                for docID in doc_list:
                    if doc_list[docID] != 0:
                        self.reciprocal_rank_data[queryID] = (1 / (list(doc_list.keys()).index(docID) + 1))
                        break

    def precision_at_k(self):
        '''
        This method will compute the precision.
        :return:
        '''
        for queryID in self.relevance_information:
            if queryID in self.retrieval_model_run_information:
                self.precision_at_k_data[queryID] = {}
                self.precision_at_k_data[queryID]["5"] = list(self.precision_data[queryID].items())[4]
                self.precision_at_k_data[queryID]["20"] = list(self.precision_data[queryID].items())[19]

