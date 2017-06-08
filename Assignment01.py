from __future__ import print_function
import unittest

'''Assignment 01.py completed by David Faller for CS 2050'''

''' when run with "-m unittest", the following produces:
    FAILED (failures=9, errors=2)
    your task is to fix the failing tests by implementing the necessary
    methods. '''

class LinkedList(object):
    class Node(object):
        # pylint: disable=too-few-public-methods
        ''' no need for get or set, we only access the values inside the
            LinkedList class. and really, never have setters. '''
        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node

    def __init__(self, initial=None):
        if initial is not None:
            self.front = self.back = self.current = self.previous  = None
            for entry in initial:
                self.push_front(str(entry))
        else:
            self.front = self.back = self.current = self.previous  = None

    def empty(self):
        return self.front == self.back == None

    def __iter__(self):
        self.current = self.front
        return self

    def __next__(self):
        if self.current:
            tmp = self.current.value
            self.current = self.current.next_node
            return tmp
        else:
            raise StopIteration()

    def iter_previous(self):
        '''Method to iterate self.previous'''
        self.previous = self.current

    def single(self):
        '''Method to determine if a linked list is a single-item list'''
        return self.front == self.back != None

    def __str__(self):
        '''Method to return a string of list node values to satisfy TestStr, pops values from list for simplicity'''
        reverse_string = ""
        while not self.empty():
            if self.front != self.back:
                reverse_string += self.pop_back() + ', '
            else:
                reverse_string += self.pop_back()
        return reverse_string

    def __repr__(self):
        '''Method to create a simple string representation for a given linked list to satisfy TestRepr'''
        representation = "LinkedList(("+self.__str__()+"))"
        return representation

    def push_front(self, value):
        new = self.Node(value, self.front)
        if self.empty():
            self.front = self.back = new
        else:
            self.front = new

    ''' you need to(at least) implement the following three methods'''
    def pop_front(self):
        '''Method removes first node of list and returns its value'''
        if self.empty():
            raise RuntimeError("list is empty, can't pop front")
        else:
            tmp_value = self.front.value
            if self.single():
                self.__init__()
                return tmp_value
            else:
                self.front = self.front.next_node
                return tmp_value

    def push_back(self, value):
        '''Method adds node at end of list and sets its value'''
        new = self.Node(value, None)
        if self.empty():
            self.front = self.back = new
        else:
            self.back.next_node = new
            self.back = new

    def pop_back(self):
        '''Method finds penultimate node in list, makes it the final node,
        and returns the value of the previous final node'''
        if self.empty():
            raise RuntimeError("list is empty, can't pop back")
        else:
            tmp_value = self.back.value
            if self.single():
                self.__init__()
                return tmp_value
            else:
                self.__iter__()
                while self.current.next_node != self.back:
                    self.__next__()
                self.back = self.current
                return tmp_value

    def __delete__(self, value):
        '''Method deletes all nodes in a list associated with a given value'''
        if self.empty():
            raise RuntimeError("list is empty, can't delete anything")
        else:
            removal_count = 0
            if value == self.front.value:
                self.pop_front()
                removal_count += 1
            if not self.single():
                self.__iter__()
                self.iter_previous()
                self.__next__()
                while self.current != self.back:
                    if value == self.current.value:
                        self.previous.next_node = self.current.next_node
                        removal_count += 1
                    else:
                        self.iter_previous()
                    self.__next__()
                if value == self.back.value:
                    self.pop_back()
                    removal_count += 1
            return "Deleted " + str(removal_count) + " instances of '" + str(value) +"'"

    def find_middle(self):
        '''Method returns the middle value of an odd-noded list or returns a tuple of an even-noded list'''
        if self.empty():
            raise RuntimeError("list is empty, no middle")
        else:
            middle = self.front
            if self.single():
                return middle.value
            else:
                count = 1
                self.__iter__()
                while self.current != self.back:
                    if 0 == count%2:
                        middle = middle.next_node
                    self.__next__()
                    count +=1
                if 0 == count%2:
                    even_middle = middle.next_node
                    return (middle.value, even_middle.value)
                else:
                    return middle.value


