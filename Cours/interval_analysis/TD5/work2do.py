from interval.ifunctions import i_pow, inter, i_sqr, i_r_abs, i_sqrt, size, bisect, union
from interval.interval import Interval
from math import sqrt


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
    center_1 = (8, 8)
    radius_1 = 2
    center_2 = (7, 7)
    radius_2 = 5

    points = [(box[0].inf, box[1].inf), (box[0].inf, box[1].sup), (box[0].sup, box[1].inf), (box[0].sup, box[1].sup)]

    # Get amount of points outside circle 1 and inside circle 2.
    count = 0
    count_inside_circle_1 = 0
    for i in points:
        val_1 = (center_1[0] - i[0])**2 + (center_1[1] - i[1])**2
        val_2 = (center_2[0] - i[0])**2 + (center_2[1] - i[1])**2
        if(val_1 > radius_1**2 and val_2 <= radius_2**2): count+=1
        if(val_1 < radius_1**2): count_inside_circle_1+=1

    # If all 4 points are ok then the box corresponds
    if count == 4: return 1
    # If some points are ok, partial solution
    if count != 0:
        return 0

    # No points inside but have center of circle in the box
    if(center_2[0] >= box[0].inf and center_2[0] <= box[0].sup and center_2[1] >= box[1].inf and center_2[1] <= box[1].sup):
        if count_inside_circle_1 == 4:return -1
        return 0

    # Detect lines that intersect with circle
    a = (radius_2)**2
    length_y1 = sqrt(abs(-(box[1].inf - center_2[1])**2 + a))
    length_y2 = sqrt(abs(-(box[1].sup - center_2[1])**2 + a))
    length_x1 = sqrt(abs(-(box[0].inf - center_2[0])**2 + a))
    length_x2 = sqrt(abs(-(box[0].sup - center_2[0])**2 + a))

    # Inferior vertical line
    if box[1].inf >= center_2[1] - radius_2 and box[1].inf <= center_2[1] + radius_2:
        if box[0].inf <= center_2[0] - length_y1 and box[0].sup >= center_2[0] - length_y1:
            return 0
        if box[0].inf <= center_2[0] + length_y1 and box[0].sup >= center_2[0] + length_y1:
            return 0
        return -1

    # Superior vertical line
    if box[1].sup >= center_2[1] - radius_2 and box[1].sup <= center_2[1] + radius_2:
        if box[0].inf <= center_2[0] - length_y2 and box[0].sup >= center_2[0] - length_y2:
            return 0
        if box[0].inf <= center_2[0] + length_y2 and box[0].sup >= center_2[0] + length_y2:
            return 0
        return -1
    
    # Left horizontal line
    if box[0].inf >= center_2[0] - radius_2 and box[0].inf <= center_2[0] + radius_2:
        if box[1].inf <= center_2[1] - length_x1 and box[1].sup >= center_2[1] - length_x1:
            return 0
        if box[1].inf <= center_2[1] + length_x1 and box[1].sup >= center_2[1] + length_x1:
            return 0
        return -1

    # Right horizontal line 
    if box[0].sup >= center_2[0] - radius_2 and box[0].sup <= center_1[0] + radius_2:
        if box[1].inf <= center_2[1] - length_x2 and box[1].sup >= center_2[1] - length_x2:
            return 0
        if box[1].inf <= center_2[1] + length_x2 and box[1].sup >= center_2[1] + length_x2:
            return 0
        return -1

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
    stop = False
    dst_prev, b1_prev, b2_prev = dst, b1, b2


    # If circle included in box, do nothing
    if (b1[0].inf>b2[0].inf)&(b1[0].sup<b2[0].sup) &(b1[1].inf>b2[1].inf) &(b1[1].sup<b2[1].sup):
        return dst, b1, b2
    iter = 0
    while not stop:
        ## FORWARD
        a = b2[0] - b1[0]
        b = b2[1] - b1[1]
        c = i_sqr(a)
        d = i_sqr(b)
        e_t = c + d
        e_t = inter(e_t, i_sqr(dst))
        e_t = inter(Interval(dst.inf, float("inf")), e_t)

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

    return dst, b1, b2


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
        e_t = inter(Interval(float("-inf"), dst.sup), e_t)

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

    dst, b1, box = c_dst_sup(Interval(2, 2), [Interval(8, 8), Interval(8, 8)], box )
    dst, b2, box = c_dst_inf(Interval(5, 5), [Interval(7, 7), Interval(7, 7)], box )
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

    list_indeterminate
    L = []
    # domain = contract(domain)
    L.append(domain)
    while len(L) != 0:
        val = L.pop()
        val = contract(val)
        ret = test_fct(val)
        if(ret == 1):
            list_solutions.append(val)
        elif(ret == -1):
            list_non_solutions.append(val)
        elif(size(val[0]) < epsilon):
            list_indeterminate.append(val)
        else:
            x1, x2 = bisect(val)
            L.append(x1)
            L.append(x2)
        nb_iterations+=1
    
    print("nb iterations:", nb_iterations)
    print("nb boxes (", len(list_solutions) + len(list_non_solutions) + len(list_indeterminate), "):",
          len(list_solutions), "solutions,", len(list_non_solutions), "non solutions,",
          len(list_indeterminate), "unknown")
    return nb_iterations