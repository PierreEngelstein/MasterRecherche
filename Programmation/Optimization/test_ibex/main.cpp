#include <iostream>
#include "ibex.h"

// Some utilities macros to simplify printing
#define print_base(out, x) out << x
#define print(x) print_base(std::cout, x)
#define println(x) print(x << std::endl);

int main_1()
{
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
        println("dist(x, pt) <=>" << f.eval(ibex::IntervalVector(1, ibex::Interval(0, 1))))
        //println("gradient dist <=> " << f.gradient(ibex::IntervalVector(1, ibex::Interval(0, 1)))) // free() error in here ??
    }

    {
        println("**********")
        ibex::Variable x(2, "x");
        ibex::Variable pt(2, "p");
        ibex::Function dist(x, pt, ibex::sqrt(ibex::sqr(x[0] - pt[0])  + ibex::sqr(x[1] - pt[1]) ));
        ibex::Vector pt1 = ibex::Vector::zeros(2);
        ibex::Vector pt2 = ibex::Vector::ones(2);
        ibex::Function f(x, ibex::Return(dist(x, pt1), dist(x, pt2)));
        println("f: x -> (||x-(1, 1)||, ||x-(0, 0)||) <=> " << f.eval_vector(ibex::IntervalVector(1, ibex::Interval(1, 2))))
    }

    {
        println("**********")
        ibex::Variable x(2, "x");
        ibex::Function f(x, ibex::Return(ibex::Return(2*x, -x, ibex::ExprVector::ROW), ibex::Return(-x, 3*x, ibex::ExprVector::ROW)));
        println("f: x -> ((2x, -x);(-x,3x)) <=> \n" << f.eval_matrix(ibex::IntervalVector(1, ibex::Interval(0, 1))))
    }

    {
        println("**********")
        ibex::Function f("/home/pierre/Documents/Polytech/MasterRecherche/Programmation/Optimization/test_ibex/test_function.txt");
        println("f: x -> ((2x, -x);(-x,3x)) <=> \n" << f.eval_matrix(ibex::IntervalVector(1, ibex::Interval(0, 1))))

        ibex::Function euler("/home/pierre/Documents/Polytech/MasterRecherche/Programmation/Optimization/test_ibex/euler.txt");
        println("f: x -> euler matrix <=> \n" << euler.eval_matrix(ibex::IntervalVector(6, ibex::Interval(0, 1))))
    }

    {
        println("**********")
        ibex::Variable x, y, z;
        double d = 0.5 * sqrt(2);
        ibex::Function f(x, y, ibex::Return(ibex::sqrt(ibex::sqr(x) + ibex::sqr(y)) - d, ibex::sqrt(ibex::sqr(x-1.0) + ibex::sqr(y-1.0)) - d));
        ibex::CtcFwdBwd ctc(f);
        ibex::IntervalVector v(2, ibex::Interval(-10, 10));
        println("v (before) = " << v)
        ctc.contract(v);
        println("v (after contract) = " << v)

        ibex::IntervalVector v1(2, ibex::Interval(-10, 10));
        ibex::CtcFixPoint fp(ctc, 1e-03);
        fp.contract(v1); // Can also put v directly as it is concretely a single iteration of fp.
        println("v (after recursive contract) = " << v1)
    }

    {
        println("**********")
        // Union contraction
        ibex::Variable x;
        ibex::NumConstraint c1(x,x<=-1);
        ibex::NumConstraint c2(x,x>=1);
        ibex::CtcFwdBwd ctc1(c1);
        ibex::CtcFwdBwd ctc2(c2);
        ibex::IntervalVector box(1,ibex::Interval::pos_reals()); // the box [0,oo)
        ibex::CtcUnion ctc3(ctc1,ctc2); // a contractor w.r.t. (x<=-1 or x>=1)
        ctc3.contract(box); // box will be contracted to [1,oo)
        println("Union contract: " << box)
        // Intersection contraction
        ibex::Variable y;
        ibex::NumConstraint c4(y, y >= -1);
        ibex::NumConstraint c5(y, y <= 1);
        ibex::CtcFwdBwd ctc4(c4);
        ibex::CtcFwdBwd ctc5(c5);
        ibex::IntervalVector box1(1, ibex::Interval::all_reals()); // [-oo, oo)
        ibex::CtcCompo ctc6(ctc4, ctc5);
        ctc6.contract(box1); // Contract to [-1,1]
        println("Intersection contract: " << box1)
        // Newton contraction
        ibex::Variable z, w;
        ibex::Function f(z, w, ibex::Return(ibex::sqrt(ibex::sqr(z) + ibex::sqr(w) ) - 1, ibex::sqrt(ibex::sqr(z - 1.0) + ibex::sqr(w - 1.0)) - 1.0));
        double initBox[][2] = {{0.999, 1.001}, {-0.001, 0.001}};
        ibex::IntervalVector box2(2, initBox);
        ibex::CtcNewton newton(f);
        newton.contract(box2);
        println("Newton contract: " << box2)
    }

    {
        println("**********")
        const int N=6;
        double bx[N]={5.09392,4.51835,0.76443,7.6879,0.823486,1.70958};
        double by[N]={0.640775,7.25862,0.417032,8.74453,3.48106,4.42533};
        double bz[N]={5.0111,2.5197,7.5308,3.52119,5.85707,4.73568};
        ibex::Interval bX[N];
        ibex::Interval bY[N];
        ibex::Interval bZ[N];
        for(int i = 0; i < N; i++){
            bX[i] = bx[i] + ibex::Interval(-0.1,0.1);
            bY[i] = by[i] + ibex::Interval(-0.1,0.1);
            bZ[i] = bz[i] + ibex::Interval(-0.1,0.1);
        }
        bX[5] += 10; // Apply an artificial outlier

        // Distance function
        ibex::Variable x(2), px, py;
        ibex::Function dist(x, px, py, ibex::sqrt(ibex::sqr(x[0]-px) + ibex::sqr(x[1] - py)));

        // Distance function to each point
        ibex::Function f0(x, dist(x, bX[0], bY[0]) - bZ[0]);
        ibex::Function f1(x, dist(x, bX[1], bY[1]) - bZ[1]);
        ibex::Function f2(x, dist(x, bX[2], bY[2]) - bZ[2]);
        ibex::Function f3(x, dist(x, bX[3], bY[3]) - bZ[3]);
        ibex::Function f4(x, dist(x, bX[4], bY[4]) - bZ[4]);
        ibex::Function f5(x, dist(x, bX[5], bY[5]) - bZ[5]);
        // Distance contractors
        ibex::CtcFwdBwd c0(f0);
        ibex::CtcFwdBwd c1(f1);
        ibex::CtcFwdBwd c2(f2);
        ibex::CtcFwdBwd c3(f3);
        ibex::CtcFwdBwd c4(f4);
        ibex::CtcFwdBwd c5(f5);

        ibex::IntervalVector initBox(2, ibex::Interval(0, 10)); // [0,10]x[0,10]
        ibex::Array<ibex::Ctc> array(c0, c1, c2, c3, c4, c5);
        ibex::CtcQInter q(array, 5); // q-intersection of each individual contractors
        ibex::IntervalVector box=initBox;
        q.contract(box);
        println("q-inter result: " << box)

        ibex::CtcFixPoint fix(q);
        fix.contract(box);
        println("fixpoint + q-inter result: " << box)
    }

    class MyContractor : public ibex::Ctc {
    public:
        explicit MyContractor(int nbVar): ibex::Ctc(nbVar){}
        void contract(ibex::IntervalVector& box) override{
            box = box.mid() + 0.5 * ibex::Interval(-1,1)*box.rad();
        }
    };

    {
        println("**********")
        MyContractor ct(3);
        ibex::IntervalVector box(3, ibex::Interval(0, 1));
        ct.contract(box);
        println("box - MyContractor: " << box)
        ibex::CtcFixPoint fix(ct, 0.001);
        fix.contract(box);
        println("box - fixpoint(MyContractor): " << box)
    }

    {


        println("**********")
        double _p1[9][2] = {{0.1, 0.1}, {0, 0},
                           {0, 0}, {0, 0}};
        ibex::IntervalMatrix p1(2, 2, _p1);

        double _p2[9][2] = {{0.3, 0.3}, {0.3, 0.3},
                            {0.3, 0.3}, {0.3, 0.3}};
        ibex::IntervalMatrix p2(2, 2, _p2);

        double _p3[9][2] = {{0, 0}, {0, 0},
                            {0, 0}, {0.1, 0.1}};
        ibex::IntervalMatrix p3(2, 2, _p3);

        println(p1)
        println(p2)
        println(p1[0][0] + p1[1][1])
    }
    return 0;
}