''' C-level work '''
class TestEmpty(unittest.TestCase):
    def test(self):
        self.assertTrue(LinkedList().empty())

class TestPushFrontPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertEqual(linked_list.pop_back(), 2)
        self.assertEqual(linked_list.pop_back(), 3)
        self.assertTrue(linked_list.empty())

class TestPushFrontPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertTrue(linked_list.empty())

class TestPushBackPopFront(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back(2)
        linked_list.push_back(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertTrue(linked_list.empty())

class TestPushBackPopBack(unittest.TestCase):
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back([3, 2, 1])
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), [3, 2, 1])
        self.assertEqual(linked_list.pop_back(), "foo")
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertTrue(linked_list.empty())

''' B-level work '''
class TestInitialization(unittest.TestCase):
    def test(self):
        linked_list = LinkedList(("one", 2, 3.141592))
        self.assertEqual(linked_list.pop_back(), "one")
        self.assertEqual(linked_list.pop_back(), "2")
        self.assertEqual(linked_list.pop_back(), "3.141592")

class TestStr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__str__(), '1, 2, 3')

''' A-level work '''
class TestRepr(unittest.TestCase):
    def test(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__repr__(), 'LinkedList((1, 2, 3))')

class TestErrors(unittest.TestCase):
    def test_pop_front_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_front())
    def test_pop_back_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_back())
    def test_middle_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().find_middle())
    def test_middle_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().find_middle())

''' write some more test cases. '''

class TestPushPushPopPushPop(unittest.TestCase):
    '''Tests Pushing and Popping on a list that hasn't been fully emptied'''
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), "foo")
        linked_list.push_back("bar")
        self.assertEqual(linked_list.pop_back(), "bar")

class TestListEmptyThenRefill(unittest.TestCase):
    '''Tests fully emptying a list and re-filling it'''
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.pop_back()
        linked_list.pop_back()
        self.assertTrue(linked_list.empty())
        linked_list.push_back(2)
        self.assertEqual(linked_list.pop_back(), 2)


''' extra credit.
    - write test cases for and implement a delete(value) method.
    - write test cases for and implement a method that finds the middle
      element with only a single traversal.
'''

class TestDeleteValue(unittest.TestCase):
    '''Tests if __delete__ method deletes all nodes associated with a given value'''
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back("foo")
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back("foo")
        linked_list.push_back("foo")
        linked_list.push_back("bar")
        linked_list.push_back("foo")
        self.assertEqual(linked_list.__delete__("foo"), "Deleted 5 instances of 'foo'")
        self.assertEqual(linked_list.pop_back(), "bar")
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertTrue(linked_list.empty())

class TestFindMiddleOdd(unittest.TestCase):
    '''Tests find_middle method for odd-noded list'''
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back("bar")
        self.assertEqual(linked_list.find_middle(), "foo")

class TestFindMiddleEven(unittest.TestCase):
    '''Tests find_middle method for even-noded list'''
    def test(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back("bar")
        linked_list.push_back(2)
        self.assertEqual(linked_list.find_middle(), ('foo', 'bar'))

''' the following is a demonstration that uses our data structure as a
    stack'''

def fact(number):
    '''"Pretend" to do recursion via a stack and iteration'''

    if number < 0: raise ValueError("Less than zero")
    if number == 0 or number == 1: return 1

    stack = LinkedList()
    while number > 1:
        stack.push_front(number)
        number -= 1

    result = 1
    while not stack.empty():
        result *= stack.pop_front()

    return result

class TestFactorial(unittest.TestCase):
    def test_less_than_zero(self):
        self.assertRaises(ValueError, lambda: fact(-1))
    def test_zero(self):
        self.assertEqual(fact(0), 1)
    def test_one(self):
        self.assertEqual(fact(1), 1)
    def test_two(self):
        self.assertEqual(fact(2), 2)
    def test_10(self):
        self.assertEqual(fact(10), 10*9*8*7*6*5*4*3*2*1)

if '__main__' == __name__:
    unittest.main()