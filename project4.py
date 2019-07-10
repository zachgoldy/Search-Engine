"""
Module Docstring for Project 4

By: Zach Gold
"""
import os
import math
from hashtables import HashTableLinear


class SearchEngine:
    """
    Builds and maintains an inverted index of documents stored in a specified directory and
        provides a functionality to search documents with query terms.
    Attributes:
        directory (str) : a directory name
        stopwords (HashTableLinear) : a hash table containing stopwords
        doc_length (HashTableLinear) : a hash table containing the total number of words in each
            document
        doc_freqs (HashTableLinear) : a hash table containing the number of documents containing the
            term for each term
        term_freqs (HashTableLinear) : a hash table of hash tables for each term. Each hash table
            contains the frequency of the term in documents (document names are the keys and the
            frequencies are the values)
    """
    def __init__(self, directory, stopwords=[]):
        self.doc_length = HashTableLinear()  # Replace HashTableLinear() with your hash table.
        self.doc_freqs = HashTableLinear()  # this will not be used in this assignment
        self.term_freqs = HashTableLinear()
        self.stopwords = stopwords
        self.index_files(directory)
        self.directory = directory

    def read_file(self, infile):
        """A helper function to read a file
        Args:
        infile (str) : the path to a file
        Returns:
        list : a list of str read from a file
        """
        with open(infile, 'r') as reader:
            return_list = reader.readlines()
        return return_list

    def parse_words(self, lines):
        """split strings into words
        Convert words to lower cases and remove new line chars.
        Exclude stopwords.
        Args:
        lines (list) : a list of strings
        Returns:
        list : a list of words
        """
        return_list = []
        for i in lines:
            i = i.lower()
            i = i.split()
            for j in i:
                j = j.replace('\n', '')
                if j not in self.stopwords:
                    return_list.append(j)
        return return_list

    def count_words(self, filename, words):
        """count words in a file and store the frequency of each
        word in the term_freqs hash table. Words should not contain stopwords.
        Also store the total count of words contained in the file
        in the doc_length hash table.
        Args:
        filename (str) : the file name
        words (list) : a list of words
        """
        #file_lines = self.read_file(filename)
        #str_list = self.parse_words(file_lines)
        for i in words:
            self.term_freqs.put(i, HashTableLinear())
        self.doc_freqs.put(filename, 0)
        for i in words:
            if i in self.term_freqs and filename in self.term_freqs[i]:
                self.term_freqs[i][filename] = self.term_freqs[i][filename] + 1
            elif i and i in self.term_freqs:
                self.term_freqs[i].put(filename, 1)
            elif i:
                self.term_freqs.put(i, HashTableLinear())
                self.term_freqs[i].put(filename, 1)
        self.doc_freqs[filename] = len(words)


    def index_files(self, directory):
        """index all text files in a given directory
        Args:
        directory (str) : the path of a directory
        """
        txt_list = os.listdir(directory)
        for i in txt_list:
            if ".txt" in i:
                j = self.parse_words(self.read_file(os.path.join(directory, i)))
                self.count_words(i, j)

    def get_weighted_freq(self, total_freq):
        """comptes the weighted frequency
        Args:
        tf (float) : term frequency
        Returns:
        float : the weighted frequency
        """
        if total_freq > 0:
            weighted_freq = 1 + math.log(total_freq)
        else:
            weighted_freq = 0
        return weighted_freq

    def get_scores(self, terms):
        """creates a list of scores for each file in corpus
        The score = weighted frequency / the total word count in the file.
        Compute this score for each term in a query and sum all the scores.
        Args:
        terms (list) : a list of str
        Returns:
        list : a list of tuples, each containing the filename and its relevancy score
        """
        scores = ([], [])
        for term in terms:
            if term not in self.term_freqs:
                raise ValueError
            for i in self.term_freqs[term].hash_table:
                if i and i.key not in scores[0]:
                    file = i.key
                    freq = i.data
                    scores[0].append(file)
                    freq = self.get_weighted_freq(freq) / self.doc_freqs[file]
                    scores[1].append(freq)
                elif i and i.key in scores[0]:
                    file = i.key
                    freq = i.data
                    freq = self.get_weighted_freq(freq) / self.doc_freqs[file]
                    ind = scores[0].index(i.key)
                    scores[1][ind] += freq
        return scores

    def rank(self, scores):
        """ranks files in the descending order of relevancy
        Args:
        scores(list) : a list of tuples: (filename, score)
        Returns:
        list : a list of tuples: (filename, score) sorted in descending order of relevancy
        """
        for i in range(len(scores[0])-1, 0, -1): # extra credit implementation of sorting algorithm.
            for j in range(len(scores[0])-1):
                if scores[1][j] < scores[1][j+1]:
                    temp = scores[0][j]
                    temp2 = scores[1][j]
                    scores[0][j] = scores[0][j+1]
                    scores[1][j] = scores[1][j+1]
                    scores[0][j+1] = temp
                    scores[1][j+1] = temp2
        return scores

    def search(self, query):
        """
        Searches query and returns stuff.
        :param query:
        :return:
        """
        temp_list = query.lower()
        temp_list = temp_list.split()
        query_list = self.parse_words(temp_list)
        scores_tuple = self.get_scores(query_list)
        ranked_scores = self.rank(scores_tuple)
        str = ""
        for i in ranked_scores[0]:
            if i:
                str += "%s/%s \n" % (self.directory, i)
        return str


def import_stopwords(filename, hashtable):
    """
    Takes a file of words and returns a hash table containing each word.
    :param filename: String referring to file mentioned
    :param hashtable: empty hashtable object (one of the 3 above)
    :return:
    hashtable
    """
    file = open(filename, "r")
    string_file = file.read()
    file.close()

    temp_string = ""
    for i in string_file:
        if i == " ":
            hashtable.put(temp_string, temp_string)
            temp_string = ""
        else:
            temp_string += i
    return hashtable


def main(directory):
    hash = HashTableLinear()
    hash = import_stopwords("stop_words.txt", hash)
    search = SearchEngine(directory, hash)
    while True:
        inp = input("Search here:")
        if inp == "q":
            break
        elif inp == "s:":
            inp = input("Search multiple things:")
            print(search.search(inp))

if __name__ == '__main__':
        # execute main() function
        main("docs")