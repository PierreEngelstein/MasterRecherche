#include <iostream>
#include "ibex.h"

// Some utilities macros to simplify printing
#define print_base(out, x) out << x
#define print(x) print_base(std::cout, x)
#define println(x) print(x << std::endl);

#ifdef __IBEX_NO_LP_SOLVER__
#error "You need a LP solver to run this example (use -DLP_LIB=... in cmake)"
#endif


ibex::Interval Trace(const ibex::IntervalMatrix& matrix){
    ibex::Interval trace(0, 0);
    for(int i = 0; i < matrix.nb_cols(); i++){
        trace += matrix[i][i];
    }
    return trace;
}

ibex::Interval Trace_Mul(const ibex::IntervalMatrix& matrix_left, const ibex::IntervalMatrix& matrix_right){
    ibex::Interval trace(0, 0);
    for(int i = 0; i < matrix_left.nb_cols(); i++){
        for(int j = 0; j < matrix_left.nb_rows(); j++){
            trace += matrix_left[i][j] * matrix_right[j][i];
        }
    }
    return trace;
}

int main(int argc, const char **argv){
    println("**********")
    double _p1[4][2] = {{0.1, 0.1}, {0, 0},
                        {0, 0}, {0, 0}};
    ibex::IntervalMatrix p1(2, 2, _p1);

    double _p2[4][2] = {{0.3, 0.3}, {0.3, 0.3},
                        {0.3, 0.3}, {0.3, 0.3}};
    ibex::IntervalMatrix p2(2, 2, _p2);

    double _p3[4][2] = {{0, 0}, {0, 0},
                        {0, 0}, {0.1, 0.1}};
    ibex::IntervalMatrix p3(2, 2, _p3);

    double _m1[4][2] = {{0, 0}, {0, 0},
                        {0, 0}, {0, 0}};
    ibex::IntervalMatrix m1(2, 2, _m1);

    double _m2[4][2] = {{0.723, 0.723}, {0.447, 0.447},
                        {0.447, 0.447}, {0.276, 0.276}};
    ibex::IntervalMatrix m2(2, 2, _m2);

    double _m3[4][2] = {{0.276, 0.276}, {-0.447, -0.447},
                        {-0.447, -0.447}, {0.724, 0.724}};
    ibex::IntervalMatrix m3(2, 2, _m3);

    println(Trace(m2*p2))
    println(Trace_Mul(m2, p2))
//    println(Trace(p3))

//    ibex::Variable mu1(2, 2);
//    ibex::Function trace(mu1, mu1[0][0] + mu1[1][1]);
//    ibex::IntervalVector res_trace(2*2);
//    println(res_trace)
//    trace.backward(m1, res_trace);
//    println(res_trace)

//    ibex::CtcFwdBwd trace_ct(trace);
//    ibex::IntervalVector initBox(2, ibex::Interval(0, 10));
//    println(initBox)
//    trace_ct.contract(initBox);
//    println("\n" << initBox)

//    ibex::Variable M1_11, M1_D, M1_22, M2_11, M2_D, M2_22, M3_11, M3_D, M3_22;
//    ibex::Function trace(M1_11, M1_22, M1_D, M1_11 * p1[0][0]);
//
//    ibex::CtcFwdBwd trace_ctc(trace);
//    double _m1_ctc[3][2] = {{0.723, 0.723}, {0.447, 0.447}, {0.276, 0.276}};
//    ibex::IntervalVector initBox(3, _m1_ctc);
//    println(initBox)
//    trace_ctc.contract(initBox);
//    println("\n" << initBox)

    ibex::System system("/home/pierre/Documents/Polytech/MasterRecherche/Programmation/Optimization/test_ibex/opti.txt");
    ibex::DefaultOptimizer o(system, 1e-07);
    println(system.goal)
    o.optimize(system.box);

    println(o.get_loup_point())
    println(o.get_uplo())
}
