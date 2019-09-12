from Phase2.SnippetGeneration import SnippetGeneration
import os



def fetch_input_queries(file_name):
        """
        Method to fetch inverted indexes of the certain input query terms only.
        :param inverted_index: the dictionary with all query terms
        :return: target_dict with inverted indexes of only query terms, query_term_freq term frequency of each word in query.
        """
        queries_dict = {}
        with open(file_name) as file_data:
            count = 1
            each_line = file_data.readline()
            while each_line:
                each_line.strip()
                query_id = each_line.split(None, 1)[0]
                query = ' '.join(each_line.split()[1:])
                # print("Line {}: {}".format(query_id, query))
                queries_dict[query_id] = query
                each_line = file_data.readline()
                count += 1
        return queries_dict


if __name__ == '__main__':

    snippet_generation = SnippetGeneration()
    queries_dict = fetch_input_queries("../queries_clean.txt")
    files = os.listdir("../" + "bm25")
    snippet_generation.generate_and_highlight_snippets(queries_dict,files)


