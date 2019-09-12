import os
import re
from collections import Counter

import nltk
from nltk import ngrams
import matplotlib.pyplot as plot
nltk.download('punkt')
import requests
import optparse
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from string import punctuation


#Function for getting the URL's from the text file
def getLinks():
    file = open("BFS.txt", "r")
    crawled_url_list = file.read().splitlines()
    print(crawled_url_list)
    for url in crawled_url_list:
        getHtml(url)

#Function to get raw html of the url's
def getHtml(url):

    htmltext = requests.get(url)
    soup = BeautifulSoup(htmltext.content, "html.parser")
    #list = text_from_html(htmltext.content)
    #print(list)
    name = url.split("/")[-1]
    subdirectory = "html_data"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    # storing the html content
    myfile = open(os.path.join(subdirectory, re.sub('/', ' ', name + ".txt")), 'w')
    myfile.write(url + '\n' + str(soup.encode('ascii')))
    # storing the html content
    myfile.close()

# def text_from_html(body):
#
#     soup = BeautifulSoup(body, 'html.parser')
#     texts = soup.findAll(text=True)
#     return u" ".join(t.strip() for t in texts).encode('utf-8')



def process_html_data (directory, arg):
    for filename in os.listdir (directory):
        new_html(filename, directory, arg)


def new_html(filename, directory, arg):
    file = open (directory + '/' + filename, 'r')
    soup = BeautifulSoup (file.read(), 'html.parser')
    file.close ()
    text_html = get_html_text(soup, arg)
    write_to_file (filename, text_html)

#Function to get clean text
def get_html_text(soup, arg):
    clean_html = remove_tags(soup, arg)
    return clean_html

#Function to remove the html tags
def remove_tags(soup, arg):
    nav_bar = soup.find ('div', class_='mw-jump')
    page_footer = soup.find ('div', class_='printfooter')
    page_site = soup.find ('div', id='siteSub')
    if nav_bar:
        soup.find ('div', class_='mw-jump').decompose()

    if page_footer:
        soup.find ('div', class_='printfooter').decompose()

    if page_site:
        soup.find ('div', id='siteSub').decompose()
    html_cleaner = remove_parameters()
    page_title = soup.find ('title')
    page_body = soup.find ('div', {'id': 'bodyContent'})
    soup_extract = html_cleaner.clean_html(str (page_title) + " " + str (page_body))
    clean_content = content_cleaner(soup_extract, arg)
    return clean_content

#Function for cleaning the html file
def content_cleaner(soup_extract, arg):
    clean_content = BeautifulSoup(soup_extract, 'lxml').get_text()
    clean_content = ' '.join(clean_content.split())
    clean_content = clean_content.replace('html ', '')
    clean_content = ''.join(content for content in clean_content if 0 < ord(content) < 127)
    if arg == "lower":
        clean_content = to_lower(clean_content)
    elif arg == "remove":
        clean_content = punctuation_remover(clean_content)
    # apply both for default where there is no choice
    else:
        clean_content = to_lower(clean_content)
        clean_content = punctuation_remover(clean_content)
    return clean_content

#Function for case folding
def to_lower (clean_content):
    clean_content = clean_content.lower()
    return clean_content

#Function to remove punctuations
def punctuation_remover(clean_content):
    clean_content = ''.join (characters for characters in clean_content if characters not in '}{][)(\><=')
    clean_content = ' '.join (
        token.strip (punctuation) for token in clean_content.split() if token.strip (punctuation))
    clean_content = ' '.join (token.replace ("'", "") for token in clean_content.split() if token.replace("'", ""))
    clean_content = ' '.join (clean_content.split())
    return clean_content

#Function to remove parameters and clean the HTML file
def remove_parameters ():
    reject_list = ['script', 'noscript', 'style', 'meta', 'semantics', 'img', 'label', 'table', 'li', 'ul',
                   'ol', 'nav', 'dl', 'dd', 'sub', 'sup', 'math']
    accept_list = ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'span', 'b', 'a', 'u', 'i', 'body']
    html_cleaner = Cleaner()
    html_cleaner.remove_unknown_tags = True
    html_cleaner.processing_instructions = True
    html_cleaner.style = True
    html_cleaner.comments = True
    html_cleaner.scripts = True
    html_cleaner.javascript = True
    html_cleaner.meta = True
    html_cleaner.links = True
    html_cleaner.embedded = True
    html_cleaner.annoying_tags = True
    html_cleaner.frames = True
    html_cleaner.forms = True
    html_cleaner.remove_tags = accept_list
    html_cleaner.kill_tags = reject_list
    return html_cleaner

#Function to write content to a file
def write_to_file(filename, text_html):
    subdirectory = "html_only_content"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass
    # storing the html content
    myfile = open(os.path.join(subdirectory, re.sub('/', ' ', filename)), 'w')
    myfile.write(str(text_html))
    # storing the html content
    myfile.close()

#Function to take the command line arguments for removing punctuation or lower case
#With no Arguments it does both
def command_Line_Arguments():
    parser_for_input = optparse.OptionParser()
    args = parser_for_input.parse_args()
    return args

#Function to generate the tri grams and write them to a file
def generate_tri_grams(directory):
    trigrams = Counter()
    for file in os.listdir(directory):
        file = open(directory + '/' + file, 'r')
        file_data = file.read()
        token = nltk.word_tokenize(file_data)
        trigrams = trigrams + Counter(ngrams(token, 3))
    generateGraph(Counter(trigrams))

#Function to generate the frequency vs rank  log-log graph for zipf's law
def generateGraph(out):
   n = 0
   list1 = []
   list2 = []
   temp = out.most_common()
   for key,value in temp:
       n +=  1
       rank = n
       list1.append(value)
       list2.append(rank)
   plot.loglog(list2,list1)
   plot.grid(True)
   plot.savefig("image.png")
   #plot.show()
   with open('tri_grams.txt', 'w') as file:
       for k, v in temp:
           file.write("{} {}\n".format(k, v))


def main():

    getLinks()
    args = command_Line_Arguments()
    arg = args[1]
    process_html_data("html_data", arg)
    generate_tri_grams("html_only_content")

if __name__ == '__main__':
    main()