from math import log
from collections import defaultdict
import os
from collections import ChainMap
from collections import OrderedDict

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0

def main():
    text_files = [f for f in os.listdir('corpus') if f.endswith('.txt')]
    text_files.reverse()
    words = defaultdict(list)
    name_count = defaultdict(list)

    words, name_count = unigram(text_files)

    with open('queries.txt', 'r', encoding="utf-8", errors="surrogateescape") as f:
        lines = ''.join(f.readlines())

    queries = read_query(lines)
    file_count = 1
    results = []
    for query in queries:
        results = []
        results.append(exec_query(words, query, name_count))
       # print(results)
        score = {}
        score = dict(ChainMap(*results))
        sorted_score = OrderedDict(sorted(score.items(), key=lambda x: x[1], reverse=True)[:100])
        counter = 1
        f = open(str(file_count) + "_BM25.txt",'a', encoding="utf-8", errors="surrogateescape")
        f.write("query_id Q0 doc_id rank BM25_score system_name" + '\n')
        for k, v in sorted_score.items():
            #print(str(int(queries.index(query))+1) + " " + "Q0" + " " + str(k) + " " + str(counter) + " " + str(v) + " " + "UniBM25")
            f.write(str(int(queries.index(query))+1) + " " + "Q0" + " " + str(k) + " "
                    + str(counter) + " " + str(v) + " " + "UniBM25" + '\n')
            counter = counter + 1
        f.flush()
        f.close()
        file_count = file_count + 1


def unigram(text_files):
    words = []
    dict_words = defaultdict(list)
    dict_count = defaultdict(list)
    for i in text_files:            #opens and reads the contents of a single file and enters the key:value information
                                    #in the dict_words, does so for the entire corpus passed.
        with open("corpus/" + i, 'r', encoding="utf-8", errors="surrogateescape") as f:
            val = f.readlines()
        #print(f.name)
        text = ''.join(val)
        words.append(text.lower().split(" ")) #cross checking whether all terms lower yet again
        #print(words)
        flat_words = combined_list(words)
        while '' in flat_words:
            flat_words.remove('')
        #print(flat_words)
        dict_count[os.path.splitext(f.name)[0].replace('corpus/', '')] = len(flat_words)
        #print(dict_count)
        for entry in flat_words: #check if the docid, count pair already present for the key
            if [os.path.splitext(os.path.basename(f.name))[0], flat_words.count(entry)] in dict_words[entry]:
                continue
            else:               #else append to the values
                dict_words[entry].append([os.path.splitext(os.path.basename(f.name))[0], flat_words.count(entry)])
        words.clear()  #clearing the word_list for the next iteration with a new file
    #print(dict_words)
    return dict_words, dict_count


def read_query(lines):
    query_list = []

    for line in lines.split('\n'):
        query = line.rstrip().split()
        query_list.append(query)

    return query_list


def calculate_BM25(n, f, qf, r, N, dl, avdl):
    K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
    fir = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    s = ((k1 + 1) * f) / (K + f)
    t = ((k2 + 1) * qf) / (k2 + qf)
    return fir * s * t


def exec_query(words,query,name_count):
    query_result = dict()
    qf = 1
    r = 0
    N = 1000
    for term in query:
        if term in words: #whether the term is in inverted index
            value = words[term] #if yes, then all the documents the term occurs in
            for single_val, freq in value: #for single document of all the documents
                if single_val in name_count: #no. of words in that document
                    n = len(value)  #no. of documents indexed by this term
                    f = freq  #frequency of that word
                    dl = name_count[single_val]  #no. of words in the document
                    avdl = sum(name_count.values()) / N  #sum of all dl's / no. of documents
                    score = calculate_BM25(n, f, qf, r, N, dl, avdl)
                    if term in query_result:
                        query_result[single_val] += score
                    else:
                        query_result[single_val] = score
    return query_result


def combined_list(list1):
    flat_list = []
    for sublist in list1:
        for item in sublist:
            flat_list.append(item)

        return flat_list

if __name__ == "__main__":
    main()
