from math import pow, exp, sqrt, pi, sin, cos, isnan
import math
from interval.interval import Interval
import random as rd

"""
    File that contains useful functions to deal with intervals and boxes
    note that a box corresponds to a list (vector) of two intervals
"""


def normalize_i_angle(angle):
    """
        Function to normalize an interval angle as following:
            - value between 0 and 720 (actually 0 and 4*pi)
            - the lower value of the interval angle must be lower than 360 (2*pi)
            - the difference between the lower and upper bound must be lower that 360 (2*pi)
        :param angle: the angle we want to normalize (an interval)
        :return : normalized angle (Interval)
    """
    if isinstance(angle, Interval):
        if math.isnan(angle.inf) or math.isnan(angle.sup):
            return Interval(float('nan'), float('nan'))
        if angle.sup < 0 and angle.inf < 0:
            diff = abs(angle.inf) - abs(angle.sup)
        else:
            diff = abs(angle.sup - angle.inf)

        if diff >= 2*pi:
            return Interval(0, 2*pi)
        elif diff != diff % (2*pi):
            print(Interval(angle.inf % (2*pi), angle.sup % (2*pi)))
            return angle
        else:
            if angle.inf < 0:
                return Interval(angle.inf + 2*pi, angle.sup + 2*pi)
            if angle.inf > 0:
                return angle
        return angle
    return None


def i_cos(angle):
    """
        Function to compute the cos value of an interval angle
        :param angle: the interval angle we want the cos of (Interval)
        :return : interval cos value (float)
    """
    if isinstance(angle, Interval):
        if size(angle) >= 2*pi:
            return Interval(-1, 1)
        val_cos_inf = cos(angle.inf)
        val_cos_sup = cos(angle.sup)

        if angle.inf >= pi:
            return -i_cos(angle - pi)
                
        if angle.sup <= pi:
            return Interval(val_cos_inf, val_cos_sup)

        if angle.sup <= 2*pi:
            return Interval(-1, max(val_cos_inf, val_cos_sup))

        return Interval(-1, 1)
    else:
        print(f"i_cos is not defined for {type(angle)}")
        return None


def i_sin(angle):
    """
        Function to compute the sin value of an interval angle
        :param angle: the interval angle we want the sin of (Interval)
        :return : interval sin value (float)
    """
    if isinstance(angle, Interval):
        angle = angle - pi/2
        angle = normalize_i_angle(angle)
        return i_cos(angle)
    else:
        print(f"i_sin is not defined for {type(angle)}")
        return None


def get_rand_value_in(interval):
    """
        Function that provides a random value inside an interval
        :param interval : the interval from which we want the value (Interval)
        :return the random value (float)
    """
    
    return rd.random() * (interval.sup - interval.inf) + interval.inf


def mid(interval):
    """
        Function that computes the middle value of an interval
        :param interval : the interval from which we want the middle value (Interval)
        :return the middle value (float)
    """
    
    return (interval.sup - interval.inf)/2 + interval.inf


def i_sqr(interval):
    """
        Function that computes the inclusion function of the square of an interval
        :param interval : the interval we want to square (i**2) (Interval)
        :return the square value of the interval
    """
    if isinstance(interval, Interval):
        return i_pow(interval, 2)
    else:
        print(f"i_sqr is not defined for {type(interval)}")
        return None

# inclusion function for exponential of an interval
def i_exp(interval):
    if isinstance(interval, Interval):
        return Interval(exp(interval.inf), exp(interval.sup))
    else:
        print(f"i_exp is not defined for {type(interval)}")
        return None


def i_sqrt(interval):
    """
        Function that computes the inclusion function of the squareRoot of an interval
        :param interval : the interval we want to squared root (Interval)
        :return the squared root value of the interval
    """
    if isinstance(interval, Interval):
        min = 0
        if interval.inf >= 0:
            min = sqrt(interval.inf)
        if interval.sup < 0:
            return Interval(float("nan"), float("nan"))
        return Interval(min, sqrt(interval.sup))
    else:
        print(f"i_sqrt is not defined for {type(interval)}")
        return None


def i_r_abs(interval):
    """
        Function that computes the inverse of the absolute function
        :param interval : the interval we want to compute the abs^-1 (Interval)
        :return the inverse of the absolute value (Box)
    """
    # if(interval.inf >= 0):
    #     return [Interval(float("-inf"), interval.inf), Interval(interval.sup, float("+inf"))]
    # if(interval.sup <= 0):
    #     return [Interval(float("-inf"), -interval.sup), Interval(-interval.inf, float("+inf"))]
    # return [Interval(float("-inf"), 0), Interval(max(-interval.inf, interval.sup), float("+inf"))]

    if interval.inf < 0 and interval.sup < 0:
        return [Interval(float("nan"), float("nan")), Interval(float("nan"), float("nan"))]
    if interval.inf < 0 and interval.sup > 0:
        return [Interval(0, interval.sup), Interval(-interval.sup, 0)]

    return [Interval(interval.inf, interval.sup), Interval(-interval.sup, -interval.inf)]


