from interval.interval import Interval


class IPose:
    """
        class to handle IPose: x, y, theta
    """

    # constructor
    def __init__(self, x=Interval(), y=Interval(), theta=Interval()):
        """
            Constructor of the IPose class
            
            :param x : the x value of the pose (Interval)
            :param y : the y value of the pose (Interval)
            :param theta : the theta value of the pose (Interval)
        """
        self.x = x
        self.y = y
        self.theta = theta

    def __str__(self):
        """
            Function to be able to print() an IPose
            :return string
        """
        return "( " + str(self.x) + " ; " + str(self.y) + " ; " + str(self.theta) + " ) "
