import re
from bs4 import BeautifulSoup
import os

class SnippetGeneration:

    def removePunctuations(self, cleaned_data):
        """
        Method to remove punctuations except, hyphens.
        :param cleaned_data: the to be cleaned data
        :return: free of ounctuations data.
        """
        cleaned_data = ''.join(chars for chars in cleaned_data if chars not in '}{][)(\><=')
        pattern = re.compile('[^a-zA-Z0-9-]')
        cleaned_data = re.sub(pattern, ' ', cleaned_data)
        cleaned_data = ' '.join(cleaned_data.split())
        return cleaned_data


    def remove_redundant_corpus(self, cleaned_data):
        # Removing redundant spaces.
        cleaned_data = ' '.join(cleaned_data.split())
        clean = []
        lis = cleaned_data.split()
        check = False
        for i in range(len(lis) - 1, -1, -1):
            if 'AM' in lis[i] or 'PM' in lis[i] or 'am' in lis[i] or 'pm' in lis[i] or check == True:
                clean.append(lis[i])
                check = True
            else:
                continue
        clean.reverse()
        strr = ' '.join(clean)
        return strr


    def filterPageData(self,content, toLower, toNoPunct):
        """
        Method to remove trailing spaces, punctuations, special characters etcs.,
        :param cleaned_data:
        :param toLower:
        :param toNoPunct:
        :return:
        """
        cleaned_data = self.remove_redundant_corpus(content)
        # Removing punctuations.
        if (toNoPunct):
            cleaned_data = self.removePunctuations(cleaned_data)
        if toLower:
            # Making all text to lower.
            cleaned_data = cleaned_data.lower()
        # Removing this as this is not required anytime.
        # else:
        #     cleaned_data = self.removePunctuations(cleaned_data)
        #     # Making all text to lower.
        #     cleaned_data = cleaned_data.lower()
        return cleaned_data


    def get_file_content(self, doc_id, query):
        '''
        THis method will get the file content after the punctuations and case folding is performed.
        :param doc_id: the id of the document
        :param query: the query
        :return:cleaned content.
        '''
        with open("../test-collection/htmls/" + doc_id + '.html', encoding='utf8') as file_data:
            file_content = file_data.read()
            html_content = BeautifulSoup(file_content, "html.parser")
            body_content = html_content.find('pre')
            content = body_content.getText()
            url = re.sub('\s+', ' ', doc_id).strip()
            cleaned_data = self.filterPageData(content, False, False)
            return cleaned_data


    def is_significant_word(self,word, sd, word_freq):
        '''
        This method will check if the given word is significant or not.
        :param word: thw word on which significance is checked.
        :param sd: number of sentences in the document
        :param word_freq: number of times the words occurred.
        :return: 
        '''
        if sd < 25 and word_freq[word] >= 4 - 0.1 * (25 - sd):
            return True
        elif 25 <= sd <= 40 and word_freq[word] >= 4:
            return True
        return word_freq[word] >= 4 + 0.1 * (sd - 40)


    def get_significance_factor(self,sentence, word_freq, sd, query):
        '''
        This method will get each sentence and split each word, check if it is significant or not and add it to a list.
        This also will also add the query words and remove stop words for clacullation the significant factor.
        :param sentence: the sentence for which we are comouting th esignificant factor.
        :param word_freq: the frequency of each word.
        :param sd: number of sentences in the document.
        :param query: the query on which this operation is being performed.
        :return: 
        '''
        sentence = sentence.lower()
        sentence_split = sentence.split()
        significant_words = set()

        stop_words = []
        f = open('../test-collection/common_words')
        for l in f:
            stop_words.append(l.strip())

        for q in query.split():
            if q not in stop_words:
                significant_words.add(q)

        for word in sentence_split:
            if self.is_significant_word(word, sd, word_freq) and word not in stop_words:
                significant_words.add(word)

        start, end = -1, 0
        flag = False
        for w in range(len(sentence_split)):
            if sentence_split[w] in significant_words:
                if not flag:
                    start = w
                    flag = True
                end = w
        if start == -1 and end == 0:
            return 0, 0, 0
        sig_trimmed = sentence_split[start:end + 1]
        if len(sig_trimmed) == 0:
            return 0, 0, 0
        num_sig_words = 0

        if end - start > 15:
            end = start + 15
        for w in sig_trimmed:
            if w in significant_words:
                num_sig_words += 1
        return num_sig_words ** 2 / len(sig_trimmed), start, end


    def generate_snippet(self,sentences, q):
        '''
        This method will generate snippets based on the computed significant factors.
        :param sentences: the list of sentences from the document./
        :param q: the query.
        :return: 
        '''
        sentence_sigfactor = {}
        word_freq = {}
        tot_words = 0
        sd = len(sentences)
        for sentence in sentences:
            for w in sentence.split():
                tot_words += 1
                processed_w = w.lower()
                if processed_w not in word_freq:
                    word_freq[processed_w] = 0
                word_freq[processed_w] += 1

        for sentence in sentences:
            sentence_split = sentence.split()
            sig_factor, start, end = self.get_significance_factor(sentence, word_freq, sd, q)
            if start < end:
                sentence_sigfactor[' '.join(sentence_split[start:end + 1])] = sig_factor
        sigs = sorted(sentence_sigfactor.items(), key=lambda x: x[1], reverse=True)
        res = []
        if len(sigs) < 3:
            for i in range(len(sigs)):
                res.append(sigs[i][0])
        else:
            for i in range(3):
                res.append(sigs[i][0])
        return res

    def generate_and_highlight_snippets(self,queries_dict, files):
        '''
        This method will generate and highlight and snippets and write them to a file/.
        :param queries_dict: The inout queries are sent as dictionary.
        :param files: the files.
        :return:
        '''
        snipptes_dict = {}
        for file in files:
            f = open("../bm25/" + file, 'r', encoding="utf8")
            results = ""
            for line in f:

                result_str = ""
                query_id = line.split()[0]
                query = queries_dict[query_id]
                doc_id = line.split()[2]
                print("\nFor file", doc_id)
                file_content = self.get_file_content(doc_id, query)
                sentences = re.split(r"\.[\s\n]+", file_content)
                snippets = self.generate_snippet(sentences, query)
                highlighted_snippets = []
                query_terms = query.split()
                for s in snippets:
                    highlighted_snippets.append(self.snippet_highlight(s, query_terms) + ' ...\n')
                snipptes_dict[doc_id] = ' '.join(highlighted_snippets)
                result_str = result_str + (''.join(highlighted_snippets))
                results = results + (doc_id+"\n"+result_str+"\n")
            self.write_to_file(file, "../bm25_snippets", results)


    def snippet_highlight(self,snippet, query_terms):
        '''
        This method will highglight the snippet where ever the respective query words are found.
        :param snippet: the snippet generated from the above technique.
        :param query_terms: the terms in the query.
        :return: returns the resultant snippet.
        '''
        highlight_terms = []
        for s in snippet.split():
            if s.lower() in query_terms:
                highlight_terms.append('<b>' + s + '</b>')
            else:
                highlight_terms.append(s)
        res = (' '.join(highlight_terms))
        res = res.replace("</b> <b>", " ")
        return res

    def write_to_file(self, file, folder, result_str):
        """
        This method is to write into the document and scores into file in the required format
        :param sorted_term_freq: the documment and score to be written into the file.
        :param queryId: the Id of the query.
        :return: None
        """
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder + "/" + file)
        with open(filename, 'w', encoding="utf-8") as file_data:
            file_data.write(result_str)
        file_data.close()