def inter(i1, i2):
    """
        Function that computes the intersection between box/interval and box/interval
        :param i1 : the first box/interval we want to compute the intersection (Box/Interval)
        :param i2 : the second box/interval we want to compute the intersection (Box/Interval)
        :return the intersection of i1 and i2 (Box/Interval)
    """
    if isinstance(i1, Interval) and isinstance(i2, Interval):
        if((math.isnan(i2.inf) or math.isnan(i2.sup)) or (math.isnan(i1.inf) or math.isnan(i1.sup))):
            return Interval(float("nan"), float("nan"))
        if i1.sup < i2.inf or i2.sup < i1.inf:
            return Interval(float("nan"), float("nan"))
        return Interval(max(i1.inf, i2.inf), min(i1.sup, i2.sup))
    elif isinstance(i1, Interval) and isinstance(i2, list):
        list_inter = []
        for i in i2:
            list_inter.append(inter(i1, i))
        val = None
        for i in range(0, len(list_inter)):
            if val is None:
                val = list_inter[i]
            else:
                val = union(val, list_inter[i])
        return val
        
    elif isinstance(i1, list) and isinstance(i2, Interval):
        return inter(i2, i1)
    elif isinstance(i1, list) and isinstance(i2, list):
        inter_1 = inter(i1[0], i2[0])
        inter_2 = inter(i1[1], i2[1])
        return [inter_1, inter_2]
    else:
        print(f"inter is not defined for {type(i1)} and {type(i2)}")
        return None


def inter_angle(a1, a2):
    """
        Function that computes the intersection between box/interval angle and box/interval angle
        :param a1 : the first box/interval angle we want to compute the intersection of (Box/Interval)
        :param a2 : the second box/interval angle we want to compute the intersection of (Box/Interval)
        :return the intersection of a1 and a2 (Box/Interval)
    """
    if isinstance(a1, Interval) and isinstance(a2, Interval):
        angle1 = normalize_i_angle(a1)
        angle2 = normalize_i_angle(a2)
        return normalize_i_angle(inter(angle1, angle2))
    else:
        print(f"inter_angle  is not defined between {a1.__class__.__name__} and {a2.__class__.__name__}")
        return None


def union(i1, i2):
    """
        Function that computes the union of two intervals
        :param i1 : the first interval we want to compute the union (Interval)
        :param i2 : the second interval we want to compute the union (Interval)
        :return the union of the intervals (Interval)
    """
    if(isnan(i1.inf) or isnan(i1.sup)):
        return i2
    if(isnan(i2.inf) or isnan(i2.sup)):
        return i1
    return Interval(min(i1.inf, i2.inf), max(i1.sup, i2.sup))


# function that bisect an interval or a box
# the bisection of the box is always done over the first dimension i1
def bisect(val):
    if isinstance(val, Interval):
        return Interval(val.inf, val.inf + size(val)/2), Interval(val.inf + size(val)/2, val.sup)
    elif isinstance(val, list):
        if(size(val[0]) > size(val[1])):
            return [Interval(val[0].inf, val[0].inf + size(val[0])/2), val[1]], [Interval(val[0].inf + size(val[0])/2, val[0].sup), val[1]]
        else:
            return [val[0], Interval(val[1].inf, val[1].inf + size(val[1])/2)], [val[0], Interval(val[1].inf + size(val[1])/2, val[1].sup)]
    else:
        print("this is neither a box nor an interval")


def size(interval):
    """
        Function that computes the size of an interval
        :param interval : the interval we want to compute the size
        :return the size of the interval (float)
    """
    return interval.sup - interval.inf


def i_pow(interval, power):
    """
        Function that computes the power of an interval
        :param interval : the interval we want to compute the power of (Interval)
        :param power : the value of the power (integer >= 0)
        :return the power of the interval (Interval)
    """
    if power == 0:
        if interval.inf == 0 and interval.sup == 0:
            return Interval(float("nan"), float("nan"))
        else:
            return Interval(0, 0)
    if(power == 1):
        return interval
    if(power < 0):
        return interval
    
    if power % 2 == 0:
        if interval.sup < 0:
            return Interval((-interval.inf)**power, (-interval.sup)**power)
        elif interval.inf < 0:
            return Interval(0, (max(-interval.inf, interval.sup))**power)
        else:
            return Interval(interval.inf**power, interval.sup**power)
    else:
        if interval.sup < 0:
            return Interval((interval.sup)**power, (interval.inf)**power)
        elif interval.inf < 0:
            return Interval(-(-interval.inf)**power, (interval.sup)**power)
        else:
            return Interval((interval.inf)**power, (interval.sup)**power)

def to_str(var):
    """
        Function that concert a Interval, a box or a list of boxes into a string, to be able to display it
        :param var : an Interval, a Box or a list of Boxes
        :return the string corresponding to var (string)
    """
    if isinstance(var, Interval):
        return str(var)
    elif isinstance(var, list):
        if isinstance(var[0], list):
            msg = ""
            for b in var:
                msg += to_str(b) + "\n"
            return msg
        else:
            return f"[ {to_str(var[0])}, {to_str(var[1])} ]"
    print("this is neither a box nor an interval")
    return NotImplemented
