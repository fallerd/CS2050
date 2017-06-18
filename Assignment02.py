from __future__ import print_function
import unittest
import math

'''
Description: CS2050 Assignment 02
Author: David Faller
Version: 1
Help provided to: samson01, nbarnes7
Help received from:
'''

'''
    Implement a dictionary using chaining.
    You may assume every key has a hash() method, e.g.:
    >>> hash(1)
    1
    >>> hash('hello world')
    -2324238377118044897
'''


class dictionary:
    def __init__(self, init=None):
        self.__limit = 10
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0

        if init:
            for i in init:
                self.__setitem__(i[0], i[1])

    def hash_modulo(self, key):
        ''' Returns appropriate hash for size of dictionary. '''
        return hash(key) % self.__limit

    def values(self):
        ''' Returns all values in list, sorted. '''
        value_list = [key_value[1] for hashed_key in self.__items for key_value in hashed_key]
        value_list.sort()
        return value_list

    def keys(self):
        ''' Returns all keys in list, sorted. '''
        key_list = [key_value[0] for hashed_key in self.__items for key_value in hashed_key]
        key_list.sort()
        return key_list

    def items(self):
        ''' Returns all key value pairs in list of tuples, sorted. '''
        item_list = [(key_value[0], key_value[1]) for hashed_key in self.__items for key_value in hashed_key]
        item_list.sort()
        return item_list

    def __len__(self):
        ''' Returns length of dictionary. '''
        return self.__count

    def __flattened(self):
        return [item for inner in self.__items for item in inner]

    def __iter__(self):
        return (iter(self.__flattened()))

    def __str__(self):
        return (str(self.__flattened()))

    def load_factor(self):
        ''' Returns load factor as int in range 0-100. '''
        return int(100 * float(self.__count) / self.__limit)

    def _rehash_(self):
        ''' Creates new dict with hash based on current self.__limit. '''
        old_items = self.__items
        self.__items = [[] for _ in range(self.__limit)]
        self.__count = 0
        for hashed_key in old_items:
            for key_value in hashed_key:
                self.__setitem__(key_value[0], key_value[1])

    def _half_rehash_(self):
        ''' Halves limit, rehashes dict. '''
        self.__limit = int(math.floor(self.__limit * .5))
        self._rehash_()

    def _double_rehash_(self):
        ''' Doubles limit, rehashes dict. '''
        self.__limit *= 2
        self._rehash_()

    def __setitem__(self, key, value):
        ''' Add key/value to the dictionary, deals with collisions and duplicate keys. '''
        hashed_key = self.hash_modulo(key)
        if self.__items[hashed_key]:  # if hashed key collides, check for key duplicates
            for key_value in self.__items[hashed_key]:  # iterate through keys to check for duplicates
                if key_value[0] == key:
                    key_value[1] = value
                    return
        self.__items[hashed_key].append([key, value])  # if no hash collision, add new vey/value
        self.__count += 1
        if self.load_factor() > 75:
            self._double_rehash_()

    def __getitem__(self, key):
        ''' Retrieve value from the dictionary for given key. '''
        hashed_key = self.hash_modulo(key)
        for key_value in self.__items[hashed_key]:  # look in hashed key entry, iterate if collided
            if key_value[0] == key:
                return key_value[1]

    def __contains__(self, key):
        ''' Implements the 'in' operator '''
        for hashed_key in range(self.__limit):  # iterate through whole dict
            if self.__items[hashed_key]:  # if hash key has been init, iterate through in case of collisions
                for key_value in self.__items[hashed_key]:
                    if key_value[0] == key or key_value[1] == key:
                        return True
        return False

    def __delitem__(self, key):
        ''' Implements the 'del' operator. '''
        hashed_key = self.hash_modulo(key)
        for key_value in self.__items[hashed_key]:  # look in hashed key entry, iterate if collided
            if key_value[0] == key:
                self.__items[hashed_key].remove(key_value)
                self.__count -= 1
                if self.load_factor() < 25:
                    self._half_rehash_()
                break

    def __eq__(self, other_dict):
        ''' Implements the '=' operator. '''
        if self.__count == other_dict.__count:
            zipped = zip(self.items(), other_dict.items())
            for pairs in zipped:
                if pairs[0] != pairs[1]:
                    return False
            return True


''' C-level work
'''


