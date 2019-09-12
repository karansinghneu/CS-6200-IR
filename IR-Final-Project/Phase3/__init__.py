from Phase3.Evaluation import Evaluation
from Phase1.TF_IDF import TF_IDF
from Phase1.Stopper import Stopper
import os

def read_inverted_index(inverted_index_filename):
    '''
    This method will read inverted index and create a dictionary of inverted indexes.
    :param inverted_index_filename:
    :return:
    '''
    fopen = open(inverted_index_filename, 'r', encoding='utf-8')
    dic = {}
    for line in fopen:
        lst = list(line.split())
        key = lst[0]
        dic[key] = []
        i = 1
        print("list length", len(lst))
        while i < len(lst):
            dic[key].append((lst[i], lst[i + 1]))
            i += 2
    return dic


def read_number_of_terms(unigram_couts_filename):
    fopen = open(unigram_couts_filename, 'r', encoding='utf-8')
    dic = {}
    for line in fopen:
        content = line.strip().split()
        dic[content[0]] = int(content[1])
    return dic

def run_tfidf(inverted_index, number_of_terms):

    stopper = Stopper(inverted_index)
    new_index = stopper.create_new_index()
    new_terms = stopper.create_new_term()
    tf_idf = TF_IDF(new_index, new_terms)
    tf_idf.get_all_scores("/pseudo_relevance_feedback/Expanded_queries_dms_prf.txt", "../tf_idf_stop_expand", "TF_IDF")

def run_bm25(inverted_index, number_of_terms):
    stopper = Stopper(inverted_index)
    new_index = stopper.create_new_index()
    new_terms = stopper.create_new_term()
    tf_idf = TF_IDF(new_index, new_terms)
    tf_idf.get_all_scores("/semantic_query_expansion/Expanded_queries_bm25_sqe.txt", "../bm_25_stop_sqe", "BM25")

def run_inverted_index():
    inverted_index_file_name = os.path.join('../inverted_indexes/', "corpus_inverted_index.txt")
    inverted_index = read_inverted_index(inverted_index_file_name)
    unigram_count_file_name = os.path.join('../inverted_indexes/', "corpus_unigram_counts.txt")
    number_of_terms = read_number_of_terms(unigram_count_file_name)
    return inverted_index,number_of_terms

if __name__ == '__main__':
    inverted_index, number_of_terms = run_inverted_index()
    run_tfidf(inverted_index, number_of_terms)
    run_bm25(inverted_index,number_of_terms)
    evaluation1 = Evaluation()

    evaluation1.begin_evaluation("../tf_idf","TF_IDF_BASE")
    evaluation1.begin_evaluation("../bm25", "BM25_BASE")
    evaluation1.begin_evaluation("../dm_smoothing", "D_SMOOTH_BASE")
    evaluation1.begin_evaluation("../Lucene_base", "LUCENE_BASE")
    evaluation1.begin_evaluation("../bm25_prf", "BM25_PRF")
    evaluation1.begin_evaluation("../dm_smoothing_prf", "D_SMOOTH_PRF")
    evaluation1.begin_evaluation("../Lucene_base", "LUCENE_BASE")
    evaluation1.begin_evaluation("../bm_25_sqe", "BM25_SQE")
    evaluation1.begin_evaluation("../dm_smoothing_sqe", "D_SMOOTHING_SQE")
    evaluation1.begin_evaluation("../bm25_stop","BM25_STOP")
    evaluation1.begin_evaluation("../dm_smoothing_stop", "D_SMOOTHING_STOP")
    evaluation1.begin_evaluation("../bm_25_stop_sqe", "BM25_STOP_SQE")
    evaluation1.begin_evaluation("../tf_idf_stop_expand", "TF_IDF_STOP_PRF")