import unittest
from interval.interval import Interval
from interval.contractors import c_mul, c_add, c_sqr
import math as math


class TestContractors(unittest.TestCase):
    def test_c_add(self):
        # a = b + c
        a, b, c = c_add(Interval(float("-inf"), float("inf")), Interval(0, 12), Interval(-15, 3))
        self.assertEqual(a, Interval(-15, 15))
        self.assertEqual(b, Interval(0, 12))
        self.assertEqual(c, Interval(-15, 3))
        a, b, c = c_add(Interval(0, 5), Interval(-12, -1), Interval(-15, 3))
        self.assertEqual(a, Interval(0, 2))
        self.assertEqual(b, Interval(-3, -1))
        self.assertEqual(c, Interval(1, 3))
        a, b, c = c_add(Interval(4, 5), Interval(-12, -1), Interval(-15, 3))
        self.assertTrue(math.isnan(a.inf) or math.isnan(a.inf))
        self.assertTrue(math.isnan(b.inf) or math.isnan(b.inf))
        self.assertTrue(math.isnan(c.inf) or math.isnan(c.inf))
        print("[CONTRACTORS] add contractor OK")

    def test_c_mul(self):
        # a = b * c
        a, b, c = c_mul(Interval(float("-inf"), float("inf")), Interval(0, 12), Interval(-15, 3))
        self.assertEqual(a, Interval(-180, 36))
        self.assertEqual(b, Interval(0, 12))
        self.assertEqual(c, Interval(-15, 3))
        a, b, c = c_mul(Interval(0, 5), Interval(-12, -1), Interval(-15, 3))
        self.assertEqual(a, Interval(0, 5))
        self.assertEqual(b, Interval(-12, -1))
        self.assertEqual(c, Interval(-5, 0))
        a, b, c = c_mul(Interval(3, 7), Interval(3, 7), Interval(-1, 0))
        self.assertTrue(math.isnan(a.inf) or math.isnan(a.inf))
        self.assertTrue(math.isnan(b.inf) or math.isnan(b.inf))
        self.assertTrue(math.isnan(c.inf) or math.isnan(c.inf))
        a, b, c = c_mul(Interval(3, 7), Interval(3, 7), Interval(-1, 3))
        self.assertEqual(a, Interval(3, 7))
        self.assertEqual(b, Interval(3, 7))
        self.assertAlmostEqual(c.inf, 0.4286, 3)
        self.assertAlmostEqual(c.sup, 2.3333, 3)
        a, b, c = c_mul(Interval(float("-inf"), 3), Interval(2, float("inf")), Interval(1, 3))
        self.assertEqual(a, Interval(2, 3))
        self.assertEqual(b, Interval(2, 3))
        self.assertEqual(c, Interval(1, 1.5))
        print("[CONTRACTORS] mul contractor OK")

    def test_c_sqr(self):
        # a = b^2
        a, b = c_sqr(Interval(float("-inf"), float("inf")), Interval(0, 12))
        self.assertEqual(a, Interval(0, 144))
        self.assertEqual(b, Interval(0, 12))
        a, b = c_sqr(Interval(float("-inf"), float("inf")), Interval(float("-inf"), 12))
        self.assertEqual(a, Interval(0, float("inf")))
        self.assertEqual(b, Interval(float("-inf"), 12))
        a, b = c_sqr(Interval(3, 4), Interval(float("-inf"), float("inf")))
        self.assertEqual(a, Interval(3, 4))
        self.assertEqual(b, Interval(-2, 2))
        a, b = c_sqr(Interval(-2, -1), Interval(float("-inf"), float("inf")))
        self.assertTrue(math.isnan(a.inf) or math.isnan(a.inf))
        self.assertTrue(math.isnan(b.inf) or math.isnan(b.inf))
        print("[CONTRACTORS] sqr contractor OK")

