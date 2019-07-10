import unittest
from hashtables import *
import hashtables

class TestList(unittest.TestCase):
    def test_sepchain(self):
        hash = HashTableSepchain()
        file = open("stop_words.txt", "r")
        file_string = file.read()
        file.close()
        length = 0
        for i in file_string:
            if i == " ":
                length += 1
        hash = import_stopwords("stop_words.txt", hash)
        self.assertEqual(hash.hash_table[hash.hash_string("please")].key, "please")
        self.assertEqual(hash.num_items, length)

    def test_linear(self):
        hash = HashTableSepchain()
        file = open("stop_words.txt", "r")
        file_string = file.read()
        file.close()
        length = 0
        for i in file_string:
            if i == " ":
                length += 1
        hash = import_stopwords("stop_words.txt", hash)
        self.assertEqual(hash.hash_table[hash.hash_string("please")].key, "please")
        self.assertEqual(hash.num_items, length)

    def test_quadratic(self):
        hash = HashTableSepchain()
        file = open("stop_words.txt", "r")
        file_string = file.read()
        file.close()
        length = 0
        for i in file_string:
            if i == " ":
                length += 1
        hash = import_stopwords("stop_words.txt", hash)
        self.assertEqual(hash.hash_table[hash.hash_string("please")].key, "please")
        self.assertEqual(hash.num_items, length)



if __name__ == '__main__':
    unittest.main()