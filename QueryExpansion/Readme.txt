Download and setup Lucene - (https://lucene.apache.org/)
The version used in this Assignment is Lucene 4.7.2.

Once you download Lucene, the setup is pretty straightforward. You need to create a new Java project and add the following three jars into your project’s list of referenced libraries:
1) lucene-core-VERSION.jar
2) lucene-queryparser-VERSION.jar
3) lucene-analyzers-common-VERSION.jar.

Where VERSION is to be substituted with the version of Lucene that you downloaded. For example, in the provided example, we have version 4.7.2, therefore, the first jar file would be lucene-core-4.7.2.jar. Make sure that the system requirements for that version are met.

TASK 1:
1. You will have to create a file with the queries in the following format:

1 Robotic space missions
2 Mars exploration
3 unmanned spacecraft
4 Planetary moons
5 Satellites in Space

Followed by this you have to enter the file name in the code at line number : 96 of the file Lucene.java

After running the file Lucene.java, the terminal will ask you to enter:
 
 Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\temp\index):
 Enter the full path (for eg. /Users/rksingh/Desktop/Information_Retrieval/HW4) and press enter. After that the terminal will ask you to enter :

 Enter the FULL path of the corpus (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
[Acceptable file types: .xml, .html, .html, .txt]:
Enter the full path (for eg. /Users/rksingh/Desktop/Information_Retrieval/HW4/corpus) and press enter.

 A file is generated with the top 100 ranked documents for each and every query with the name "Ranked_doc_List_Lucene.txt"

The top 100 results for each of the 5 queries from task 1b). is in the file called "Ranked_doc_List_Lucene.txt"

TASK 2:
For task 2, the following libraries have been used in Python

from collections import defaultdict
import os
from collections import OrderedDict

import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

Enter the command : python task2.py in the terminal to execute the task 2.
The stop words have been removed using the stopwords list provided by nltk and the code takes care of it.

Task 2.b similar to that of 1 by creating a file with the queries.

The term and their term frequencies for k=10 and query 1 is in the file:
unigramtfTable_query_1.txt
The term and their term frequencies for k=10 and query 2 is in the file:
unigramtfTable_query_2.txt
The term and their term frequencies for k=10 and query 3 is in the file:
unigramtfTable_query_3.txt
The term and their term frequencies for k=10 and query 4 is in the file:
unigramtfTable_query_4.txt
The term and their term frequencies for k=10 and query 5 is in the file:
unigramtfTable_query_5.txt

The term and their term frequencies for k=5 and query 1 is in the file:
unigramtfTable_query_1_k_5.txt
The term and their term frequencies for k=5 and query 2 is in the file:
unigramtfTable_query_2_k_5.txt
The term and their term frequencies for k=5 and query 3 is in the file:
unigramtfTable_query_3_k_5.txt
The term and their term frequencies for k=5 and query 4 is in the file:
unigramtfTable_query_4_k_5.txt
The term and their term frequencies for k=5 and query 5 is in the file:
unigramtfTable_query_5_k_5.txt

The list of expansion terms identified for each of 5 queries along with the values used for k and n, in a single text file called "Deliverable_4.txt"

The top 100 results for each of the 5 queries from task 2b), after incorporating query
expansion:
For k=10 and n=8
"Ranked_doc_List_Lucene_Expansion_n_8.txt"
For k=10 and n=7
"Ranked_doc_List_Lucene_Expansion_n_7.txt"
For k=10 and n=6
"Ranked_doc_List_Lucene_Expansion_n_6.txt"
For k=5 and n=8
"Ranked_doc_List_Lucene_Expansion_k_5_n_8.txt"
For k=5 and n=7
"Ranked_doc_List_Lucene_Expansion_k_5_n_7.txt"
For k=5 and n=6
"Ranked_doc_List_Lucene_Expansion_k_5_n_6.txt"

Task 3:

Analysis of the results from Task 3 in the file called "Task3.txt"