class test_add_two(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[2] = "two"
        self.assertEqual(len(s), 2)
        self.assertEqual(s[1], "one")
        self.assertEqual(s[2], "two")


class test_add_twice(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = "one"
        s[1] = "one"
        self.assertEqual(len(s), 1)
        self.assertEqual(s[1], "one")


class test_store_false(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = False
        self.assertTrue(1 in s)
        self.assertTrue(1 in s)
        self.assertFalse(s[1])


class test_store_none(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[1] = None
        self.assertTrue(1 in s)
        self.assertEqual(s[1], None)


class test_none_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[None] = 1
        self.assertTrue(None in s)
        self.assertEqual(s[None], 1)


class test_False_key(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[False] = 1
        self.assertTrue(False in s)
        self.assertEqual(s[False], 1)


class test_collide(unittest.TestCase):
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(len(s), 2)
        self.assertTrue(0 in s)
        self.assertTrue(10 in s)


class test_none_collide(unittest.TestCase):
    ''' Testing to make sure nones collide/overwrite correctly. '''
    def test(self):
        s = dictionary()
        s[None] = "zero"
        s[None] = "ten"
        self.assertEqual(len(s), 1)
        self.assertFalse("zero" in s)
        self.assertTrue("ten" in s)


''' B-level work
    Add doubling and rehashing when load goes over 75%
    Add __delitem__(self, key)
'''


class test_double_rehash(unittest.TestCase):
    ''' Checks key hashes and load factor before and after doubling and rehashing. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(s.hash_modulo(0), s.hash_modulo(10))
        self.assertEqual(s.load_factor(), 20)
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        s["A"] = "Letter A"
        s[5] = "five"
        s[11] = "eleven"
        self.assertEqual(len(s), 8)
        self.assertEqual(s.load_factor(), 40)
        self.assertNotEqual(s.hash_modulo(0), s.hash_modulo(10))
        self.assertEqual(s[11], "eleven")


class test_delitem(unittest.TestCase):
    ''' Checks to confirm that del removes list key/value pairs. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        s[11] = "eleven"
        del s[0]
        self.assertFalse(0 in s)
        self.assertFalse("zero" in s)
        self.assertTrue(10 in s)
        del s[10]
        del s[11]
        self.assertFalse(10 in s)
        self.assertFalse(11 in s)
        self.assertFalse("ten" in s)
        self.assertFalse("eleven" in s)
        self.assertEqual(len(s), 0)


''' A-level work
    Add halving and rehashing when load goes below 25%
    Add keys()
    Add values()
'''


class test_half_rehash(unittest.TestCase):
    ''' Checks key hashes and load factor before and after halving and rehashing. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        self.assertEqual(s.hash_modulo(0), s.hash_modulo(10))
        s[1] = "one"
        s[2] = "two"
        s[3] = "three"
        s["A"] = "Letter A"
        s[5] = "five"
        s[11] = "eleven"
        self.assertEqual(len(s), 8)
        self.assertEqual(s.load_factor(), 40)
        self.assertNotEqual(s.hash_modulo(0), s.hash_modulo(10))
        del s["A"]
        del s[1]
        del s[5]
        del s[11]
        self.assertEqual(len(s), 4)
        self.assertEqual(s.load_factor(), 40)
        self.assertEqual(s.hash_modulo(0), s.hash_modulo(10))
        del s[10]
        del s[3]
        del s[0]
        self.assertEqual(len(s), 1)
        self.assertEqual(s.load_factor(), 50)


class test_values(unittest.TestCase):
    ''' Test return of sorted values in dictionary. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        s["A"] = "Letter A"
        self.assertEqual(["Letter A", "ten", "zero"], s.values())


class test_keys(unittest.TestCase):
    ''' Test return of sorted keys in dictionary. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        s["A"] = "Letter A"
        self.assertEqual([0, 10, "A"], s.keys())


''' Extra credit
    Add __eq__()
    Add items(), "a list of D's (key, value) pairs, as 2-tuples"
'''


class test_eq(unittest.TestCase):
    ''' Creates unordered dicts and compares for equality. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        d = dictionary()
        d[10] = "ten"
        d[0] = "zero"
        d[1] = "one"
        del d[1]
        d1 = dictionary()
        d1[10] = "ten"
        self.assertTrue(d == s)
        self.assertFalse(d1 == s)


class test_items(unittest.TestCase):
    ''' Tests return of sorted list of 2-tuples containing the key/value pairs. '''
    def test(self):
        s = dictionary()
        s[0] = "zero"
        s[10] = "ten"
        s["A"] = "Letter A"
        self.assertEqual([(0, "zero"), (10, "ten"), ("A", "Letter A")], s.items())


unittest.main()
