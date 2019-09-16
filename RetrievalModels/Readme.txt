Download and setup Lucene - (https://lucene.apache.org/)
The version used in this Assignment is Lucene 4.7.2.

Once you download Lucene, the setup is pretty straightforward. You need to create a new Java project and add the following three jars into your project’s list of referenced libraries:
1) lucene-core-VERSION.jar
2) lucene-queryparser-VERSION.jar
3) lucene-analyzers-common-VERSION.jar.

Where VERSION is to be substituted with the version of Lucene that you downloaded. For example, in the provided example, we have version 4.7.2, therefore, the first jar file would be lucene-core-4.7.2.jar. Make sure that the system requirements for that version are met.


The deliverables are in the following files:

--> Your source code for both tasks (both indexing and retrieval modules for Task 2).
Task1.py and Lucene.java

--> 10 tables (one per query x two IR systems) each containing at MOST 100 docIDs ranked by score.
query 1 --> "1_Lucene.txt"
query 2 --> "2_Lucene.txt"
query 3 --> "3_Lucene.txt"
query 4 --> "4_Lucene.txt"
query 5 --> "5_Lucene.txt"
query 1 --> "1_BM25.txt"
query 2 --> "2_BM25.txt"
query 3 --> "3_BM25.txt"
query 4 --> "4_BM25.txt"
query 5 --> "5_BM25.txt"

--> A very short report describing your implementation.
"Implementation.txt"

-->A brief discussion comparing the top 5 results between the two search engines for each query.
"Comparison_Lucene_BM25.txt"


TASK 1:
For task 1, the following libraries have been used in Python

from math import log
from collections import defaultdict
import os
from collections import ChainMap
from collections import OrderedDict

Enter the command : python Task1.py in the terminal to execute the task 1.
The BM25 has been performed using the following values given in the assignment:
k1 = 1.2
k2 = 100
b = 0.75

1. You will have to create a file with the queries in the following format:

1 milky way galaxy
2 hubble space telescope
3 international space station
4 big bang theory
5 mars exploratory missions

Followed by this you have to enter the file name in the code at line number : 20 of the file Task1.py

The top 100 ranked documents gets stored in the following files for respective queries:
query 1 --> "1_BM25.txt"
query 2 --> "2_BM25.txt"
query 3 --> "3_BM25.txt"
query 4 --> "4_BM25.txt"
query 5 --> "5_BM25.txt"


TASK 2:
1. You will have to create a file with the queries in the following format:

1 milky way galaxy
2 hubble space telescope
3 international space station
4 big bang theory
5 mars exploratory missions

Followed by this you have to enter the file name in the code at line number : 96 of the file Lucene.java

After running the file Lucene.java, the terminal will ask you to enter:
 
 Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\temp\index):
 Enter the full path (for eg. /Users/rksingh/Desktop/Information_Retrieval/HW4) and press enter. After that the terminal will ask you to enter :

 Enter the FULL path of the corpus (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
[Acceptable file types: .xml, .html, .html, .txt]:
Enter the full path (for eg. /Users/rksingh/Desktop/Information_Retrieval/HW4/corpus) and press enter.

 A file is generated with the top 100 ranked documents for each and every query with the name "Ranked_doc_List_Lucene.txt"

The top 100 results for each of the 5 queries for Lucene are present in the following files:
query 1 --> "1_Lucene.txt"
query 2 --> "2_Lucene.txt"
query 3 --> "3_Lucene.txt"
query 4 --> "4_Lucene.txt"
query 5 --> "5_Lucene.txt"

The top 100 results for each of the 5 queries for BM25 are present in the following files:
query 1 --> "1_BM25.txt"
query 2 --> "2_BM25.txt"
query 3 --> "3_BM25.txt"
query 4 --> "4_BM25.txt"
query 5 --> "5_BM25.txt"
