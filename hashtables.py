"""
Module implements three types of hashtables and collisions: Seperate chaining,
and quadratic and linear probing.

All 3 are implemented as different classes.
"""
from linked_list import Node

class HashTableSepchain:
    """
    Implementation of Hash Table using Seperate chaining

    Attributes:
        self.hash_table(list): List of nodes containing key data and next values
        num_items(int): number of key/data pairs in the hash table.
        num_collisions(int): number of collisions that have occurred
        size(int): size of the hash_table (including null values)
    """
    def __init__(self, table_size=11):
        """
        Initiates object
        :param table_size: initial size of table
        """
        self.hash_table = [None] * table_size
        self.num_items = 0
        self.num_collisions = 0
        self.num_items = table_size

    def __eq__(self, other):
        """
        Tests for equality with other sepchain object
        :param other:  other sepchain object
        :return: True if equal, False if not.
        """
        if other.size != self.num_items:
            return False
        else:
            for i in range(self.num_items):
                if self.hash_table[i] != other.hash_table[i]:
                    return False
            return True

    def __repr__(self):
        """
        Creates a string representation of the hashtable
        :return: str(String): string represetnation of hashtable
        """
        return str(self.hash_table)

    def hash_string(self, string):
        """
        Takes a string and returns its hash value
        :param string(String): String put into function
        :return: hash(int): Hash value of the string
        """
        hash_int = 0
        for letter in string:
            hash_int = (hash_int * 31 + ord(letter)) % self.num_items
        return hash_int

    def put(self, key, data):
        """
        Puts a new key/data Node into the table
        :param key: the key
        :param data: the data value
        :return: None
        """
        self.num_items += 1
        if self.num_items/self.num_items > 1.5:
            new_hash = self.resize()
            self.hash_table = new_hash.hash_table
            self.num_items = new_hash.size
        index = self.hash_string(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, data)
        else:
            self.hash_table[index].next = Node(key, data)
            self.num_collisions += 1

    def resize(self):
        """
        Creates a new table with twice the size of the old one, and fills it up
        with the old tables values, sets hash table to the new table
        :return:
        """
        new_hash = HashTableSepchain(self.num_items*2 + 1)
        for i in self.hash_table:
            if i is not None:
                new_hash.put(i.key, i.data)
        return new_hash

    def get(self, key):
        """
        Finds the data value of a Node given its key
        :param key(String): key
        :return: data value (String)
        """
        for i in self.hash_table:
            if i is not None:
                if i.key == key:
                    return i.data
        raise LookupError

    def contains(self, key):
        """
        Tests to see if a table has a Node with a certain key in it
        :param key(String): key the function looks for
        :return: True if key is found, False if not.
        """
        found = False
        for i in self.hash_table:
            if i.key == key:
                found = True
        return found

    def remove(self, key):
        """
        Removes a key/data pair from the table given its key
        :param key: (String) key the function searches for
        :return: key/data pair that the function removed.
        """
        if not self.contains(key):
            raise LookupError
        else:
            for i in range(len(self.hash_table)):
                if self.hash_table[i] is not None:
                    if self.hash_table[i].key == key:
                        self.num_items -= 1
                        return self.hash_table.pop(i)

    def size(self):
        """
        Returns the number of items that the hash table has stored.
        :return:  num_items(int): see above.
        """
        return self.num_items

    def load_factor(self):
        """
        Returns load factor.
        :return: load_factor(int)
        """
        return self.num_items/self.num_items()

    def collisions(self):
        """
        Returns number of collisions that the hash table has
        experienced.
        :return:  num_collisions(int)
        """
        return self.num_collisions

    def __getitem__(self, key):
        """
        Resets default get item to the get function we made
        :param key: see get function
        :return:
        """
        return self.get(key)

    def __setitem__(self, key, data):
        """
        Resets default set item function to put function
        see put function for more info.
        :param key:
        :param data:
        :return:
        """
        self.put(key, data)

    def __contains__(self, key):
        """
        Resets default contains function to our new contains function.
        See contains() for more info.
        :param key:
        :return:
        """
        return self.contains(key)


