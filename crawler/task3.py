import math
import operator

inlink_dict = {}
outlink_dict = {}
last_page_rank_dict = {}
new_page_rank_dict = {}
page_list = []
sink_page_list = []
url_page_rank_dict={}
#for lambda of 0.15
d = 0.85
#for lambda of 0.25
#d= 0.75
#for lambda of 0.35
#d= 0.65
#for lambda of 0.5
#d= 0.5
prefix_url= "https://en.wikipedia.org/wiki/"
file_name =""

#Function for parsing the graph
def parse_graph(graph):
    file_content = open (graph, 'r')
    for line in file_content.readlines ():
        words = line.split()
        populate_inlink_dictionary(words)
        populate_page_list(words)
    populate_outlink_dictionary()


def populate_inlink_dictionary(words):
    key = words[0]
    values = words[1:]
    inlink_dict[key] = values


def populate_page_list(words):
    page_list.insert(0, words[0])

#Function for populating the outlink dictionary
def populate_outlink_dictionary():
    for key in inlink_dict.keys():
        for value in inlink_dict[key]:
            if value in outlink_dict.keys():
                outlink_dict[value] = outlink_dict[value] + 1
            else:
                outlink_dict[value] = 1


#Function for assigning the initial page rank
def calculate_startup_pagerank():
    N = len(page_list)
    for page in page_list:
        last_page_rank_dict[page] = float(1) / N
    populate_sink_pagelist()

#Function for keeping a track of the sink pages
def populate_sink_pagelist():
    for page in page_list:
        if page not in outlink_dict.keys():
            sink_page_list.insert(0, page)

#Function to compute the L2 Norm
def calculateL2norm(new_page_rank_dict, last_page_rank_dict):
    sum = 0
    for page in new_page_rank_dict:
        diff= abs(new_page_rank_dict[page] - last_page_rank_dict[page])
        sum = sum + diff ** 2
    return math.sqrt(sum)

#Function to compute the page rank
# d is the damping factor
def pagerank_calculation():
    counter = 0
    iteration = 1
    file_l2norm = open(str(file_name)+"_L2-norm_pagerank_d" +str(d) + ".txt", "w+")
    file_l2norm.write("Iteration Number" + " : " + "L2Norm" + " : " + "sum of the computed PageRank values" + "\n")
    calculate_startup_pagerank()
    while counter < 4:
        sink_page_rank = 0
        for page in sink_page_list:
            sink_page_rank = sink_page_rank + last_page_rank_dict[page]
        for page in page_list:
            new_page_rank_dict[page] = float (1 - d) / len(page_list)
            new_page_rank_dict[page] += d * float(sink_page_rank / len (page_list))
            for inlink_page in inlink_dict[page]:
                new_page_rank_dict[page] = new_page_rank_dict[page] + (
                        d * float(last_page_rank_dict[inlink_page]) / float(outlink_dict[inlink_page]))

        current_L2norm = calculateL2norm(new_page_rank_dict, last_page_rank_dict)
        values = 0
        for page in new_page_rank_dict:
            values = values + new_page_rank_dict[page]

        file_l2norm.write(str(iteration) + " : " + str(current_L2norm) + " : " + str(values) + "\n")
        if current_L2norm < 0.001:
            counter = counter + 1
        else:
            counter = 0
        for page in page_list:
            last_page_rank_dict[page] = new_page_rank_dict[page]
        iteration = iteration + 1
    file_l2norm.close ()

#Function to sort the page rank and the url
def sort_page_rank_URL(page_rank_map):
    count=0
    file_page_rank = open(str(file_name)+"_SortedPageRank_URL_d" +str(d) + ".txt", "w+")
    file_page_rank.write("******************PageRank******************" + "\n")
    file_page_rank.write("The pages as per their URL and scores are : " + "\n")
    for docId in page_rank_map.keys():
        new_key = prefix_url + str(docId)
        url_page_rank_dict[new_key] = page_rank_map[docId]
    sorted_url_pagerank = sorted(url_page_rank_dict.items (), key=operator.itemgetter (1), reverse=True)
    while count < len(sorted_url_pagerank):
        file_page_rank.write(str (sorted_url_pagerank[count]))
        file_page_rank.write("\n")
        count=count+1
    file_page_rank.close()

#Function to sort the page rank with doc ids
def sort_page_rank_docID(page_rank_map):
    count=0
    sort_page_rank_URL(page_rank_map)
    sorted_dict = sorted(page_rank_map.items (), key=operator.itemgetter (1), reverse=True)
    file_page_rank = open(str(file_name)+"_SortedPageRank_docID_d"+str(d) + ".txt", "w+")
    file_page_rank.write("******************PageRank******************" + "\n")
    file_page_rank.write("The pages as per their docID and scores are : " + "\n")
    while count < 50 and count < len (sorted_dict):
        file_page_rank.write(str (sorted_dict[count]))
        file_page_rank.write("\n")
        count = count + 1
    file_page_rank.close()

#Function for sorting the inlink count in descending order
def sort_in_link (inlink):
    temp_dict = {}
    file_in_link = open(str(file_name)+"_Sorted_Inlink_d"+str(d) + ".txt", "w+")
    file_in_link.write("*******************InlinkStats*******************" +"\n")
    file_in_link.write("The pages sorted in descending order of the Inlink count are :" +"\n")
    for page in inlink.keys():
        temp_dict[page] = len(inlink.get(page))
    sorted_dict = sorted(temp_dict.items(), key=operator.itemgetter(1), reverse=True)
    count = 0
    while count < 20 and count < len (sorted_dict):
        file_in_link.write(str(sorted_dict[count]) +"\n")
        count += 1

#Function to count the number of sources
def count_sources(inlink_dict):
    counter = 0
    for page in inlink_dict.keys():
        if not inlink_dict[page]:
            counter += 1
    return counter

#Function to calculate the maximum in degree
def maximum_in_degree():
    max_in_degree = 0
    for key in inlink_dict.keys():
        values = inlink_dict[key]
        current_length = len(values)
        if max_in_degree < current_length:
            max_in_degree = current_length
    return max_in_degree

#Function to calculate the maximum out degree
def maximum_out_degree():
    max_out_degree = 0
    for key in outlink_dict.keys():
        value = outlink_dict[key]
        if max_out_degree < value:
            max_out_degree = value
    return max_out_degree


def main():
    graph = input('Enter the filename containing the graph: ')
    global file_name
    file_name = graph.split(".")[0]
    parse_graph(str(graph))
    pagerank_calculation()
    sort_page_rank_docID(new_page_rank_dict)
    sort_in_link(inlink_dict)
    file_stats = open(str(file_name)+"_Stats_d"+ str(d) + ".txt", "w+")
    file_stats.write("*******************GraphStatistics*******************" + "\n")
    file_stats.write(
        "The total number of pages in the graph with no out-links (sinks) are : " + str (len (sink_page_list)) + "\n")
    file_stats.write(
        "The total number of pages in the graph with no in-links (sources) are : " + str (
            count_sources (inlink_dict)) + "\n")
    file_stats.write("The maximum in-degree in the graph is : " + str(maximum_in_degree ()) + "\n")
    file_stats.write("The maximum out-degree in the graph is : " + str(maximum_out_degree ()) + "\n")
    file_stats.close()

if __name__ == "__main__":
    main()