from interval.ifunctions import inter, i_sqr, i_sqrt, union

"""
    File that contains basic contractors
"""


# contractor a=b+c
def c_add(a, b, c):
    """ :param a (Interval)
        :param b (Interval)
        :param c (Interval)
    """
    return inter(a, b + c), inter(b, a - c), inter(c, a - b)


# contractor a=b*c
def c_mul(a, b, c):
    """ :param a (Interval)
        :param b (Interval)
        :param c (Interval)
    """
    return inter(a, b * c), inter(b, a / c), inter(c, a / b)


# contractor a=b^2
def c_sqr(a, b):
    """ :param a (Interval)
        :param b (Interval)
    """
    return inter(a, b*b), inter(b, i_sqrt(a))
