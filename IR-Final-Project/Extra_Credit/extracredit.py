import os
import re
from collections import Counter
import itertools


def words(text):
    return re.findall(r'\w+', text.lower())


WORDS = Counter(words(open('text_content.txt').read()))


def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N


def correction(word):
    "Most probable spelling correction for word."
    res = []
    wrd_set = candidates(word)
    for i in range(len(wrd_set)):
        max_item = max(wrd_set, key=P)
        res.append(max_item)
        wrd_set.remove(max_item)
    return res


def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def prob_score(query):
    res = 0
    for w in query:
        res += P(w)
    return res


# given_query = "modeing nd simlation ina agrriculltural ecoesystems"
#Example: "portabl operati sytem cajm"
given_query = input('Enter the query. Example: portabl operati sytem cajm\n')

query = given_query.lower()
corrected_queries = set()
query_dic = {}
for q in query.split():
    query_dic[q] = correction(q)
p = []
for k, v in query_dic.items():
    p.append(v)
res_lst_lst = list(itertools.product(*p))
res_lst = []
for rll in res_lst_lst:
    res_lst.append(" ".join(rll))
topk = {}

for q in res_lst:
    topk[q] = prob_score(q)

sqrs = sorted(topk.items(), key=lambda x: x[1], reverse=True)
suggested_queries = []
if len(sqrs) < 6:
    for i in range(len(sqrs)):
        suggested_queries.append(sqrs[i][0])
else:
    for i in range(6):
        suggested_queries.append(sqrs[i][0])

if len(suggested_queries) == 1 and query == suggested_queries[0]:
    print(query)
    print("Query is right")
else:
    print('Did you mean?')
    for s in suggested_queries:
        print(s)
