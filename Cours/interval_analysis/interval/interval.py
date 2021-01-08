import math


class Interval:
    """
        class to handle Intervals
    """

    # constructor
    def __init__(self, inf=0.0, sup=0.0):
        """
            Constructor of the Interval class
            
            :param inf : the inf value of the interval (float)
            :param sup : the sup value of the interval (float)
        """
        if inf > sup:
            tmp = inf
            inf = sup
            sup = tmp
        self.inf = inf
        self.sup = sup

    '''
        handling the basic arithmetic operations over intervals
    '''

    # addition (self + other)
    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.inf + other.inf, self.sup + other.sup)
        else:  # this is an number
            return Interval(self.inf + other, self.sup + other)

    # reverse addition (other + self)
    def __radd__(self, other):
        return self + other

    # negation (-self)
    def __neg__(self):
        return Interval(-self.sup, -self.inf)

    # subtraction (self - other)
    def __sub__(self, other):
        return self + (-other)

    # reverse subtraction (other - self)
    def __rsub__(self, other):
        return other + (-self)

    # Manages multiplication for 0s and inf
    def _mul_inf(self, val1, val2):
        if val1 == 0 and (val2 == float("+inf") or val2 == float("-inf")):
            return 0
        if val2 == 0 and (val1 == float("+inf") or val1 == float("-inf")):
            return 0
        if val1 != 0 and val1 != float("inf") and val1 != float("-inf") and (val2 == float("+inf") or val2 == float("-inf")):
            return val2
        if val2 != 0 and val2 != float("inf") and val2 != float("-inf") and (val1 == float("+inf") or val1 == float("-inf")):
            return val1
        return val1 * val2

    # multiplication (self * other)
    def __mul__(self, other):
        if isinstance(other, Interval):
            vals = []
            vals.append(self._mul_inf(self.inf, other.inf))
            vals.append(self._mul_inf(self.inf, other.sup))
            vals.append(self._mul_inf(self.sup, other.inf))
            vals.append(self._mul_inf(self.sup, other.sup))

            # Get min value
            min = vals[0]
            for i in vals:
                if i < min:
                    min = i

            # get max value
            max = vals[0]
            for i in vals:
                if i > max:
                    max = i
            
            return Interval(min, max)
        else:  # this is an number
            if other < 0:
                return Interval(self._mul_inf(self.sup, other), self._mul_inf(self.inf, other))
            return Interval(self._mul_inf(self.inf, other), self._mul_inf(self.sup, other))

    # reverse multiplication (other * self)
    def __rmul__(self, other):
        return self * other
    
    # reverse division for python 3 (other / self)
    def __rtruediv__(self, other):
        if isinstance(other, Interval):
            return other / self
        else:  # this is an number
            if(self.inf != 0 and self.sup != 0 and (0 < self.inf or 0 > self.sup)):
                return other * Interval(1/self.sup, 1/self.inf)
            if(self.inf != 0 and self.sup != 0 and (0 > self.inf and 0 < self.sup)):
                return Interval(float("-inf"), float("+inf"))
            if(self.inf == 0 and self.sup != 0):
                return Interval(other/other.sup, float("+inf"))
            if(self.inf != 0 and self.sup == 0):
                return Interval(float("-inf"), other/other.inf)
            return Interval()

    # division for python 3 (self / other)
    def __truediv__(self, other):
        if isinstance(other, Interval):
            if(other.inf != 0 and other.sup != 0 and (0 < other.inf or 0 > other.sup)):
                return self * Interval(1/other.sup, 1/other.inf)
            if(other.inf != 0 and other.sup != 0 and (0 > other.inf and 0 < other.sup)):
                return Interval(float("-inf"), float("+inf"))
            if(other.inf == 0 and other.sup != 0):
                return self * Interval(1/other.sup, float("+inf"))
            if(other.inf != 0 and other.sup == 0):
                return self * Interval(float("-inf"), 1/other.inf)
        else:
            if other == 0:
                return Interval(float("-inf"), float("+inf"))
            else:
                return Interval(self.inf/other, self.sup/other)

    # reverse division for python 2 (other / self)
    def __rdiv__(self, other):
        if isinstance(other, Interval):
            return other / self
        else:  # this is an number
            if(self.inf != 0 and self.sup != 0 and (0 < self.inf or 0 > self.sup)):
                return other * Interval(1/self.sup, 1/self.inf)
            if(self.inf != 0 and self.sup != 0 and (0 > self.inf and 0 < self.sup)):
                return Interval(float("-inf"), float("+inf"))
            if(self.inf == 0 and self.sup != 0):
                return Interval(other/other.sup, float("+inf"))
            if(self.inf != 0 and self.sup == 0):
                return Interval(float("-inf"), other/other.inf)
            return Interval()

    # division for python 2 (self / other)
    def __div__(self, other):
        if isinstance(other, Interval):
            if(other.inf != 0 and other.sup != 0 and (0 < other.inf or 0 > other.sup)):
                return self * Interval(1/other.sup, 1/other.inf)
            if(other.inf != 0 and other.sup != 0 and (0 > other.inf and 0 < other.sup)):
                return Interval(float("-inf"), float("+inf"))
            if(other.inf == 0 and other.sup != 0):
                return self * Interval(1/other.sup, float("+inf"))
            if(other.inf != 0 and other.sup == 0):
                return self * Interval(float("-inf"), 1/other.inf)
        else:
            if other == 0:
                return Interval(float("-inf"), float("+inf"))
            else:
                return Interval(self.inf/other, self.sup/other)

    def is_empty(self):
        """
            Function to test if the interval is an empty set or not
            :return boolean value
        """
        return (self.sup != self.sup or self.inf != self.inf)

    def __str__(self):
        """
            Function to be able to print() an Interval
            :return string
        """
        return "[" + "{:.4f}".format(self.inf) + ";" + "{:.4f}".format(self.sup) + "]"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Interval):
            return self.inf == other.inf and self.sup == other.sup
        return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3, just for Python 2)"""
        return not self.__eq__(other)
