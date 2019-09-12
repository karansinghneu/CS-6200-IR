import re
import time
import sys
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from time import strftime

common_prefix = "https://en.wikipedia.org"
current_time = strftime("%Y-%m-%d-%H%M%S")
count = defaultdict(int)

'''
 dfs(seed, list) Function
 description : dfs crawling of the urls as inorder traversal
 Arguments:
    seed: The Url with depth in dict format
    list: No focussed crawling for DFS
 Output: Generate file with dfs crawled urls
'''


def dfs(seed, list):
    visited = []
    stack = [{'url': seed, 'depth': 1}]                 # add seed url in stack list alognwith its depth

    print('----------DFS Crawling started ----------')
    while len(stack)!=0 and len(visited) < 1000:      # while condition to stopped crawling
        node = stack.pop()                              # select topmost dict of stack list
        if node['url'] not in (obj['url'] for obj in visited):  # to check if url is not already visited
            visited.append(node)                        # mark node as visited by appending it to visited list
            with open('dfs_focussed' + '_' + current_time + '.txt', 'a') as myfile:  # append node in file
                myfile.write(common_prefix + node['url'] + '\n')
            if node['depth'] < 6:                     # condition to crawl only till depth : 6
                urls = findurl(node, list)           # find all url in given node (from top to bottom of the page)
                if urls is not None:
                    if len(urls) != 0:  # add crawledUrl list to stack list only if available
                        crawledUrl = urls[
                                     ::-1]  # reverse the url so first url is always on top of stack (from bottom to top of the page)
                        stack = stack + crawledUrl          # add crawled urls list to stack list
        else:
            with open('duplicates.txt', 'a') as myfile:
                count[node['url']] += 1
                for k, v in count.items():
                    myfile.write(k + "-Count:" + str(v) + "\n")
    print('----------The number of pages crawled are {}----------'.format(len(visited)))

'''
 bfs(seed, list) Function
 description : bfs crawling of the urls
 Arguments:
    seed: The Url with depth in dict format
    list: The list of keywords to filter the crawled urls
 Output: Generate file with bfs crawled urls
'''

def bfs(seed, list):
    visited = []
    queue = [{'url': seed, 'depth': 1}]                 # add seed url in stack list along with its depth

    print('----------BFS Crawling started: {}----------')
    while len(queue) != 0 and len(visited) < 1000:      # while condition to stopped crawling
        print("THIS IS THE LENGTH", len(queue), len(visited))
        node = queue.pop(0)                             # select first dict of stack list
        if node['url'] not in (obj['url'] for obj in visited):  # to check if url is not already visited
            visited.append(node)                        # mark node as visited by appending it to visited list
            with open('bfs_focussed' + '_' + current_time + '.txt', 'a') as myfile:  # append node in file
                myfile.write(common_prefix + node['url'] + '\n')
            if node['depth'] < 6:                     # condition to crawl only till depth : 6
                urls = findurl(node, list)           # find all url in given node (from top to bottom of the page)
                if len(urls) != 0:                        #add crawledUrl list to stack list only if available
                    print("This is the length",len(urls))
                    queue = queue + urls                # add crawled urls list to stack list
        elif len(list) !=0:
            with open('duplicates.txt', 'a') as myfile:
                count[node['url']] += 1
                for k, v in count.items():
                    myfile.write(k + "Repeated Count:" + str(v) + "\n")

    print('----------The number of pages crawled are {}----------'.format(len(visited)))

'''
 findurl(node, list) Function
 description : Function to crawl the node with given keywords (focussed crawling)
 Arguments:
    node: The Url with depth in dict format
    list:The list of keywords to filter the crawled urls
'''
def findurl(node, list):
    try:
        time.sleep(1)                               # be polite and use a delay of at least 1 sec
        htmltext = requests.get(common_prefix + node['url'])
        soup = BeautifulSoup(htmltext.content, "html.parser")
        output = []
        getHtml(node, soup)
        for link in soup.findAll('a', href=True):   # find all the links from seed page
            if re.search('#', link['href']):        # ignore url that contains '#' (properly treat URLs with #)
                continue
            if re.search(':', link['href']):        # ignore url that contains ':' (avoid administrative link)
                continue
            if link['href'].startswith('/Main_Page') :
                continue
            if len(list)!= 0:
                for keyword in list:
                    if link['href'].startswith('/wiki') and re.search(keyword, link['href'],
                                                                      re.IGNORECASE):  # contains 'keyword'
                        output.append({'url': link['href'], 'depth': node['depth'] + 1})  # append urls to output list
            if len(list)==0:
                if link['href'].startswith('/Main_Page'):
                    continue
                if link['href'].startswith('/wiki'):  # contains 'keyword'
                    output.append({'url': link['href'], 'depth': node['depth'] + 1})    #append urls to output list
        print("Here is the output", output)
        return output
    except IOError as err:
        print("The exception", err)
        print("No network route to the host".format(err))

def getHtml(current, soup):
    name = current['url'].split("/")[-1]
    with open(str(name) + '.txt', 'a') as myfile:  # append node in file
        myfile.write(common_prefix + current['url'] + '\n' + str(soup.encode('ascii')))

#Input: python filename <seed> <bfs/dfs> <keyword separated with commas>
#Then: sys.argv = [filename, <seed>, <bfs/dfs>, <keywords separated with commas>]
def main():
    list=[]

    if len(sys.argv) > 3:
        keyword = sys.argv[3]
        list.append(keyword.split(","))
        print(list)
    elif len(sys.argv) < 3:
        sys.exit('Format to run: python {0} <seed> <bfs/dfs> <key>(optional)'.format(sys.argv[0]))
    else:
        keyword = []
    seed = sys.argv[1]
    if sys.argv[2] == 'bfs':
        bfs(seed, keyword)  # call to bfs function
    if sys.argv[2] == 'dfs':
        dfs(seed, keyword)  # call to dfs function


if __name__ == '__main__':
    main()