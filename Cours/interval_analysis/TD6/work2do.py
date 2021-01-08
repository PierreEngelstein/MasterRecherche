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
    x1 = x1_
    y1 = y1_
    x2 = x2_
    y2 = y2_
    # TODO
    return dst, x1, y1, x2, y2


def compute_i_pose(vl, vr):
    """
    :param vl: the left wheel odometry (float)
    :param vr: the right wheel odometry (float)
    :return: nothing, update the gv.I_POSE and gv.I_LANDMARKS global variables
    """
    # TODO
    pass
