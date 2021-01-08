from interval.ifunctions import i_pow, size, bisect
from math import sqrt

def inclusion_test(box):
    # equation of a circle : (xc-x)^2+(yc-y)^2-r^2=0
    # be a circle c1 of radius 2 and center (8,8)
    # be a circle c2 of radius 5 and center (7,7)
    # I want to be outside of the circle c1 but inside the circle c2
    # This function returns 1 if all the points of the box satisfy the constraint
    # This function returns -1 if none of the point of the box satisfies the constraint
    # This function returns 0 otherwise
    """ :param box : a list of two intervals (Box)
        :return -1, 1 or 0 (int)
    """
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

def sivia_2d(domain, epsilon, list_solutions, list_non_solutions, list_indeterminate, test_fct):
    """ :param domain : the domain we want to compute the inversion on (Box)
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
    L.append(domain)
    while len(L) != 0:
        val = L.pop()
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
