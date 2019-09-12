IR 6200 HW2 Web Crawler- Link Analysis

Setup(MAC env recommended)-

Additional libraries used:
BeautifulSoup
Requests
nltk
matplotlib
lxml
os
re
collections
opt parse
string

To download any library just execute the command : pip install "Library name"

OR

You can run pip install requirements.txt , to install all the dependencies 

1. Unzip file
2. Install python 
3. Go to Project settings and add the libraries above in Project Interpreter:

Task 1 :

1. Navigate to the directory where you unzip the file
2. To run task1 - python task1.py lower
For generating text files after only case folding.
3. python task1.py remove
For generating text files after only removing punctuations.
4. python task1.py
For generating text files after case folding and removing punctuations.

Deliverables
Check the directory "html_data" for raw html files.
Check the directory "html_only_content" for clean html files.
check the file "tri_grams.txt" for tri-grams with their frequencies
Check the file "image.png" for log-log plot
Check the file "1-g.txt" for response on Task 1-g  


Task 2 :

1. To run task2 - python task2.py

Deliverables
The file G1.txt contains the crawled in links for BFS.txt as per the format provided.
The file G2.txt contains the crawled in links for FOCUSED.txt as per the format provided.
The file "g1_Stats_d0.85" for simple statistics on g1.txt 
The file "g2_Stats_d0.85" for simple statistics on g2.txt 


Task 3 :
1. To run task3 - python task3.py
Then enter the filename, for G1 enter "g1.txt"
for G2 enter "g2.txt"

Deliverables
The file "g1_L2-norm_pagerank_d0.85.txt" for Listing of L2-norm values for g1.txt
The file "g2_L2-norm_pagerank_d0.85.txt" for Listing of L2-norm values for g2.txt

The file "g1_SortedPageRank_URL_d0.85" for steady state value of PageRank for all the url's for g1.txt
The file "g2_SortedPageRank_URL_d0.85" for steady state value of PageRank for all the url's for g2.txt

The file "g1_SortedPageRank_docID_d0.85" the top 50 pages by their doc id and score for g1.txt.
The file "g2_SortedPageRank_docID_d0.85" the top 50 pages by their doc id and score for g2.txt.


Task 4:
Deliverables

The file "g1_Sorted_Inlink_d0.85" for sorted documents based on their raw in link count for g1.txt
The file "g2_Sorted_Inlink_d0.85" for sorted documents based on their raw in link count for g2.txt 
I have commented the damping values for 4.a.1 in the code for task3.py
The analysis of task 4 can be found in Task4_Analysis.txt


In the code i have taken a damping factor which is nothing but 1-lambda and thus if the filename says 0.85 it is actually a lambda of 0.15.


Deliverable for Task 3-c (Ungraded)
"sample.txt" the graph given in the task.
"sample_Stats_d0.85" stats for sample graph
"sample_SortedPageRank_URL_d0.85" for sample graph
"sample_SortedPageRank_docID_d0.85" for sample graph
"sample_L2-norm_pagerank_d0.85" for sample graph
"sample_Sorted_Inlink_d0.85" for sample graph
