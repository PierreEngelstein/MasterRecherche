import unittest
import math
from math import pi as pi
from interval.interval import Interval
from interval.ifunctions import *


class TestIFunctions(unittest.TestCase):
    def test_normalize_i_angle(self):
        res = normalize_i_angle(Interval(float("nan"), 3))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        res = normalize_i_angle(Interval(3, float("nan")))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        res = normalize_i_angle(Interval(-pi, 0))
        self.assertAlmostEqual(res.inf, pi, 5)
        self.assertAlmostEqual(res.sup, 2*pi, 5)
        res = normalize_i_angle(Interval(-pi, pi))
        self.assertAlmostEqual(res.inf, 0, 5)
        self.assertAlmostEqual(res.sup, 2*pi, 5)
        res = normalize_i_angle(Interval(-15*pi, 0))
        self.assertAlmostEqual(res.inf, 0, 5)
        self.assertAlmostEqual(res.sup, 2*pi, 5)
        res = normalize_i_angle(Interval(-pi/2, pi/2))
        self.assertAlmostEqual(res.inf, pi + pi/2, 5)
        self.assertAlmostEqual(res.sup, 2*pi + pi/2, 5)
        res = normalize_i_angle(Interval(-pi/2, 0))
        self.assertAlmostEqual(res.inf, pi + pi/2, 5)
        self.assertAlmostEqual(res.sup, 2*pi, 5)
        res = normalize_i_angle(Interval(pi/2, 2*pi/2))
        self.assertAlmostEqual(res.inf, pi/2, 5)
        self.assertAlmostEqual(res.sup, 2*pi/2, 5)
        res = normalize_i_angle(Interval(0, pi))
        self.assertAlmostEqual(res.inf, 0, 5)
        self.assertAlmostEqual(res.sup, pi, 5)
        print("[iFUNCTIONS] normalize angle OK")

    def test_i_cos(self):

        res = i_cos(Interval(pi - pi/5, pi + pi/3))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, -0.5, 5)
        res = i_cos(Interval(3*pi/3 - pi/5, 3*pi/3 + pi/5))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, -0.809017, 5)
        res = i_cos(Interval(pi - pi/5, pi + pi/5))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, -0.809017, 5)
        res = i_cos(Interval(2*pi - pi/5, 2*pi + pi/5))
        self.assertAlmostEqual(res.inf, 0.809017, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        res = i_cos(Interval(4*pi - pi/5, 4*pi + pi/5))
        self.assertAlmostEqual(res.inf, 0.809017, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        res = i_cos(Interval(0, 2*pi))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        res = i_cos(Interval(0.5, 7.0))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, 1, 5)

        print("[iFUNCTIONS] cos OK")

    def test_i_sin(self):
        res = i_sin(Interval(pi/2 - pi / 5, pi/2 + pi / 3))
        self.assertAlmostEqual(res.inf, 0.5, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        res = i_sin(Interval(5*pi/2 - pi / 5, 5*pi/2 + pi / 3))
        self.assertAlmostEqual(res.inf, 0.5, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        res = i_sin(Interval(3*pi/2 - pi / 5, 3*pi/2 + pi / 3))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, -0.5, 5)
        res = i_sin(Interval(7*pi/2 - pi / 5, 7*pi/2 + pi / 3))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, -0.5, 5)
        res = i_sin(Interval(0, 2*pi))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        res = i_sin(Interval(0.5, 7.0))
        self.assertAlmostEqual(res.inf, -1, 5)
        self.assertAlmostEqual(res.sup, 1, 5)
        print("[iFUNCTIONS] sin OK")

    def test_get_rand_value_in(self):
        i_vector = [Interval(-5, 5), Interval(5, 10), Interval(-10, -5)]
        for i in i_vector:
            for _ in range(0, 50):
                i_rand = get_rand_value_in(i)
                self.assertTrue(i.inf < i_rand < i.sup)
        print("[iFUNCTIONS] get rand value in OK")

    def test_mid(self):
        self.assertAlmostEqual(mid(Interval(-5, 5)), 0, 5)
        self.assertAlmostEqual(mid(Interval(-5, 4)), -0.5, 5)
        self.assertAlmostEqual(mid(Interval(-5, -3)), -4, 5)
        self.assertAlmostEqual(mid(Interval(7, 12)), 9.5, 5)
        print("[iFUNCTIONS] mid OK")

    def test_i_sqr(self):
        res = i_sqr(Interval(2, 4))
        self.assertAlmostEqual(res.inf, 4, 5)
        self.assertAlmostEqual(res.sup, 16, 5)
        res = i_sqr(Interval(-4, -2))
        self.assertAlmostEqual(res.inf, 4, 5)
        self.assertAlmostEqual(res.sup, 16, 5)
        res = i_sqr(Interval(-4, 2))
        self.assertAlmostEqual(res.inf, 0, 5)
        self.assertAlmostEqual(res.sup, 16, 5)
        res = i_sqr(Interval(-2, 5))
        self.assertAlmostEqual(res.inf, 0, 5)
        self.assertAlmostEqual(res.sup, 25, 5)
        print("[iFUNCTIONS] sqr OK")

    def test_i_exp(self):
        res = i_exp(Interval(3, 5))
        self.assertAlmostEqual(res.inf, 20.0855, 4)
        self.assertAlmostEqual(res.sup, 148.4132, 4)
        res = i_exp(Interval(-3, 5))
        self.assertAlmostEqual(res.inf, 0.0498, 4)
        self.assertAlmostEqual(res.sup, 148.4132, 4)
        res = i_exp(Interval(-5, -3))
        self.assertAlmostEqual(res.inf, 0.0067, 4)
        self.assertAlmostEqual(res.sup, 0.0498, 4)
        res = i_exp(Interval(float("-inf"), -3))
        self.assertAlmostEqual(res.inf, 0, 4)
        self.assertAlmostEqual(res.sup, 0.0498, 4)
        print("[iFUNCTIONS] exp OK")

    def test_i_sqrt(self):
        res = i_sqrt(Interval(-3, -1))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        res = i_sqrt(Interval(-3, 0))
        self.assertAlmostEqual(res.inf, 0, 4)
        self.assertAlmostEqual(res.sup, 0, 4)
        res = i_sqrt(Interval(-3, 3))
        self.assertAlmostEqual(res.inf, 0, 4)
        self.assertAlmostEqual(res.sup, 1.7321, 4)
        res = i_sqrt(Interval(0, 5))
        self.assertAlmostEqual(res.inf, 0, 4)
        self.assertAlmostEqual(res.sup, 2.2361, 4)
        res = i_sqrt(Interval(7, 12))
        self.assertAlmostEqual(res.inf, 2.6458, 4)
        self.assertAlmostEqual(res.sup, 3.4641, 4)
        res = i_sqrt(Interval(7, float("inf")))
        self.assertAlmostEqual(res.inf, 2.6458, 4)
        self.assertAlmostEqual(res.sup, float("inf"), 4)
        print("[iFUNCTIONS] sqrt OK")

    def test_i_r_abs(self):
        i = Interval(2, 3)
        res = i_r_abs(i)
        self.assertEqual(len(res), 2)
        self.assertTrue(res[0].inf == i.inf and res[0].sup == i.sup and res[1].inf == -i.sup and res[1].sup == -i.inf or
                        res[1].inf == i.inf and res[1].sup == i.sup and res[0].inf == -i.sup and res[0].sup == -i.inf)
        i = Interval(2, float("inf"))
        res = i_r_abs(i)
        self.assertEqual(len(res), 2)
        self.assertTrue(res[0].inf == i.inf and res[0].sup == i.sup and res[1].inf == -i.sup and res[1].sup == -i.inf or
                        res[1].inf == i.inf and res[1].sup == i.sup and res[0].inf == -i.sup and res[0].sup == -i.inf)
        i = Interval(-3, float("inf"))
        res = i_r_abs(i)
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0].inf, 0, 5)
        self.assertAlmostEqual(res[0].sup, float("inf"), 5)
        self.assertAlmostEqual(res[1].inf, -float("inf"), 5)
        self.assertAlmostEqual(res[1].sup, 0, 5)
        i = Interval(-3, -2)
        res = i_r_abs(i)
        self.assertEqual(len(res), 2)
        self.assertTrue(math.isnan(res[0].inf) and math.isnan(res[0].sup) and
                        math.isnan(res[1].inf) and math.isnan(res[1].sup))
        print("[iFUNCTIONS] reverse absolute OK")

    def test_inter(self):
        res = inter(Interval(1, 2), Interval(3, 4))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        res = inter(Interval(1, 2), Interval(-4, -3))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        res = inter(Interval(1, 5), Interval(2, 7))
        self.assertEqual(res, Interval(2, 5))
        res = inter(Interval(1, 5), Interval(-3, 2))
        self.assertEqual(res, Interval(1, 2))
        res = inter(Interval(1, 5), Interval(2, 3))
        self.assertEqual(res, Interval(2, 3))

        res = inter(Interval(1, 5), [Interval(2, 3), Interval(5, 7)])
        self.assertEqual(res, Interval(2, 5))
        res = inter(Interval(1, 4), [Interval(2, 3), Interval(5, 7)])
        self.assertEqual(res, Interval(2, 3))
        res = inter(Interval(4, 8), [Interval(2, 3), Interval(5, 7)])
        self.assertEqual(res, Interval(5, 7))
        res = inter(Interval(1, 9), [Interval(2, 3), Interval(5, 7)])
        self.assertEqual(res, Interval(2, 7))
        res = inter(Interval(4, 4), [Interval(2, 3), Interval(5, 7)])
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))

        res = inter([Interval(5, 7), Interval(2, 3)], Interval(1, 5))
        self.assertEqual(res, Interval(2, 5))
        res = inter([Interval(5, 7), Interval(2, 3)], Interval(1, 4))
        self.assertEqual(res, Interval(2, 3))
        res = inter([Interval(5, 7), Interval(2, 3)], Interval(4, 8))
        self.assertEqual(res, Interval(5, 7))
        res = inter([Interval(5, 7), Interval(2, 3)], Interval(1, 9))
        self.assertEqual(res, Interval(2, 7))
        res = inter([Interval(5, 7), Interval(2, 3)], Interval(4, 4))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))

        res = inter([Interval(5, 7), Interval(2, 4)],
                    [Interval(3, 6), Interval(1, 3)])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], Interval(5, 6))
        self.assertEqual(res[1], Interval(2, 3))

        res = inter([Interval(5, 7), Interval(2, 4)],
                    [Interval(3, 4), Interval(1, 3)])
        self.assertEqual(len(res), 2)
        self.assertTrue(math.isnan(res[0].inf))
        self.assertTrue(math.isnan(res[0].sup))
        self.assertEqual(res[1], Interval(2, 3))

        res = inter([Interval(5, 7), Interval(7, 10)],
                    [Interval(6, 9), Interval(4, 6)])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0], Interval(6, 7))
        self.assertTrue(math.isnan(res[1].inf))
        self.assertTrue(math.isnan(res[1].sup))

        res = inter(Interval(6, 9), Interval(4, float("nan")))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))

        res = inter(Interval(float("nan"), 9), Interval(4, 10))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        print("[iFUNCTIONS] inter OK")

    def test_size(self):
        res = size(Interval(3, 7))
        self.assertEqual(res, 4)
        res = size(Interval(-7, -3))
        self.assertEqual(res, 4)
        res = size(Interval(-7, 3))
        self.assertEqual(res, 10)
        res = size(Interval(-7, float("inf")))
        self.assertEqual(res, float("inf"))
        print("[iFUNCTIONS] size OK")

    def test_union(self):
        res = union(Interval(2, 7), Interval(3, 5))
        self.assertEqual(res, Interval(2, 7))
        res = union(Interval(-3, -2), Interval(9, 12))
        self.assertEqual(res, Interval(-3, 12))
        res = union(Interval(-float("inf"), -2), Interval(9, 12))
        self.assertEqual(res, Interval(-float("inf"), 12))
        res = union(Interval(-float("nan"), -2), Interval(9, 12))
        self.assertEqual(res, Interval(9, 12))
        res = union(Interval(9, 12), Interval(-float("nan"), -2))
        self.assertEqual(res, Interval(9, 12))
        res = union(Interval(-float("inf"), -2), Interval(9, float("inf")))
        self.assertEqual(res, Interval(-float("inf"), float("inf")))
        print("[iFUNCTIONS] union OK")

    def test_i_pow(self):
        res = i_pow(Interval(2, 7), 1)
        self.assertAlmostEquals(res.inf, 2, 5)
        self.assertEqual(res.sup, 7, 5)
        res = i_pow(Interval(2, 7), 4)
        self.assertAlmostEquals(res.inf, 16, 5)
        self.assertEqual(res.sup, 2401, 5)
        res = i_pow(Interval(-7, -2), 4)
        self.assertAlmostEquals(res.inf, 16, 5)
        self.assertEqual(res.sup, 2401, 5)
        res = i_pow(Interval(-2, 7), 4)
        self.assertAlmostEquals(res.inf, 0, 5)
        self.assertEqual(res.sup, 2401, 5)
        res = i_pow(Interval(-2, 7), 3)
        self.assertAlmostEquals(res.inf, -8, 5)
        self.assertEqual(res.sup, 343, 5)
        res = i_pow(Interval(-2, 7), 6)
        self.assertAlmostEquals(res.inf, 0, 5)
        self.assertEqual(res.sup, 117649, 5)
        print("[iFUNCTIONS] pow OK")

    def test_inter_angle(self):
        res = inter_angle(Interval(pi/4, pi/3), Interval(pi+pi/4, pi+pi/3))
        self.assertTrue(math.isnan(res.inf))
        self.assertTrue(math.isnan(res.sup))
        res = inter_angle(Interval(pi/4, pi/3), Interval(2*pi+pi/4, 2*pi+pi/3.5))
        self.assertAlmostEquals(res.inf, pi/4, 5)
        self.assertAlmostEquals(res.sup, pi/3.5, 5)
        res = inter_angle(Interval(pi/2, pi+pi/2), Interval(2*pi/3, pi+pi/3))
        self.assertAlmostEquals(res.inf, 2*pi/3, 5)
        self.assertAlmostEquals(res.sup, pi+pi/3, 5)
        res = inter_angle(Interval(2*pi/3, 2*pi+pi/3), Interval(0, pi/2))
        self.assertAlmostEquals(res.inf, 0, 5)
        self.assertAlmostEquals(res.sup, pi/3, 5)
        res = inter_angle(Interval(pi/2, 5*pi/2), Interval(3*pi/2, 4*pi))
        self.assertAlmostEquals(res.inf, 0, 5)
        self.assertAlmostEquals(res.sup, 2*pi, 5)
        print("[iFUNCTIONS] inter angle OK")
        pass

    def test_bisect(self):
        res = bisect(Interval(4, 6))
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0].inf, 4, 4)
        self.assertAlmostEqual(res[0].sup, 5, 4)
        self.assertAlmostEqual(res[1].inf, 5, 4)
        self.assertAlmostEqual(res[1].sup, 6, 4)
        res = bisect(Interval(-6, -4))
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0].inf, -6, 4)
        self.assertAlmostEqual(res[0].sup, -5, 4)
        self.assertAlmostEqual(res[1].inf, -5, 4)
        self.assertAlmostEqual(res[1].sup, -4, 4)
        res = bisect(Interval(-6, 3))
        self.assertEqual(len(res), 2)
        self.assertAlmostEqual(res[0].inf, -6, 4)
        self.assertAlmostEqual(res[0].sup, -1.5, 4)
        self.assertAlmostEqual(res[1].inf, -1.5, 4)
        self.assertAlmostEqual(res[1].sup, 3, 4)
        res = bisect([Interval(-6, 3), Interval(2, 3)])
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 2)
        self.assertEqual(len(res[1]), 2)
        self.assertAlmostEqual(res[0][0].inf, -6, 4)
        self.assertAlmostEqual(res[0][0].sup, -1.5, 4)
        self.assertAlmostEqual(res[0][1].inf, 2, 4)
        self.assertAlmostEqual(res[0][1].sup, 3, 4)
        self.assertAlmostEqual(res[1][0].inf, -1.5, 4)
        self.assertAlmostEqual(res[1][0].sup, 3, 4)
        self.assertAlmostEqual(res[1][1].inf, 2, 4)
        self.assertAlmostEqual(res[1][1].sup, 3, 4)
        res = bisect([Interval(-6, 3), Interval(0, 10)])
        self.assertEqual(len(res), 2)
        self.assertEqual(len(res[0]), 2)
        self.assertEqual(len(res[1]), 2)
        self.assertAlmostEqual(res[0][0].inf, -6, 4)
        self.assertAlmostEqual(res[0][0].sup, 3, 4)
        self.assertAlmostEqual(res[0][1].inf, 0, 4)
        self.assertAlmostEqual(res[0][1].sup, 5, 4)
        self.assertAlmostEqual(res[1][0].inf, -6, 4)
        self.assertAlmostEqual(res[1][0].sup, 3, 4)
        self.assertAlmostEqual(res[1][1].inf, 5, 4)
        self.assertAlmostEqual(res[1][1].sup, 10, 4)

        print("[iFUNCTIONS] bisect OK")
