from __future__ import print_function
from sys import stdin
import unittest

'''
Description: Assignment 04 - Family Tree
Author: David Faller
Version: 02
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
            allowed. Names form a set.'''
        if not self.find(child):
            where = self.find(parent)
            if not where:
                raise ValueError('could not find ' + parent)
            if not where.left:
                where.left = FamilyTree(child, where)
            elif not where.right:
                where.right = FamilyTree(child, where)
            else:
                raise ValueError(self + 'already has the allotted two children')

    def find(self, name):
        '''Return node with given name'''
        if self.name == name: return self
        if self.left:
            left = self.left.find(name)
            if left: return left
        if self.right:
            right = self.right.find(name)
            if right: return right
        return None

    def Parent(self, name):
        '''Return name of parent'''
        if self.find(name):
            if self.find(name).parent:
                return self.find(name).parent.name
        else:
            return None

    def grandparent(self, name):
        '''Return name of grandparent'''
        if self.find(name):
            parent = self.Parent(name)
            if self.find(parent).parent:
                return self.find(parent).parent.name
        else:
            return None

    def generations(self, new_root=None):
        ''' Return a list of lists, where each sub-list is a generation.  '''

        if new_root:
            this_level = [self.find(new_root)]
            if this_level == [None]: return None
        else:
            this_level = [self]
        next_level = []
        result = []
        names = []

        while this_level:
            names.append(this_level[0].name)
            if this_level[0].left:
                next_level.append(this_level[0].left)
            if this_level[0].right:
                next_level.append(this_level[0].right)
            this_level.pop(0)

            if not this_level:
                result.append(names)
                names = []
                this_level = next_level
                next_level = []

        return result

    def inorder(self, list=None):
        ''' Return a list of the in-order traversal of the tree. '''
        if None == list:
            list = []
        if self.left:
            self.left.inorder(list)
            list.append(self.name)
            if self.right:
                self.right.inorder(list)
                return list
            list.append(self.name)
            return list
        list.append(self.name)
        return list

    def preorder(self, list=None):
        ''' Return a list of the pre-order traversal of the tree. '''
        if None == list:
            list = []
        list.append(self.name)
        if self.left:
            self.left.preorder(list)
            if self.right:
                self.right.preorder(list)
                return list
            return list
        return list


    def postorder(self, list=None):
        ''' Return a list of the post-order traversal of the tree. '''
        if None == list:
            list = []
        if self.left:
            self.left.postorder(list)
            if self.right:
                self.right.postorder(list)
                list.append(self.name)
                return list
            list.append(self.name)
            return list
        list.append(self.name)
        return list

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

    def test_inorder(self):
        self.assertEquals(self.tree.inorder(), ["Bart", "Homer", "Lisa", "Grandpa", "Herb"])
    def test_preorder(self):
        self.assertEquals(self.tree.preorder(), ["Grandpa", "Homer", "Bart", "Lisa", "Herb"])
    def test_postorder(self):
        self.assertEquals(self.tree.postorder(), ["Bart", "Lisa", "Homer", "Herb", "Grandpa"])

class BLevelTests(unittest.TestCase):
    def setUp(self):
        self.tree = FamilyTree("Grandpa")
        self.tree.add_below("Grandpa", "Homer")
        self.tree.add_below("Grandpa", "Herb")
        self.tree.add_below("Homer", "Bart")
        self.tree.add_below("Homer", "Lisa")
    def testparent(self):
        self.assertEquals(self.tree.Parent("Lisa"), "Homer")
        self.assertEquals(self.tree.Parent("Marge"), None)
    def test_grandparent(self):
        self.assertEquals(self.tree.grandparent("Lisa"), "Grandpa")
    def test_no_grandparent(self):
        self.assertEquals(self.tree.grandparent("Homer"), None)
        self.assertEquals(self.tree.grandparent("Marge"), None)

class ALevelTests(unittest.TestCase):
    def setUp(self):
        self.tree = FamilyTree("Grandpa")
        self.tree.add_below("Grandpa", "Homer")
        self.tree.add_below("Grandpa", "Herb")
        self.tree.add_below("Homer", "Bart")
        self.tree.add_below("Homer", "Lisa")
        self.tree.add_below("Lisa", "Zia")
        self.tree.add_below("Bart", "Kirk")
        self.tree.add_below("Bart", "Picard")
    def test_generations(self):
        self.assertEquals(self.tree.generations(), \
            [["Grandpa"], ["Homer", "Herb"], ["Bart", "Lisa"], ["Kirk", "Picard", "Zia"]])

    ''' Write some more tests, especially for your generations method. '''

    def test_generations_additive(self):
        tree1 = FamilyTree(None)
        self.assertEquals(tree1.generations(), [[None]])
        tree1.add_below(None, "Homer")
        tree1.add_below(None, "Herb")
        self.assertEquals(tree1.generations(), [[None], ["Homer", "Herb"]])
        tree1.add_below("Homer", None)
        self.assertEquals(tree1.generations(), [[None], ["Homer", "Herb"]])

    def test_generations_from(self):
        self.assertEquals(self.tree.generations("Homer"), [["Homer"], ["Bart", "Lisa"], ["Kirk", "Picard", "Zia"]])
        self.assertEquals(self.tree.generations("Bart"), [["Bart"], ["Kirk", "Picard"]])
        self.assertEquals(self.tree.generations("Marge"), None)

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
