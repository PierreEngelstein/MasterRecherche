import random as rd
from math import *

""" You do not need to modify this file """


class Robot:
    """
        Class that simulate a two wheeled differential robot

        The considered cinematic model:
        |   x'   |   | cos(wdt)  -sin(wdt)  0 |   | x-ICCx |   | ICCx |
        |   y'   | = | sin(wdt)   cos(wdt)  0 | * | y-ICCy | + | ICCy |
        | theta' |   |     0          0     1 |   | theta  |   |  wdt |

        with:
            dt = the time step

            | ICCx | = | x-R.sin(theta) |
            | ICCy |   | y+R.cos(theta) |

            R = (l/2) * (Vl+Vr)/(Vr-Vl)
            w = (Vr-Vl)/l
            Vl and Vr :  the left and right wheel velocity
            l : the space between the wheels
    """

    def __init__(self):
        """
            Constructor of the Robot class

            _l : distance between the two wheels
            _l_known : the known value of the distance between the wheels
            _errL : imprecision over the _l value
            _x : x position of the robot
            _y : y position of the robot
            _theta : orientation of the robot
            _Vl : left wheel velocity
            _Vr : right wheel velocity
            _V_max : the wheels max speed
            _delta_t : time step between two positions updates
            _drift : drifting error (diff between command speed and real speed)
            _odometry : the computed moved distance in direct line
            _compass : orientation of the robot calculated using a compass with _errCompass precision
            _errOdo : the error of the _odometry value
            _errCompass : the error over the compass value
            _deltaTargetOrientation : min delta between the robot orientation
                                      and the target direction (for autonomous navigation)
        """
        self._errL = 5.0
        self._l_known = 200.0
        self._l = self._l_known + rd.uniform(0, 2 * self._errL) - self._errL
        self._x = 0.0
        self._y = 0.0
        self._theta = 0
        self._Vl = 0.0
        self._Vr = 0.0
        self._V_max = 0.0
        self._delta_t = 1.0
        self._drift = 1.0
        self._odometry = 0
        self._compass = 0
        self._errOdo = 0
        self._errCompass = 1 * pi / 180
        self._deltaTargetOrientation = 0.1

    def get_drift(self):
        """ return the _drift value (maximal error between the command and the wheel speed) """
        return self._drift

    def get_l_error(self):
        """ return the _errL value (maximal error over the _l estimation) """
        return self._errL

    def get_l(self):
        """ return the _l_known value, the known distance between the wheels with an _errL error """
        return self._l_known

    def get_delta_t(self):
        """ return the _delta_t value """
        return self._delta_t

    def get_odometry(self):
        """ return the distance done by the robot between two steps with an _errOdo error """
        return self._odometry

    def get_error_odometry(self):
        """ return _errOdo value (maximal error over the odometry estimation) """
        return self._errOdo

    def get_compass(self):
        """ return the orientation of the robot with an _errCompass error """
        return self._compass

    def get_error_compass(self):
        """ return _errCompass value (maximal error over the compass estimation) """
        return self._errCompass

    @staticmethod
    def normalize_angle(angle):
        """
            Function to constraint an angle between 0 and 2*pi

            :param angle : the angle we want to normalize
            :return angle : the normalized angle
        """
        change = True
        while change:
            change = False
            if angle < 0:
                angle += (2 * pi)
                change = True
            elif angle > (2 * pi):
                change = True
                angle -= (2 * pi)
        return angle

    def init_robot(self, x, y, theta, l_wheel, err_l, v_max, drift, delta_t, err_odo, err_compass):
        """
            Function to initialize a robot

            :param x : x position of the robot
            :param y : y position of the robot
            :param theta : orientation of the robot
            :param l_wheel : distance between the two wheels
            :param err_l : error over the distance between the two wheels
            :param v_max : the two wheels max speed
            :param drift : drifting error (diff between command speed and real speed)
            :param delta_t : time step between two positions updates
            :param err_odo : error over the odometry computation
            :param err_compass : error over the compass computation
        """
        self._x = x
        self._y = y
        self._theta = theta

        self._l_known = l_wheel
        self._errL = err_l
        self._l = self._l_known + rd.uniform(0, 2 * self._errL) - self._errL

        self._delta_t = delta_t
        self._V_max = v_max
        self._drift = drift
        self._errOdo = err_odo
        self._errCompass = err_compass

    def move(self, vl, vr):
        """
            Function to move the robot according to the cinematic model and
                - the left and right wheel speed (Vl, vr)
                - the step time _delta_t (dt)
                - the drift of the robot _drift (error between command and actual wheel speed)

            :param vl : left wheel speed
            :param vr : right wheel speed
        """
        self._Vl = vl
        self._Vr = vr

        vl = vr = 0
        while vl == vr:
            # we add drifting to the command speed
            # it is assumed that it is very unlikely (impossible)that the
            #    robot will have the same speed over the two wheels, that is, it can not move straight forward

            vl = rd.uniform(self._Vl - self._drift, self._Vl + self._drift)
            vr = rd.uniform(self._Vr - self._drift, self._Vr + self._drift)

        self._Vl = vl
        self._Vr = vr

        # computation of the new position according to the model
        w = (vr - vl) / self._l
        wt = w * self._delta_t

        r = (self._l / 2.0) * (vl + vr) / (vr - vl)

        new_x = r * (sin(self._theta + wt) - sin(self._theta)) + self._x
        new_y = r * (cos(self._theta) - cos(self._theta + wt)) + self._y

        # computation of the odometry with the errOdo
        self._odometry = sqrt((new_x - self._x) ** 2 +
                              (new_y - self._y) ** 2) - rd.uniform(0, 2 * self._errOdo) + self._errOdo
        if self._odometry < 0:
            self._odometry = 0

        self._x = new_x
        self._y = new_y
        self._theta = Robot.normalize_angle(self._theta + wt)

        self._compass = self._theta - rd.uniform(0, 2 * self._errCompass) + self._errCompass

    def move_random_in_box(self, x_inf, x_sup, y_inf, y_sup):
        """
            Function to move the robot randomly inside a bounded environment. When the robot is out of the bounds
            it goes to the center

            :param x_inf: x inf bounded values of the environment
            :param x_sup : x sup bounded values of the environment
            :param y_inf : y inf bounded values of the environment
            :param y_sup : y sup bounded values of the environment
            :return vl, vr : the wheel speeds command
        """

        if x_sup >= self._x >= x_inf and y_sup >= self._y >= y_inf:
            # the speed of the wheels is generated randomly according to the max speed
            vr = rd.uniform(0, self._V_max)
            vl = rd.uniform(0, self._V_max)
        else:
            # if the robot is outside the moving area, it aims the center of the
            #    environment to go back in
            vl, vr = self.go_2_target((x_sup + x_inf) / 2.0, (y_inf + y_sup) / 2.0)

        self.move(vl, vr)

        return vl, vr

    def go_2_target(self, xc, yc):
        """ 
            Function that computes left and right wheel velocity to move the robot
            toward a target 

            :param xc : x position of the target
            :param yc : y position of the target
            :return vl : left wheel velocity
            :return vr : right speed velocity
        """

        # we compute difference between the robot and the target direction
        ang_c = Robot.normalize_angle(self.get_oriented_angle(xc, yc))
        diff = self._theta - ang_c

        if abs(diff) <= self._deltaTargetOrientation:
            # the robot needs to go forward
            vr = self._V_max
            vl = self._V_max
        elif abs(diff) < pi:
            if diff < 0:
                # the robot need to turn left
                vr = self._V_max
                vl = self._V_max / 2
            else:
                # the robot need to turn right
                vr = self._V_max / 2
                vl = self._V_max
        else:
            if diff > 0:
                # the robot need to turn left
                vr = self._V_max
                vl = self._V_max / 2
            else:
                # the robot need to turn right
                vr = self._V_max / 2
                vl = self._V_max

        return vl, vr

    def get_oriented_angle(self, xc, yc):
        """ 
            Function that provides an oriented angle from the robot position
            and the target position 

            :param xc : x position of the target
            :param yc : y position of the target
            :return angle :  the oriented angle
        """
        angle = 0
        dst = sqrt((self._x - xc) ** 2 + (self._y - yc) ** 2)
        if dst != 0:
            # note that this could be done with tan()
            theta_cos = acos((xc - self._x) / dst)
            theta_sin = asin((yc - self._y) / dst)

            if self._y <= yc:
                angle = theta_cos
            else:
                if self._x > xc:
                    angle = -theta_sin + pi
                else:
                    angle = theta_sin
        return angle

    def is_in(self, i_pose):
        """
            Function to test if the robot is in the I_POSE ([i_x], [i_y], [i_theta])

            :param i_pose : the interval position and orientation we want to test
        """
        is_in_x = i_pose.x.inf <= self._x <= i_pose.x.sup
        is_in_y = i_pose.y.inf <= self._y <= i_pose.y.sup
        self._theta = Robot.normalize_angle(self._theta)
        is_in_theta = (i_pose.theta.inf <= self._theta <= i_pose.theta.sup or
                       i_pose.theta.inf <= self._theta + 2 * pi <= i_pose.theta.sup)
        return is_in_x and is_in_y and is_in_theta

    def __str__(self):
        """
            Function to be able to print() an Interval
        """
        return "(" + "{:.4f}".format(self._x) + "," + "{:.4f}".format(self._y) + "," + "{:.4f}".format(
            self._theta) + ")"

    def get_private_x(self):
        return self._x

    def get_private_y(self):
        return self._y

    def get_private_l(self):
        return self._l

    def get_private_theta(self):
        return self._theta
