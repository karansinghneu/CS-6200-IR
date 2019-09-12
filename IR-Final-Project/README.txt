SETUP
1.Install Python(latest Version) in your system.
2. To run my code please run "pip install requirements.txt" to import all the libraries needed for this project.
or
3. Please check requirements.txt for dependencies needed to run the project.


To run and compile Tasks:
Phase1 - Package:
1. To run Task 1, Task 2 and Task 3 of phase 1, run __init.py__ in Phase 1 package.
We clearly mentioned which methods corresponds to task 1 and task 2 and task 3.
Please remember: Lucene java files is also in Phase 1 folder.
Phase2 - Package:
2. To run phase-2 run __init.py__ in phase 2 package.
Phase 3 - Package:
3. To run phase 3, run __init.py__ in phase 3 package.
4. To run Extra Credit, please run extracredit.py file in Extra Credit package.

Citations:
1) BeautifulSoup
2) nltk
3) Pretty Table
4) itertools

DOCUMENTS:
All the files have top 100 ranked documents as mentioned in the project description.
Phase 1:

Input_folder:
1. test-collection Folder: provided as base for this assignment.
2. cacm_stem_query.txt : has the stemmed queries provided.

OutFiles:
1. corpus: this has all the files after cleaning.
2. bm25 : Base run: this folder has output scores for each queries with files starting with query id.
3. dm_smoothing: Base run: this folder has output scores for each queries with files starting with query id.
4. tf_idf: Base run: this folder has output scores for each queries with files starting with query id.
5. bm_25_prf: Pseudo Relevance: This folder has ranked documents for each query for bm 25.
6. dm_smoothing_prf: Pseudo Relevance: This folder has ranked documents for each query for Dirichlet Smoothing.
7. bm25_sqe: Semantic Query Expansion using Thesaurus/:  This folder has ranked documents for each query for bm 25.
8. dm_smoothing_sqe:  Semantic Query Expansion using Thesaurus/:  This folder has ranked documents for each query for Dirichlet Smoothing
9. bm_25_stop: The folder has all the ranked documents for each query after stopping using commons.txt for bm25 model.
10. dm_smoothing_stop: The folder has all the ranked documents for each query after stopping using commons.txt for dirichlet smoothing model.
11. cacm_stem_corpus: This has cleaned files after cleaning the cacm_stem corpus file.
12. bm25_stem: This folder has all the ranked documents of each query after performing the bm25 on stemmed corpus with given 7 stemmed queries.
13. dm_smoothing_stem: This folder has all the ranked documents of each query after performing the bm25 on stemmed corpus with given 7 stemmed queries.
14. Lucene_base: This folder has the document ranks for each query after performing lucene base model.
15. Pseudo Relevance Feedback: This folder has the files with expanded queries on bm25 and dirichlet smoothing
16. Semantic Query Expansion: This folder has the files with expanded queries on bm25 and dirichlet smoothing.
17. Task_3_Query_Analysis.txt: Has the query by query anlaysis for 4 runs(2 base line and 2 variations(Stemmed)).
(This can also be found in report).


File names format:

Phase 2:
Input:
1. test-collection Folder: provided as base for this assignment.
2. cacm_stem_query.txt : has the stemmed queries provided.

Out_files:
1. queries_clean.txt - this file has cleaned queries.

Out_Folders:
1. bm25_snippets: This folder has each query related documents names and the snippet generated for that
corresponding document with highlighted words og BM25 run.


Phase 3:
Input:
1. test-collection Folder: provided as base for this assignment.
2. cacm_stem_query.txt : has the stemmed queries provided.

Out_files:
1. queries_clean.txt - this file has cleaned queries.
Out Folders:
1. Evaluation: This folder has folders in it with base run name as the folder name
2. Sub Folders in Evaluation: Each folder, has 2 pretty tables,
    a. one with precision and recall values of each document
    b. One with query id, precison @5 and precision @10.
    Details of Prcision recall tables on all runs:
    1. BM_25_BASE: Base run on BM25.
    2. D_SMOOTH_BASE: Base run Dirichlet Smoothing
    3. TF_IDF_BASE: Base run on TF_IDF Base model
    4. LUCENE_BASE: Base run on Lucene Base Model
    5. BM25_PRF: Run on Pseudo Relevance Model - BM25 model.
    6. D_SMOOTH_PRF: Run on Pseudo Relevance Model - Dirichlet Smoothing model
    7. BM25_SQE: Run on Semantic Query Expansion Model - BM25
    8. D_SMOOTHING_SQE: Run on Semantic Query Expansion Model - Dirichlet Smoothing model
    9. BM25_STOP: Run Stopping on BM25
    10. D_SMOOTHING_STOP: Run stopping on Dirichlet Smoothing
    11. TF_IDF_STOP_PRF: Run Model which combines Stopping and Pseudo Relavance Feedback.
    12. BM25_STOP_SQE: Run on model which combines Stopping and Semantic Query Expansion.
3. tf_idf_stop_expand: This folder has the document rankings of each document when stopping and pseudo relevance
feedback is performed on each query and evaluation for this also can be found in Evaluations with STOP AND EXPAND
appended to the folder name alongside tf-idf.
4. bm_25_stop_sqe: This folder has the document rankings of each document when stopping and semantic query expansion
is performed on each query and evaluation for this also can be found in Evaluations with STOP AND SQE
appended to the folder name alongside tf-idf.


EXTRA CREDIT:
output files:
For the first time please run commented code, to generate text_content.py

Input :
Input query in the console.

OutPut:
You get Did you mean?
And results in the next lines( upto maximum of 6)

Naming of Files:
Number in the beginning indicates of the file names indicates the query id and post the number the type of model name
run is added to suffix.
Ex: 1 BM25: it means query id is 1, and run is BM25.


Other:
Queries.txt is where you add input queries for task 1 and task2.
inverted_indexes: This has the inverted index file for normal corpus and total numbers of terms for each file.
inverted_indexes_stem: This has the inverted index file of the stemmed corpus and total numbers of terms in each file.

