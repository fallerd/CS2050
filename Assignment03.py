from __future__ import print_function
import unittest

'''
Description: Recursive Find-and-Replace Function
Author: David Faller
Version: 1000
Help received from: pohuing on /r/python discord channel: helped condense
    'if find == None or replace == None or string == None ...'
Help provided to:
'''

def findandreplace(find, replace, string):
    if None in (find, replace, string) or find == "" or len(string) == 0:
        return string
    if string[:len(find)] == find:
        return (replace + findandreplace(find, replace, string[len(find):]))
    return (string[0] + findandreplace(find, replace, string[1:]))


class TestFindAndReplace(unittest.TestCase):
    def test_all_none(self):
        self.assertEqual(findandreplace(None, None, None), None)
    def test_find_none(self):
        self.assertEqual(findandreplace(None, "a", "aabb"), "aabb")
    def test_find_empty(self):
        self.assertEqual(findandreplace("", "a", "aabb"), "aabb")
    def test_replace_none(self):
        self.assertEqual(findandreplace("a", None, "aabb"), "aabb")
    def test_string_none(self):
        self.assertEqual(findandreplace("a", "b", None), None)
    def test_simple(self):
        self.assertEqual(findandreplace("a", "b", "aabb"), "bbbb")
    def test_middle(self):
        self.assertEqual(findandreplace("t", "z", "aatbb"), "aazbb")
    def test_end(self):
        self.assertEqual(findandreplace("t", "z", "aabb t"), "aabb z")
    def test_remove(self):
        self.assertEqual(findandreplace(" ", "", " a abb"), "aabb")
    def test_gettysburg(self):
        self.assertEqual(findandreplace("Four score", "Twenty", \
            "Four score and seven years ago"), "Twenty and seven years ago")
    def test_gettysburg(self):
        self.assertEqual(findandreplace("seven", "eight", \
            "Four score and seven years ago"), "Four score and eight years ago")

if '__main__' == __name__:
            unittest.main()