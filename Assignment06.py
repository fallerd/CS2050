from __future__ import print_function
import unittest, sys

'''
Description: N Queens Solver
Author: David Faller
Version: 02
Help received from: http://www.datagenetics.com/blog/august42012/
Help provided to:
'''

def safe(one, two):
    if one[0] == two[0]: return False
    if one[1] == two[1]: return False
    if abs(two[0]-one[0]) == abs(two[1]-one[1]): return False
    return True

def print_solution(size, placed):
    print("for:", size)
    if placed == []:
        print("no solution found")
        return

    print('-' * size)

    for i in range(size):
        for j in range(size):
            if (i, j) in placed:
                sys.stdout.write("Q")
            else:
                sys.stdout.write(".")
        print()

    print('-' * size)


def solve_queens(size, row = 0, placed = []):
    if row >= size:
        print_solution(size, placed)
        return True

    for column in range(size):
        cleared=[]
        for queen in placed:
            cleared.append(safe(queen, [row, column]))
        if False not in cleared:
            tmp = solve_queens(size, row + 1, placed + [(row, column)])
            if tmp:
                return tmp

counter = 1

def all_solutions(size, row = 0, placed = []):
    global counter
    if row >= size:
        print("Solution:", counter)
        print_solution(size, placed)
        counter +=1
        return True

    for column in range(size):
        cleared=[]
        for queen in placed:
            cleared.append(safe(queen, [row, column]))
        if False not in cleared:
            all_solutions(size, row + 1, placed + [(row, column)])


class TestBoard(unittest.TestCase):
    def test_safe(self):
        self.assertFalse(safe([0, 0], [1, 1]))
        self.assertFalse(safe([0, 0], [1, 0]))
        self.assertTrue(safe([0, 0], [1, 2]))
        self.assertTrue(safe([0, 0], [2, 1]))

    '''def test_solution(self):
        solve_queens(4)
        solve_queens(5)
        solve_queens(6)
        solve_queens(7)
        solve_queens(8)'''

    def test_solutions(self):
        all_solutions(8)



if '__main__' == __name__:
    unittest.main()
