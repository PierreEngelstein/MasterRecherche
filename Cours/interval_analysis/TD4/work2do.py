from interval.ifunctions import inter, i_sqr, i_r_abs, i_sqrt, union


# dst:Interval, b1:Box, b2:Box
# contract b1 and b2 according to the euclidean distance dst
def c_dst(dst, b1, b2):
    """
    :param dst: the distance between b1 and b2 (Interval)
    :param b1: a point b1 (Box)
    :param b2: a point b2 (Box)
    :return: updated dst, b1, b2 (Interval, Box, Box)
    """
    stop = False
    dst_prev, b1_prev, b2_prev = dst, b1, b2

    while not stop:
        ## FORWARD
        a = b2[0] - b1[0]
        b = b2[1] - b1[1]
        c = i_sqr(a)
        d = i_sqr(b)
        e_t = c + d
        e_t = inter(e_t, i_sqr(dst))

        ## BACKWARD
        dst = inter(dst, i_sqrt(e_t))
        c = inter(c, e_t-d)
        d = inter(d, e_t-c)
        a = inter(a, union(i_sqrt(c), -i_sqrt(c)))
        b = inter(b, union(i_sqrt(d), -i_sqrt(d)))
        
        b1[0] = inter(b1[0], b2[0] - a)
        b2[0] = inter(b2[0], a + b1[0])
        b1[1] = inter(b1[1], b2[1] - b)
        b2[1] = inter(b2[1], b + b1[1])

        if dst == dst_prev and b1_prev[0] == b1[0] and b1_prev[1] == b1[1] and b2_prev[0] == b2[0] and b2_prev[1] == b2[1]:
            stop = True
        dst_prev, b1_prev, b2_prev = dst, b1, b2

    return dst, b1, b2
