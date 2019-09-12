from Phase1.Indexer import Indexer
from Phase1.Cleaner import Cleaner
from Phase1.TF_IDF import TF_IDF
from Phase1.BM25 import BM25
from Phase1.DMSmoothing import DMSmoothing
from Phase1.PseudoRelevance import PseudoRelevance
from Phase1.SemanticQueryExpansion import SemanticQueryExpansion
from Phase1.Stopper import Stopper
from Phase1.CacmStemmer import CacmStemmer
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
    '''
    This method will read number of unigrams and create a dictionary.
    :param unigram_couts_filename:
    :return:
    '''
    fopen = open(unigram_couts_filename, 'r', encoding='utf-8')
    dic = {}
    for line in fopen:
        content = line.strip().split()
        dic[content[0]] = int(content[1])
    return dic


def clean_index():
    '''
    This method is common for task for, to clean and index all the documents.
    :return:
    '''
    global index, inverted_index, number_of_terms
    cleaner = Cleaner()
    cleaner.clean_file()
    cleaner.clean_query()
    if not os.path.exists("../inverted_indexes"):
        os.makedirs("../inverted_indexes")
    index = Indexer()
    index.indexer("../inverted_indexes/corpus_inverted_index.txt", "../inverted_indexes/corpus_unigram_counts.txt",
                  "corpus")


def tf_idf_run(inverted_index, number_of_terms):
    '''
     This method will run Tf-idf base run for Task 1.
    :param inverted_index: the dictionary created for inverted indexes
    :param number_of_terms: the dictionary created for unigram count
    '''
    tf_idf = TF_IDF(inverted_index, number_of_terms)
    tf_idf.get_all_scores("queries_clean.txt", "../tf_idf", "TF_IDF")


def bm25_run(inverted_index, number_of_terms):
    '''
     This method will run bm 25 base run for Task 1.
    :param inverted_index: the dictionary created for inverted indexes
    :param number_of_terms: the dictionary created for unigram count
    '''
    global bm25
    bm25 = BM25(inverted_index, number_of_terms)
    bm25.get_all_scores("queries_clean.txt", "../bm25", "BM25")


def dirichlet_smoothing_run(inverted_index, number_of_terms):
    '''
    This method will run dirichlet smoothing base run for Task 1.
    :param inverted_index: the dictionary created for inverted indexes
    :param number_of_terms: the dictionary created for unigram count
    :return:
    '''
    global dms
    dms = DMSmoothing(inverted_index, number_of_terms)
    dms.get_all_scores("queries_clean.txt", "../dm_smoothing", "DIRICHLET")


def get_inv_count_from_file():
    '''
    This method will create dictionaries from inverted index and and unigram counts file
    :return:
    '''
    global inverted_index, number_of_terms
    inverted_index_file_name = os.path.join('../inverted_indexes/', "corpus_inverted_index.txt")
    inverted_index = read_inverted_index(inverted_index_file_name)
    unigram_count_file_name = os.path.join('../inverted_indexes/', "corpus_unigram_counts.txt")
    number_of_terms = read_number_of_terms(unigram_count_file_name)
    return inverted_index, number_of_terms


def pseudo_relevance_run(inverted_index, number_of_terms):
    '''
    This method will run all the details needed for Task 2 part(b).
    :param inverted_index: the dictionary created for inverted indexes
    :param number_of_terms: the dictionary created for unigram count
    :return:
    '''
    if not os.path.exists("../pseudo_relevance_feedback"):
        os.makedirs("../pseudo_relevance_feedback")
    pseudo_rel_file_name = os.path.join('../pseudo_relevance_feedback/', "Expanded_queries_dms_prf.txt")
    pseudo_rel_file_name_bm25 = os.path.join('../pseudo_relevance_feedback/', "Expanded_queries_bm25_prf.txt")

    pseudo_relevance = PseudoRelevance()
    pseudo_relevance.get_all_expansion_queries(pseudo_rel_file_name)
    pseudo_relevance.get_all_expansion_queries(pseudo_rel_file_name_bm25)

    dms = DMSmoothing(inverted_index, number_of_terms)
    dms.get_all_scores("/pseudo_relevance_feedback/Expanded_queries_dms_prf.txt", "../dm_smoothing_prf", "DIRICHLET")

    bms = BM25(inverted_index, number_of_terms)
    bms.get_all_scores("/pseudo_relevance_feedback/Expanded_queries_bm25_prf.txt", "../bm25_prf", "BM25")


