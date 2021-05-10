//
// Created by pierre on 4/20/21.
//

#include "ibex.h"

const auto minXLog = std::exp(-1);

ibex::Interval Newton(const ibex::Interval& in, const double& target, const double& precision = 1e-03){
    ibex::Interval res = in;
    auto prev = res;
    int operations = 0;
    do {
        auto xc = ibex::Interval(res.mid(), res.mid());
        prev = res;
        auto deriv = ibex::log(res) + 1;
        if(deriv.contains(0)) break;
        res = xc - ((ibex::xlog(xc) - target)/deriv);
        operations ++;
    } while (ibex::abs(prev - res).ub() >= precision);
    printvar(operations)
    return res;
}

ibex::Interval bwd_log_positive(const double& y, const double precision = 0.001){
    if(y <= 0) return ibex::Interval::empty_set();
    ibex::Interval it(1, 10);
    int max = 10;
    int operations = 0;
    while(true){
        auto pair = it.bisect();
        auto f1 = ibex::xlog(pair.first);
        auto f2 = ibex::xlog(pair.second);
        operations ++;
        if(f1.contains(y)) {
            it = Newton(pair.first, y, precision);
        }
        else if(f2.contains(y)) {
            it = Newton(pair.second, y, precision);
        }
        else {
            it.set_empty();
            it = ibex::Interval(max, max+10);
            max += 10;
            continue;
        }
        if(std::abs(it.ub() - it.lb()) <= precision){
            break;
        }
    }
    printvar(operations)
    return it;
}

std::array<ibex::Interval, 2> bwd_xlog(const double& y, const double& precision = 0.001){
    if(y < -minXLog) return {ibex::Interval::empty_set(), ibex::Interval::empty_set()};
    if(y > 0) return {ibex::Interval::empty_set(), ibex::Interval::empty_set()}; // TODO backward for y > 0

    ibex::Interval it(0, minXLog);
    std::array<ibex::Interval, 2> result;
    int operations = 0;
    while(true){
        auto pair = it.bisect();
        auto f1 = ibex::xlog(pair.first);
        auto f2 = ibex::xlog(pair.second);
        operations++;
        if(f1.contains(y)) it = Newton(pair.first, y, precision);
        else if(f2.contains(y)) it = Newton(pair.second, y, precision);
        else {
            result[0] = ibex::Interval::empty_set();
            break;
        }
        if(std::abs(it.ub() - it.lb()) <= precision){
            result[0] = it;
            break;
        }
    }
    printvar(operations)

    operations = 0;
    it = ibex::Interval(minXLog, 1);
    while(true){
        auto pair = it.bisect();
        auto f1 = ibex::xlog(pair.first);
        auto f2 = ibex::xlog(pair.second);
        operations++;
        if(f1.contains(y)) it = Newton(pair.first, y, precision);
        else if(f2.contains(y)) it = Newton(pair.second, y, precision);
        else {
            result[1] = ibex::Interval::empty_set();
            break;
        }
        if(std::abs(it.ub() - it.lb()) <= precision){
            result[1] = it;
            break;
        }
    }
    printvar(operations)
    return result;
}


int main_1(int argc, const char** argv){
    auto res = bwd_xlog(-0.2, 1e-15);
    printvar(res[0])
    printvar(res[1])

    auto res_pos = bwd_log_positive(100, 1e-15);
    printvar(res_pos)

    auto it = ibex::Interval(0, std::exp(-1));
//    Newton(it, -0.2, 1e-15);

}
