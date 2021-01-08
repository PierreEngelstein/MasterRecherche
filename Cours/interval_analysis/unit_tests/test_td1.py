import unittest
from interval.interval import Interval
from interval.ifunctions import to_str
from TD1.work2do import evaluate_function, get_min_function


class TestTD1(unittest.TestCase):
    # def evaluate_function(listbox, delta, domain, inclusion_function):
    @staticmethod
    def inclusion_function(x):
        if x.sup <= 4:
            return x
        elif x.inf >= 4:
            return -x+8
        else:
            return Interval(min(x.inf, -x.sup+8), 4)

    def test_evaluate_function(self):
        listbox = []
        domain = [Interval(0, 8), Interval(-float("inf"), float("inf"))]
        evaluate_function(listbox, 8, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 1)
        self.assertEqual(listbox[0][0], Interval(0, 8))
        self.assertEqual(listbox[0][1], Interval(0, 4))

        evaluate_function(listbox, 4, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 2)
        self.assertEqual(listbox[0][0], Interval(0, 4))
        self.assertEqual(listbox[0][1], Interval(0, 4))
        self.assertEqual(listbox[1][0], Interval(4, 8))
        self.assertEqual(listbox[1][1], Interval(0, 4))

        evaluate_function(listbox, 2, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 4)
        self.assertEqual(listbox[0][0], Interval(0, 2))
        self.assertEqual(listbox[0][1], Interval(0, 2))
        self.assertEqual(listbox[1][0], Interval(2, 4))
        self.assertEqual(listbox[1][1], Interval(2, 4))
        self.assertEqual(listbox[2][0], Interval(4, 6))
        self.assertEqual(listbox[2][1], Interval(2, 4))
        self.assertEqual(listbox[3][0], Interval(6, 8))
        self.assertEqual(listbox[3][1], Interval(0, 2))
        print("[TD1] evaluate function OK")

    def test_get_min_function(self):
        # def get_min_function(listbox, delta, domain, inclusion_function):
        listbox = []
        domain = [Interval(0, 8), Interval(-float("inf"), float("inf"))]
        get_min_function(listbox, 8, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 1)
        self.assertEqual(listbox[0][0], Interval(0, 8))
        self.assertEqual(listbox[0][1], Interval(0, 4))

        get_min_function(listbox, 4, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 2)
        self.assertEqual(listbox[0][0], Interval(0, 4))
        self.assertEqual(listbox[0][1], Interval(0, 4))
        self.assertEqual(listbox[1][0], Interval(4, 8))
        self.assertEqual(listbox[1][1], Interval(0, 4))

        get_min_function(listbox, 2, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 4)
        self.assertEqual(listbox[0][0], Interval(0, 2))
        self.assertEqual(listbox[0][1], Interval(0, 2))
        self.assertEqual(listbox[1][0], Interval(2, 4))
        self.assertEqual(listbox[1][1], Interval(2, 4))
        self.assertEqual(listbox[2][0], Interval(4, 6))
        self.assertEqual(listbox[2][1], Interval(2, 4))
        self.assertEqual(listbox[3][0], Interval(6, 8))
        self.assertEqual(listbox[3][1], Interval(0, 2))

        get_min_function(listbox, 1, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 4)
        self.assertEqual(listbox[0][0], Interval(0, 1))
        self.assertEqual(listbox[0][1], Interval(0, 1))
        self.assertEqual(listbox[1][0], Interval(1, 2))
        self.assertEqual(listbox[1][1], Interval(1, 2))
        self.assertEqual(listbox[2][0], Interval(6, 7))
        self.assertEqual(listbox[2][1], Interval(1, 2))
        self.assertEqual(listbox[3][0], Interval(7, 8))
        self.assertEqual(listbox[3][1], Interval(0, 1))

        get_min_function(listbox, 0.5, domain, TestTD1.inclusion_function)
        self.assertEqual(len(listbox), 4)
        self.assertEqual(listbox[0][0], Interval(0, 0.5))
        self.assertEqual(listbox[0][1], Interval(0, 0.5))
        self.assertEqual(listbox[1][0], Interval(0.5, 1))
        self.assertEqual(listbox[1][1], Interval(0.5, 1))
        self.assertEqual(listbox[2][0], Interval(7, 7.5))
        self.assertEqual(listbox[2][1], Interval(1, 0.5))
        self.assertEqual(listbox[3][0], Interval(7.5, 8))
        self.assertEqual(listbox[3][1], Interval(0, 0.5))
        print("[TD1] get min function OK")

