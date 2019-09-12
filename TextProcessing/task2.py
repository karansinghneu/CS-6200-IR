import requests
import time
import re
from urllib.parse import urlparse, urljoin
import collections
from bs4 import BeautifulSoup

#Function to get the child URL
def find_child_url(url):
    time.sleep(1)
    child_url_list = []

    htmltext = requests.get(url)

    soup = BeautifulSoup(htmltext.content, 'html.parser')

    body = soup.find('div', {'id': 'bodyContent'})

    if len(soup.find('ol', class_='references') or ()) > 1:
        soup.find('ol', class_='references').decompose()

    total_links = body.find_all('a', {'href': re.compile("^/wiki/")})

    for link in total_links:
        target_link = link.get('href')
        if "/wiki/Main_Page" not in target_link and ":" not in target_link:
            url = urljoin("https://en.wikipedia.org", target_link)
            if "#" in target_link:
                url = url[: url.index('#')]
            if url not in child_url_list:
                child_url_list.append(str(url))

    return child_url_list

#Function to create a graph
def generate_graph(file):
    bfs_file = open(file, "r")

    crawled_urls = bfs_file.read().splitlines()
    child_mapping = collections.OrderedDict()

    for url in crawled_urls:
        child_url_list = find_child_url(url)
        direct_links = []
        for search_url in crawled_urls:
            if search_url != url:
                if search_url in child_url_list:
                    direct_links.append(get_id(search_url))
        child_mapping[get_id(url)] = direct_links

    g = in_link_generator(child_mapping)
    if file == "BFS.txt":
        generate_graph_file(g, "g1.txt")
    else:
        generate_graph_file(g, "g2.txt")

#Function to create a file containing the graph
def generate_graph_file(graph, file):
    output_file = open(file, "w")

    for key in graph.keys():
        output_file.write(key)
        for value in graph[key]:
            output_file.write(" ")
            output_file.write(value)
        output_file.write("\n")

    output_file.close()

#Function to generate the in links
def in_link_generator(child_graph):
    in_link_graph = collections.OrderedDict()

    for key in child_graph.keys():
        in_link_graph[key] = []

    for key in child_graph.keys():
        values = child_graph[key]
        for value in values:
            if value in in_link_graph:
                temp = in_link_graph[value]
                temp.append(key)
                in_link_graph[value] = temp
    return in_link_graph

#Function to get the doc ids
def get_id(url):
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    doc_id = url_path.split("/wiki/")[1]
    return doc_id


def main():
    generate_graph("BFS.txt")
    generate_graph("FOCUSED.txt")


if __name__== '__main__':
    main()