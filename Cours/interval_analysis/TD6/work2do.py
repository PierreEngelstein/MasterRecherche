import TD6.global_variables as gv
from interval.ifunctions import *
from interval.interval import Interval


# dst:Interval, b1:Box, b2:Box
def c_dst(dst, x1_, y1_, x2_, y2_):
    """
    :param dst: the distance between point 1 and point 2 (Interval)
    :param x1_: the x coordinate of point 1 (Interval)
    :param y1_: the y coordinate of point 1 (Interval)
    :param x2_: the x coordinate of point 2 (Interval)
    :param y2_: the y coordinate of point 2 (Interval)
    :return: updated dst, x1, y1, x2, y2 (Interval, Interval, Interval, Interval, Interval)
    """
    print("in c_dst")
    x1 = x1_
    y1 = y1_
    x2 = x2_
    y2 = y2_

    b1 = [x1, y1]
    b2 = [x2, y2]

    stop = False
    dst_prev, b1_prev, b2_prev = dst, b1, b2
    iter = 0
    while not stop:
        ## FORWARD
        a = b2[0] - b1[0]
        b = b2[1] - b1[1]
        c = i_sqr(a)
        d = i_sqr(b)
        e_t = c + d
        e_t = inter(e_t, i_sqr(dst))
        e_t = inter(e_t, Interval(float("-inf"), dst.sup))

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
        iter += 1
        if iter > 20:
            stop = True
    return dst, b1[0], b1[1], b2[0], b2[0]


def compute_i_pose(vl, vr):
    """
    :param vl: the left wheel odometry (float)
    :param vr: the right wheel odometry (float)
    :return: nothing, update the gv.I_POSE and gv.I_LANDMARKS global variables
    """
    _vl = vl
    _vr = vr

    length = Interval(gv.ROBOT.get_l() - gv.ROBOT.get_l_error(), gv.ROBOT.get_l() + gv.ROBOT.get_l_error())
    vl = Interval(_vl - gv.ROBOT.get_drift(), _vl + gv.ROBOT.get_drift())
    vr = Interval(_vr - gv.ROBOT.get_drift(), _vr + gv.ROBOT.get_drift())
    theta = Interval(gv.ROBOT.get_compass() - gv.ROBOT.get_error_compass(), gv.ROBOT.get_compass() + gv.ROBOT.get_error_compass())
    # theta = gv.I_POSE.theta

    w = (vr - vl)/length
    r = (length / 2) * (vr + vl)/(vr - vl)
    ICCX = gv.ROBOT._x - r * i_sin(theta)
    ICCY = gv.ROBOT._y + r * i_cos(theta)

    x = gv.I_POSE.x
    y = gv.I_POSE.y

    coswdt = i_cos(w * gv.ROBOT.get_delta_t())
    sinwdt = i_sin(w * gv.ROBOT.get_delta_t())

    i1 = x * coswdt
    i2 = y * sinwdt
    i_1 = x * sinwdt
    i_2 = y * coswdt
    i3 = i_sin(theta)
    i4 = i_cos(theta)

    i5 = i3 * r
    i6 = x - i5 # ICCX
    i7 = i4 * r
    i8 = y + i7 # ICCY
    i9 = coswdt * i6
    i10 = sinwdt * i8
    i11 = sinwdt * i6
    i12 = coswdt * i8
    i13 = i1 - i9 - i2 + i10 + i6 # x'
    i14 = i2 - i11 + i_2 - i12 + i8 # y'

    print(gv.I_POSE.x, x, i13)

    gv.I_POSE.x = i13
    gv.I_POSE.y = i14

    # TODO
    pass
