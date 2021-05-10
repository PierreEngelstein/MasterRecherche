#include <iostream>
#include <mutex>
#include <future>
#include <interval/interval.hpp>
#define printvar(x) std::cout << #x << " = " << x << "\n";
#define println(x) std::cout << x  << "\n";
#define printerr(x) std::cout << "[Error] " << x << "\n";
#define printwarn(x) std::cout << "[Warning] " << x << "\n";


using filib::interval;
typedef interval<double> Interval;
typedef std::vector<Interval> IntervalVector;

std::ostream& operator<<(std::ostream& os, const IntervalVector& itVect) {
    os << "{";
    for(auto& it : itVect){
        os << it;
    }
    os << "}";
    return os;
}

IntervalVector bisect(const Interval& it){
    return IntervalVector({Interval(it.inf(), it.mid()), Interval(it.mid(), it.sup())});
}

Interval function(const IntervalVector& it){
    if(it.size() != 2) {printerr("IntervalVector size not correct!") return Interval();};
    return it[0] + it[1];
}

bool createBisect(std::vector<interval<double>> &variable, std::mutex& variablesMutex){
    auto currentVariable = variable;
    std::vector<Interval> newVariables;
    for(auto & j : currentVariable){
        auto variableBisect = bisect(j);
        newVariables.push_back(variableBisect[0]);
        newVariables.push_back(variableBisect[1]);
    }
    //Thread-safe access
    variablesMutex.lock();
    variable = newVariables;
    variablesMutex.unlock();
    return true;
}

void Maximize(const IntervalVector& vector, double precision=1e-07){
    std::vector<std::vector<Interval>> variables;
    std::mutex variablesMutex;

    for(auto& variable: vector){
        variables.push_back({variable});
    }

    bool done = false;
    for(int k = 0; k < 10; k++){ // TODO: replace with 'while'

        auto future = std::async([](const std::string& s ){return "Hello C++11 from " + s + ".";},"lambda function");

        std::future<bool> handle = std::async(createBisect, variables[0], variablesMutex);



        for(auto & variable : variables){
            auto currentVariable = variable;
            std::vector<Interval> newVariables;
            for(auto & j : currentVariable){
                auto variableBisect = bisect(j);
                newVariables.push_back(variableBisect[0]);
                newVariables.push_back(variableBisect[1]);
            }
            //Thread-safe access
            variablesMutex.lock();
            variable = newVariables;
            variablesMutex.unlock();
        }

        for(auto& variable_1: variables){

        }
    }
    for(int i = 0; i <= variables.size(); i++){
        printvar(variables[i])
    }
}

int main() {
    println("Interval Optimization.")
    IntervalVector vect({Interval(0, 1), Interval(0, 1)});
    Maximize(vect);
    return 0;
}
