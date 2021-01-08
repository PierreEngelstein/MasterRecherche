from math import pow, exp
from interval.interval import Interval
from interval.ifunctions import i_sqr, i_exp, bisect


def my_function(x):
    """
    :param x: a number or an interval (float/Interval)
    :return: if x is an interval, the function returns an interval, else it returns a number (float/Interval)
    """
    a = 3
    if isinstance(x, Interval):
        return i_sqr(x) + a * x - i_exp(x)
    else:
        return pow(x, 2)+a*x-exp(x)


# to get a guarantee evaluation of the function f
def evaluate_function(listbox, delta, domain, inclusion_function):
    """
    :param listbox: a list of Intervals, should be updated to contains the evaluation of the function
    :param delta: the smallest for an interval to evaluate the function in (float)
    :param domain: the domain we want to evaluate the function on (Box)
    :param inclusion_function: the inclusion function (a function)
    :return: nothing (directly update the listbox)
    """
    listbox.clear()
    current = domain[0].inf
    while current < domain[0].sup:
        listbox.append([Interval(current, current + delta),  inclusion_function(Interval(current, current+delta))])
        current += delta

# to get an enclosure of the minimum of the function f
def get_min_function(listbox, delta, domain, inclusion_function):
    """
    :param listbox: a list of Intervals, should be updated to contains the minimum of the function
    :param delta: the smallest width for a box in the listbox (float)
    :param domain: the domain we want to find the minimum of the function in (Box)
    :param inclusion_function: the inclusion function (a function)
    :return: nothing (directly update the listbox)
    """
    listbox.clear()
    # Create all the lisboxes
    current = domain[0].inf
    while current < domain[0].sup:
        listbox.append([Interval(current, current + delta),  inclusion_function(Interval(current, current+delta))])
        current += delta
    
    # Remove all listboxes that have other listboxes below them (meaning they are not on the minimum) 
    toremove = []
    for i in range(0, len(listbox)):
        ok = True
        for j in range(0, len(listbox)):
            if j != i:
                if listbox[i][1].inf > listbox[j][1].sup:
                    ok = False
                    break
        if(not ok):
            toremove.append(listbox[i])
    for i in toremove:
        listbox.remove(i)