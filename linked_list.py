class Node:
    '''THIS IS THE CLASS DOCS
        params:
            data(any type): some type of data that will be stored
                as the data variable of a new node.
            next(any type): some type of data that will be
                stored as the next variable of a new node.
        creates:
            Node object: a variable that stores a data variable and a next variable.
    '''

    def __init__(self, key =None, data= None):
        '''Initializes a Node object'''
        self.key = key
        self.data = data


    def __repr__(self):
        '''Converts Node into a String for printing'''
        return "Node(%s, %s)" % (self.key, self.data)

    def __eq__(self, other):
        '''Method to test if two nodes are equal'''
        if other is None:
            if self.key is None:
                return True
            else:
                return False
        if type(other) != Node:
            return False
        if self.data is not None and other.data is not None:
            return self.key == other.key and self.data == other.data
        elif self.data is not None and other.data is not None:
            return self.data == other.data

    def setdata(self, item):
        self.data = item


class LinkedList:
    def __init__(self):
        self.head = None
    def __eq__(self, other):
        return self.head == other.head
    def __repr__(self):
        return self.head.__repr__()
