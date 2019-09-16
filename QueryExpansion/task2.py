from collections import defaultdict
import os
from collections import OrderedDict

import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords


def main():
    corpus = dict()
    text_files1 = [f for f in os.listdir('query_1_k_5') if f.endswith('.txt')]
    text_files1.reverse()
    unigram(text_files1,"query_1_k_5")
    text_files2 = [f for f in os.listdir('query_2_k_5') if f.endswith('.txt')]
    text_files2.reverse()
    unigram(text_files2,"query_2_k_5")
    text_files3 = [f for f in os.listdir('query_3_k_5') if f.endswith('.txt')]
    text_files3.reverse()
    unigram(text_files3,"query_3_k_5")
    text_files4 = [f for f in os.listdir('query_4_k_5') if f.endswith('.txt')]
    text_files4.reverse()
    unigram(text_files4,"query_4_k_5")
    text_files5 = [f for f in os.listdir('query_5_k_5') if f.endswith('.txt')]
    text_files5.reverse()
    unigram(text_files5,"query_5_k_5")


def unigram(text_files, directory_name):
    words = []
    dict_words = defaultdict(list)
    for i in text_files:

        with open(directory_name+"/" + i, 'r') as f:
            val = f.readlines()
        text = ''.join(val)
        words.append(text.lower().split(" "))
        flat_words = combined_list(words)
        filtered_words = [word for word in flat_words if word not in stopwords.words('english')]
        print("These are flat words:", flat_words)
        # file = open("total_words.txt", 'a', encoding="ascii", errors="surrogateescape")
        # file.write(os.path.splitext(os.path.basename(f.name))[0] + "-->" + str(len(flat_words)) + '\n')
        while '' in filtered_words:
            filtered_words.remove('')
        for entry in filtered_words:
            if [os.path.splitext(os.path.basename(f.name))[0], filtered_words.count(entry)] in dict_words[entry]:
                continue
            else:
                dict_words[entry].append([os.path.splitext(os.path.basename(f.name))[0], filtered_words.count(entry)])
        words.clear()
    table_unigram(dict_words,directory_name)
    #write_uni(dict_words)


def table_unigram(dict_words,directory_name):
    count = 0
    dict_table = {}
    dict_df = {}
    print("These are dict words", dict_words)  # term:[[doc id, tf]]
    for key, value in dict_words.items():
        count = 0
        for val in value:
            count = count + val[1]
        dict_table[key] = count

    print("This is dict_table:", dict_table)
    newDict = OrderedDict(reversed(sorted(dict_table.items(), key=lambda x: x[1])))
    print("This is new Dict:", newDict)

    file = open("unigramtfTable_"+directory_name+".txt", 'a', encoding="ascii", errors="surrogateescape")
    file.write("term -> tf" + '\n')
    for key, value in newDict.items():
        try:
            file.write(str(key) + '->' + str(value) + '\n')
        except:
            pass

    file.flush()
    file.close()

def combined_list(list1):
    flat_list = []
    for sublist in list1:
        for item in sublist:
            flat_list.append(item)

    return flat_list

if __name__ == "__main__":
    main()
