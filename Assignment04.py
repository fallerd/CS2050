from __future__ import print_function
from sys import stdin
import unittest

'''
Description:
Author:
Version:
Help received from:
Help provided to:
'''

class FamilyTree(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.left = self.right = None
        self.parent = parent

    def __iter__(self):
        if self.left:
            for node in self.left:
                yield node

        yield self.name

        if self.right:
            for node in self.right:
                yield node

    def __str__(self):
        return ','.join(str(node) for node in self)

    def add_below(self, parent, child):
        ''' Add a child below a parent. Only two children per parent
            allowed. '''

        where = self.find(parent)

        if not where:
            raise ValueError('could not find ' + parent)

        if not where.left:
            where.left = FamilyTree(child, where)
        elif not where.right:
            where.right = FamilyTree(child, where)
        else:
            raise ValueError(self + 'already has the allotted two children')

    # Not a BST; have to search up to the whole tree
    def find(self, name):
        if self.name == name: return self

        if self.left:
            left = self.left.find(name)
            if left: return left

        if self.right:
            right = self.right.find(name)
            if right: return right

        return None

    def parent(self, name):
        pass

    def grandparent(self, name):
        pass

    def generations(self):
        ''' Return a list of lists, where each sub-list is a generation.  '''

        # First, create a list 'this_level' with the root, and three empty
        # lists: 'next_level', 'result', and 'names'

        # While 'this_level' has values
            # Remove the first element and append its name to 'names'

            # If the first element has a left, append it to 'next_level'
            # and do the same for the right

            # If 'this_level' is now empty
                # Append 'names' to 'result', set "this_level' to
                # 'next_level', and 'next_level' and 'names' to empty
                # lists

        # return result

    def inorder(self):
        ''' Return a list of the in-order traversal of the tree. '''
        pass

    def preorder(self):
        ''' Return a list of the pre-order traversal of the tree. '''
        pass

    def postorder(self):
        ''' Return a list of the post-order traversal of the tree. '''
        pass

class CLevelTests(unittest.TestCase):
    def test_empty(self):
        self.assertEquals(str(FamilyTree(None)), 'None')
    def setUp(self):
        self.tree = FamilyTree("Grandpa")
        self.tree.add_below("Grandpa", "Homer")
        self.tree.add_below("Grandpa", "Herb")
        self.tree.add_below("Homer", "Bart")
        self.tree.add_below("Homer", "Lisa")
    def test_str(self):
        self.assertEquals(str(self.tree), "Bart,Homer,Lisa,Grandpa,Herb")

class BLevelTests(unittest.TestCase):
    ''' Write tests for your pre, in, and post-order traversals. '''

class ALevelTests(unittest.TestCase):
    def testparent(self):
        self.assertEquals(self.tree.parent("Lisa"), "Homer")
    def test_grandparent(self):
        self.assertEquals(self.tree.grandparent("Lisa"), "Grandpa")
    def test_no_grandparent(self):
        self.assertEquals(self.tree.grandparent("Homer"), None)
    def test_generations(self):
        self.assertEquals(self.tree.generations(), \
            [["Grandpa"], ["Herb", "Homer"], ["Bart", "Lisa"]])

    ''' Write some more tests, espcially for your generations method. '''

if '__main__' == __name__:
    ''' Read from standard input a list of relatives. The first line must
        be the ultimate ancestor (the root). The following lines are in the
        form: parent child.'''

    for line in stdin:
        a = line.strip().split(" ")
        if len(a) == 1:
            ft = FamilyTree(a[0])
        else:
            ft.add_below(a[0], a[1])

    print(ft.generations())