class HashTableQuadratic:
    """
    Implementation of Hash Table using Quadratic probing

    Attributes:
        self.hash_table(list): List of nodes containing key data and next values
        num_items(int): number of key/data pairs in the hash table.
        num_collisions(int): number of collisions that have occurred
        size(int): size of the hash_table (including null values)
    """
    def __init__(self, table_size=11):
        """
        Initializes object
        :param table_size:
        """
        self.hash_table = [None] * table_size
        self.num_items = 0
        self.num_collisions = 0
        self.num_items = table_size

    def __eq__(self, other):
        """
        Tests to see if one object is equal to another
        :param other:
        :return: True if equal to other, false if not.
        """
        if other.size != self.num_items:
            return False
        else:
            for i in range(self.num_items):
                if self.hash_table[i] != other.hash_table[i]:
                    return False
            return True

    def __repr__(self):
        """
        :return: a string representation of the hash table.
        """
        return str(self.hash_table)

    def hash_string(self, string):
        """
        takes a string and returns its hash value.
        :param string: the string mentioned
        :return: hash(int): the hash value of said string.
        """
        hash = 0
        for c in string:
            hash = (hash * 31 + ord(c)) % self.num_items
        return hash

    def put(self, key, data):
        """
                Puts a new key/data Node into the table
                :param key: the key
                :param data: the data value
                :return: None
        """
        self.num_items += 1
        if self.load_factor() > .75:
            new_hash = self.resize()
            self.hash_table = new_hash.hash_table
            self.num_items = new_hash.size
        index = self.hash_string(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = {key: data}
        else:
            count = 1
            while self.hash_table[index] % self.num_items is not None:
                index = (index + count**2) % self.num_items
                count += 1
            self.hash_table[index] = {key: data}
            self.num_collisions += 1

    def resize(self):
        """
        Creates a new table with twice the size of the old one, and fills it up
        with the old tables values, sets hash table to the new table
        :return:
        """
        new_hash = HashTableSepchain(self.num_items*2 + 1)
        for i in self.hash_table:
            if i is not None:
                new_hash.put(i.key, i.data)
        return new_hash

    def get(self, key):
        """
        Finds the data value of a Node given its key
        :param key(String): key
        :return: data value (String)
        """
        for i in self.hash_table:
            if i is not None:
                if i.key == key:
                    return i.data
        raise LookupError

    def contains(self, key):
        """
        Tests to see if a table has a Node with a certain key in it
        :param key(String): key the function looks for
        :return: True if key is found, False if not.
        """
        found = False
        for i in self.hash_table:
            if i.key == key:
                found = True
        return found

    def remove(self, key):
        """
        Removes a key/data pair from the table given its key
        :param key: (String) key the function searches for
        :return: key/data pair that the function removed.
        """
        if not self.contains(key):
            raise LookupError
        else:
            for i in range(len(self.hash_table)):
                if self.hash_table[i] is not None:
                    if self.hash_table[i].key == key:
                        self.num_items -= 1
                        return self.hash_table.pop(i)

    def size(self):
        """
        Returns the number of items that the hash table has stored.
        :return:  num_items(int): see above.
        """
        return self.num_items

    def load_factor(self):
        """
        Returns load factor.
        :return: load_factor(int)
        """
        return self.num_items/self.num_items()

    def collisions(self):
        """
        Returns number of collisions that the hash table has
        experienced.
        :return:  num_collisions(int)
        """
        return self.num_collisions

    def __getitem__(self, key):
        """
        Resets default get item to the get function we made
        :param key: see get function
        :return:
        """
        return self.get(key)

    def __setitem__(self, key, data):
        """
        Resets default set item function to put function
        see put function for more info.
        :param key:
        :param data:
        :return:
        """
        self.put(key, data)

    def __contains__(self, key):
        """
        Resets default contains function to our new contains function.
        See contains() for more info.
        :param key:
        :return:
        """
        return self.contains(key)


class HashTableLinear:
    """
    Implementation of Hash Table using Seperate chaining

    Attributes:
        self.hash_table(list): List of nodes containing key data and next values
        num_items(int): number of key/data pairs in the hash table.
        num_collisions(int): number of collisions that have occurred
        size(int): size of the hash_table (including null values)
    """
    def __init__(self, table_size=2):
        """
        initializes object
        :param table_size: default table size is 11
        """
        self.hash_table = [None] * table_size
        self.num_items = 0
        self.num_collisions = 0
        self.table_size = table_size

    def __eq__(self, other):
        """
        tests to see if the object is the same as another.
        :param other: other object
        :return: True if equal, false if not
        """
        if other.size != self.num_items:
            return False
        else:
            for i in range(self.num_items):
                if self.hash_table[i] != other.hash_table[i]:
                    return False
            return True

    def __repr__(self):
        """
        Creates a string representation of the hash table
        :return: str(String): see above
        """
        return str(self.hash_table)

    def __len__(self):
        return self.num_items


    def hash_string(self, string):
        """
        Takes a String and finds its hash value
        :param string: String put into function
        :return: hash(int): hash value of said String
        """
        hash = 0
        for c in string:
            hash = (hash * 31 + ord(c)) % self.num_items
        return hash

    def put(self, key, data):
        """
                Puts a new key/data Node into the table
                :param key: the key
                :param data: the data value
                :return: None
        """
        self.num_items += 1
        if self.load_factor() > .75:
            new_hash = self.resize()
            self.hash_table = new_hash.hash_table
            self.table_size = new_hash.table_size
        index = self.hash_string(key)
        if self.hash_table[index] is None:
            self.hash_table[index] = Node(key, data)
        else:
            count = 1
            while self.hash_table[index] is not None:
                index = (index + 1) % self.num_items
                count += 1
            self.hash_table[index] = Node(key, data)
            self.num_collisions += 1

    def resize(self):
        """
        Creates a new table with twice the size of the old one, and fills it up
        with the old tables values, sets hash table to the new table
        :return:
        """
        new_hash = HashTableLinear(self.num_items*2 + 1)
        for i in self.hash_table:
            if i is not None:
                new_hash.put(i.key, i.data)
        return new_hash

    def get(self, key):
        """
        Finds the data value of a Node given its key
        :param key(String): key
        :return: data value (String)
        """
        for i in self.hash_table:
            if i and i.key == key:
                return i.data


    def contains(self, key):
        """
        Tests to see if a table has a Node with a certain key in it
        :param key(String): key the function looks for
        :return: True if key is found, False if not.
        """
        found = False
        for i in self.hash_table:
            if i:
                if i.key == key:
                    found = True
        return found

    def remove(self, key):
        """
        Removes a key/data pair from the table given its key
        :param key: (String) key the function searches for
        :return: key/data pair that the function removed.
        """
        if not self.contains(key):
            raise LookupError
        else:
            for i in range(len(self.hash_table)):
                if self.hash_table[i] is not None:
                    if self.hash_table[i].key == key:
                        self.num_items -= 1
                        return self.hash_table.pop(i)

    def size(self):
        """
        Returns the number of items that the hash table has stored.
        :return:  num_items(int): see above.
        """
        return self.num_items

    def load_factor(self):
        """
        Returns load factor.
        :return: load_factor(int)
        """
        return self.num_items/self.table_size

    def collisions(self):
        """
        Returns number of collisions that the hash table has
        experienced.
        :return:  num_collisions(int)
        """
        return self.num_collisions

    def __getitem__(self, key):
        """
        Resets default get item to the get function we made
        :param key: see get function
        :return:
        """
        return self.get(key)

    def __setitem__(self, key, data):
        """
        Resets default set item function to put function
        see put function for more info.
        :param key:
        :param data:
        :return:
        """
        for i in self.hash_table:
            if i and i.key == key:
                ind = self.hash_table.index(i)
        if ind is not None and self.hash_table[ind]:
            self.hash_table[ind].data = data
        else:
            raise ValueError

    def __contains__(self, key):
        """
        Resets default contains function to our new contains function.
        See contains() for more info.
        :param key:
        :return:
        """
        return self.contains(key)


    def key_list(self):
        key_list = []
        for i in self.hash_table:
            if i:
                key_list.append(i.data)
        return key_list