def semantic_query_exp_run(inverted_index, number_of_terms):
    '''
    This method will runn the task 2, part (c).
    :param inverted_index: the dictionary created for inverted indexes
    :param number_of_terms: the dictionary created for unigram count
    :return:
    '''
    if not os.path.exists("../semantic_query_expansion"):
        os.makedirs("../semantic_query_expansion")
    # sqe_file_name = os.path.join('../semantic_query_expansion/', "Expanded_queries_bm25_sqe.txt")
    sqe_file_name_dms = os.path.join('../semantic_query_expansion/', "Expanded_queries_dms_sqe.txt")
    sqe = SemanticQueryExpansion()
    sqe.get_all_expansion_queries(sqe_file_name_dms, inverted_index)
    # sqe.get_all_expansion_queries(sqe_file_name,inverted_index)
    # bm25 = BM25(inverted_index, number_of_terms)
    # bm25.get_all_scores("/semantic_query_expansion/Expanded_queries_bm25_sqe.txt", "../bm_25_sqe", "BM25")
    dms = DMSmoothing(inverted_index, number_of_terms)
    dms.get_all_scores("/semantic_query_expansion/Expanded_queries_dms_sqe.txt", "../dm_smoothing_sqe", "DIRICHLET")


def stopper_run(inverted_index):
    '''
    This method will run all the details for computing task 3 part(a).
    :param inverted_index: dictionary created from the file
    :return:
    '''
    global bm25, dms
    stopper = Stopper(inverted_index)
    new_index = stopper.create_new_index()
    new_terms = stopper.create_new_term()
    bm25 = BM25(new_index, new_terms)
    bm25.get_all_scores("queries_clean.txt", "../bm25_stop", "BM25")
    dms = DMSmoothing(new_index, new_terms)
    dms.get_all_scores("queries_clean.txt", "../dm_smoothing_stop", "dms")


def cacm_stemmer_run():
    '''
    This method will run all the details for computing task 3 part(b), cacm-stem.
    :return:
    '''
    cacm_stemmer = CacmStemmer()
    cacm_stemmer.index_corpus()
    index = Indexer()
    index.indexer("../inverted_indexes_stem/corpus_inverted_index_stem.txt",
                  "../inverted_indexes_stem/corpus_unigram_counts_stem.txt", "cacm_stem_corpus")
    inverted_index = read_inverted_index("../inverted_indexes_stem/corpus_inverted_index_stem.txt")
    number_of_terms = read_number_of_terms("../inverted_indexes_stem/corpus_unigram_counts_stem.txt")
    bm25 = BM25(inverted_index, number_of_terms)
    bm25.get_all_cacm_stem_scores("cacm_stem.query.txt", "../bm25_stem", "BM25")
    dms = DMSmoothing(inverted_index, number_of_terms)
    dms.get_all_cacm_stem_scores("cacm_stem.query.txt", "../dm_smoothing_stem", "DIRICHLET")


if __name__ == '__main__':
    clean_index()

    inverted_index, number_of_terms = get_inv_count_from_file()
    # Task1
    tf_idf_run(inverted_index, number_of_terms)

    bm25_run(inverted_index, number_of_terms)

    dirichlet_smoothing_run(inverted_index, number_of_terms)

    # Task 2
    pseudo_relevance_run(inverted_index, number_of_terms)

    semantic_query_exp_run(inverted_index, number_of_terms)

    # Task 3
    stopper_run(inverted_index)

    cacm_stemmer_run()
