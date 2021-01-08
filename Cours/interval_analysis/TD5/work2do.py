from interval.ifunctions import i_pow, inter, i_sqr, i_r_abs, i_sqrt, size, bisect
from interval.interval import Interval


def inclusion_test(box):
    # equation of a circle : (xc-x)^2+(yc-y)^2-r^2=0
    # be a circle c1 of radius 2 and center (8,8)
    # be a circle c2 of radius 5 and center (7,7)
    # I want to be outside of the circle c1 but inside the circle c2
    # This function returns 1 if all the points of the box satisfy the constraint
    # This function returns -1 if none of the point of the box satisfies the constraint
    # This function returns 0 otherwise
    """ :param box : the domain we want to test the inclusion on (Box)
        :return -1, 1 or 0 (int)"""
    # TODO
    return -1


# dst:Interval, b1:Box, b2:Box
# contract b1 and b2 according to the euclidean distance dst
# constraint : dst(b1, b2) >= dst
def c_dst_sup(dst, b1, b2):
    """
    :param dst: the minimal distance between b1 and b2 (Interval)
    :param b1: a 2D point (Box)
    :param b2: a 2D point (Box)
    :return: updated dst, b1, b2 (Interval, Box, Box)
    """
    # TODO
    return dst, b1, b2  # dst:Interval, b1:Box, b2:Box


# dst:Interval, b1:Box, b2:Box
# contract b1 and b2 according to the euclidean distance dst
# constraint : dst(b1, b2) <= dst
def c_dst_inf(dst, b1, b2):
    """
    :param dst: the maximal distance between b1 and b2 (Interval)
    :param b1: a 2D point (Box)
    :param b2: a 2D point (Box)
    :return: updated dst, b1, b2 (Interval, Box, Box)
    """
    # TODO
    return dst, b1, b2


def contract(box):
    """
        equation of a circle : (xc-x)^2+(yc-y)^2-r^2=0
        be a circle c1 of radius 2 and center (8,8)
        be a circle c2 of radius 5 and center (7,7)
        I want to be outside of the circle c1 but inside the circle c2
        This means that
           (xc1-x)^2+(yc1-y)^2-r1^2>=0
           (xc2-x)^2+(yc2-y)^2-r2^2<=0
        This function returns the contracted box
    :param box: the box to contract according to the constraint defined previously (Box)
    :return: the updated box (Box)
    """
    # TODO
    return box


def sivia2d(domain, epsilon, list_solutions, list_non_solutions, list_indeterminate, test_fct):
    """
        This function is a Sivia added with contractors: the idea is to contract each box before testing them
    :param domain : the domain we want to compute the inversion on (Box)
    :param epsilon : the smallest size for a box (float)
    :param list_solutions : a list of boxes that are solution of the inversion (list of Box)
    :param list_non_solutions : a list of boxes that are not solution of the inversion (list of Box)
    :param list_indeterminate : a list of boxes that we do not know if they are solution or not (list of Box)
    :param test_fct : The inclusion function test, should receive a box and return
                      1 for included, -1 for not included and 0 for indeterminate
    :return the number of iterations (int)
    """
    # initialization of the current list
    del list_solutions[:]     # list of solution boxes
    del list_non_solutions[:]  # list of non-solution boxes
    del list_indeterminate[:]  # list of unknown boxes
    nb_iterations = 0  # number of iterations for the SIVIA algorithm

    # TODO
    print("nb iterations:", nb_iterations)
    print("nb boxes (", len(list_solutions) + len(list_non_solutions) + len(list_indeterminate), "):",
          len(list_solutions), "solutions,", len(list_non_solutions),
          "non solutions,", len(list_indeterminate), "unknown")
    return nb_iterations
