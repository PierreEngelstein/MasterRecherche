#include <iostream>
#include "ibex.h"

// Some utilities macros to simplify printing
#define print_base(out, x) out << x
#define print(x) print_base(std::cout, x)
#define println(x) print(x << std::endl);

int main() {
    {
        println("**********")
        ibex::Interval x(0, 1);
        println("Interval x = " << x)
        ibex::Interval y;
        println("Interval y = " << y)
        ibex::Interval z = ibex::Interval::all_reals();
        println("Interval z = " << z)
        ibex::Interval w = ibex::Interval::empty_set();
        println("Interval w = " << w)
    }

    {
        println("**********")
        ibex::Interval x(0, 1);
        ibex::Interval y(3, 4);
        println("x+y=" << x + y << "; x*y=" << x * y)
        ibex::Interval a(-1, 1);
        println("a=" << a)
        ibex::Interval b=ibex::exp(a + 1);
        println("exp(a+1) = " << b)
    }
    {
        println("**********")
        double _x[3][2] = {{0, 1}, {2, 3}, {4 ,5}};
        ibex::IntervalVector x(3, _x);
        println(x)

        ibex::IntervalVector y(3, ibex::Interval(1, 2));
        println(y)
        ibex::IntervalVector z=ibex::IntervalVector::empty(3);
        println(z)
    }

    {
        println("**********")
        double _M[9][2] = {{0, 1}, {0, 1}, {0, 1},
                           {0, 2}, {0, 2}, {0, 2},
                           {0, 3}, {0, 3}, {0, 3}};
        ibex::IntervalMatrix M(3, 3, _M);
        println("M=\n" << M)
        double _x[3][2] = {{0, 1}, {2, 3}, {4, 5}};
        ibex::IntervalVector x(3, _x);
        println("v=" << x)
        ibex::IntervalVector y = M*x;
        println("y=M*v" << y)
        ibex::IntervalMatrix N = M.transpose();
        println("M^t = \n" << N)
    }

    {
        println("**********")
        double _M[9][2] = {{0, 1}, {0, 1}, {0, 1},
                           {0, 2}, {0, 2}, {0, 2},
                           {0, 3}, {0, 3}, {0, 3}};
        ibex::IntervalMatrix M(3, 3, _M);
        double _x[3][2] = {{0, 1}, {0, 1}, {0, 1}};
        ibex::IntervalVector x(3, _x);
        ibex::Matrix M2 = M.mag();
        ibex::Vector x2 = x.mid();
        println("M=\n" << M << "\nx=" << x)
        println("magnitude(M) = \n" << M2);
        println("mid(x) = " << x2)
        println("magnitude(M) * mid(x) = " << M2*x2)
    }

    {
        println("**********")
        ibex::Function f("x", "y", "sin(x+y)");
        ibex::Variable x("x");
        ibex::Variable y("y");
        ibex::Function f1(x, y, ibex::sin(2*(x+y)));
        double _inter[3][2] = {{0, 1}, {2, 3}};
        println("f(x, y) = sin(2*(x+y)) <=>" << f.eval(ibex::IntervalVector(2, _inter)))
    }

    {
        println("**********")
        ibex::Variable x(2);
        ibex::Variable y(2);
        ibex::Function dist(x, y, ibex::sqrt(ibex::sqr(x[0] - y[0]) + ibex::sqr(x[1] - y[1])));
        double _inter[3][2] = {{0, 1}, {2, 3}};
        println("dist(x, y) = sqrt(x[0] - y[0] + sqr(x[1] - y[1]) <=>" << dist.eval(ibex::IntervalVector(2, _inter)))

        ibex::Vector pt(2);
        pt[0] = 1; pt[1] = 2;
        ibex::Variable z(2);
        ibex::Function f(z, dist(z, pt));
        println("dist(x, pt) <=>" << f.eval(ibex::IntervalVector(2, _inter)))
    }

    return 0;
}
