from interval.ifunctions import inter, i_sqr, i_r_abs, i_sqrt


# dst:Interval, b1:Box, b2:Box
# contract b1 and b2 according to the euclidean distance dst
def c_dst(dst, b1, b2):
    """
    :param dst: the distance between b1 and b2 (Interval)
    :param b1: a point b1 (Box)
    :param b2: a point b2 (Box)
    :return: updated dst, b1, b2 (Interval, Box, Box)
    """
    # TODO

    return dst, b1, b2
