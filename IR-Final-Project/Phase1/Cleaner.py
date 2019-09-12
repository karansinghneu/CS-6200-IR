from bs4 import BeautifulSoup
import re
import os
from collections import OrderedDict


class Cleaner():

    def clean_file_stem(self):
        '''
        This method will clean the file given, to generate a cacm-stem corpus, which each file name as the doc id and
        CACM- prepended to it..
        :return:
        '''
        count = 0
        with open("../test-collection/cacm_stem.txt", encoding='utf8') as f:
           new_file = ""
           for line in f:
                if "#" in line:
                    temp = new_file
                    new_file = ""
                    if temp != "":
                        cleaned_data = self.filterPageData(temp, True, True, True)
                        self.write_text_to_file(cleaned_data,  "CACM-"+str(count), True)
                    count = count + 1
                else:
                    new_file += line

    def clean_query(self):
        '''
        This method will clean the query
        :return:
        '''
        queries = {}
        with open("../test-collection/cacm.query.txt", encoding='utf8') as file_data:
            file_content = file_data.read()
            html_content = BeautifulSoup(file_content, "html.parser")
            body_content = html_content.findAll('doc')
            body_content.reverse()
            while len(body_content) > 0:
                content = body_content.pop()
                htmlcon = content
                key = int(htmlcon.find("docno").getText())
                htmlcon.find("docno").decompose()
                con = htmlcon.getText()
                cleaned_data = self.filterPageData(con, True, True, False)
                queries[key] = cleaned_data
            sorted_queries = OrderedDict((k, v) for k, v in sorted(queries.items()))
            self.write_querie_to_file(sorted_queries)
        return sorted_queries

    def write_querie_to_file(self, queries):
        '''
        This method will write all the queries to file.
        :param queries: the dictionary with key as query id and value as query.
        :return:
        '''
        with open("../queries_clean.txt", 'w', encoding="utf-8") as file_data:
            for key, value in queries.items():
                file_data.write(str(key) + " " + value + "\n")
        file_data.close()

    def clean_file(self):
        '''
        This method will clean the htmls and make the them text and remove punctation.
        :return:
        '''
        text_files = os.listdir("../test-collection/htmls/")
        for doc_id in text_files:
            with open("../test-collection/htmls/" + doc_id, encoding='utf8') as file_data:
                file_content = file_data.read()
                html_content = BeautifulSoup(file_content, "html.parser")
                body_content = html_content.find('pre')
                content = body_content.getText()
                # Getting only the text inside the body
                url = re.sub('\s+', ' ', doc_id).strip()
                cleaned_data = self.filterPageData(content, True, True, True)
                self.write_text_to_file(cleaned_data,url, False)

    def remove_redundant_corpus(self, cleaned_data):
        '''
        This method will remove the redundant spaces.
        :param cleaned_data: the cleaned text.
        :return: cleaned text of the document.
        '''
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

    def remove_redundant_query(self, cleaned_data):
        '''
        This method will rmeove the redundant spances in the text after parsing the html.
        :param cleaned_data:
        :return:
        '''
        # Removing redundant spaces.
        return ' '.join(cleaned_data.split())

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

    def filterPageData(self, content, toLower, toNoPunct, isCorpus):
        """
        Method to remove trailing spaces, punctuations, special characters etcs.,
        :param cleaned_data:
        :param toLower:
        :param toNoPunct:
        :return:
        """
        if isCorpus:
            cleaned_data = self.remove_redundant_corpus(content)
        else:
            cleaned_data = self.remove_redundant_query(content)
        # Removing punctuations.
        if (toNoPunct):
            cleaned_data = self.removePunctuations(cleaned_data)
        if toLower:
            # Making all text to lower.
            cleaned_data = cleaned_data.lower()
        else:
            cleaned_data = self.removePunctuations(cleaned_data)
            # Making all text to lower.
            cleaned_data = cleaned_data.lower()
        return cleaned_data

    def write_text_to_file(self, html_cleaned, str_url, check):
        """
        Writing the text to file.
        :param html_cleaned: as the cleaned data.
        :param str_url: the docId
        :param title: title of the page
        :return:
        """
        if check is True:
            if not os.path.exists("../cacm_stem_corpus"):
                os.makedirs("../cacm_stem_corpus")
            filename = os.path.join('../cacm_stem_corpus/', str(str_url) + '.txt')
        else:
            if not os.path.exists("../corpus"):
                os.makedirs("../corpus")
            str_url = str_url[:-5]
            filename = os.path.join('../corpus', str(str_url) + '.txt')
        with open(filename, 'w', encoding="utf-8") as file_data:
            file_data.write(html_cleaned)
        file_data.close()
