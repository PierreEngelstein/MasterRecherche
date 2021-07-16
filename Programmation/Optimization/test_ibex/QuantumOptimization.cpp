#include <iostream>
#include "ibex.h"
#include "matplotlibcpp.h"
#include <complex>
#include <regex>
#include <execution>
#include <algorithm>

# define M_PI           3.14159265358979323846

#ifdef __IBEX_NO_LP_SOLVER__
#error "You need a LP solver to run this example (use -DLP_LIB=... in cmake)"
#endif

//double Entropy()

bool replace(std::string& str, const std::string& from, const std::string& to) {
    size_t start_pos = str.find(from);
    if(start_pos == std::string::npos)
        return false;
    str.replace(start_pos, from.length(), to);
    return true;
}

std::ostream& operator<<(std::ostream& os, const std::vector<std::array<std::array<double, 2>, 2>>& matrix){
    os << "[";
    for(auto i: matrix){
        for(auto j: i){
            os << "(";
            for(auto k: j){
                os << k << " ";
            }
            os << ")";
        }
    }
    return os;
}

template<int m_size>
std::string generate(int m_amount, bool symmetric, const std::vector<std::pair<ibex::Matrix, double>>& input){
    printvar(m_amount)
    printvar(input.size())
    if(input.size() != m_amount) return "";

    auto sum = 0.0;
    for(auto& i: input){
        sum += i.second;
    }
    if(std::abs(sum - 1) >= 0.001) {
        println("Warning, sum of probabilities is != 1 (" << sum << ")");
        return "";
    }

    std::ostringstream fileContent;
    fileContent << "Constants\n";
    fileContent << "  m_amount = " << m_amount << ";\n";
    fileContent << "  m_size = " << m_size << ";\n";
    for(int i = 0; i < input.size(); i++){
        fileContent << "  P" << (i+1) << "[m_size][m_size] = (";
        for(int j = 0; j < m_size; j++){
            fileContent << "(";
            for(int k = 0; k < m_size; k++){
                auto res = input[i].second * input[i].first;
                fileContent << res[j][k];
                if(k != m_size-1) fileContent << ", ";
            }
            fileContent << ")";
            if(j != m_size-1) fileContent << "; ";
            else fileContent << ");\n";
        }
    }
    fileContent << "\n";
    fileContent << "function tr(m1[m_size][m_size], m2[m_size][m_size])\n";
    fileContent << "  return ";
    for(int i = 1; i <= m_size; i++) {
        for (int j = 1; j <= m_size; j++) {
            fileContent << "m1(" << i << ")(" << j << ") * m2(" << j << ")(" << i << ")";
            if( j != m_size || i != m_size){
                fileContent << " + ";
            }
        }
    }
    fileContent << ";\nend\n\n";


    // Marginal entropy of M
    fileContent << "function EntropyM(";
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_M" << i << "[m_size][m_size], ";
    }
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_P" << i << "[m_size][m_size]";
        if(i != m_amount) fileContent << ", ";
        else fileContent << ")";
    }
    fileContent << "\n";
    for(int i = 1; i <= m_amount; i++){
        fileContent << "  sum_m" << i << " = ";
        for(int j = 1; j <= m_amount; j++){
            fileContent << "tr(_M" << i << ", _P" << j << ")";
            if(j != m_amount) fileContent << " + ";
            else fileContent << ";\n";
        }
    }
    fileContent << "  return ";
    for(int i = 1; i <= m_amount; i++){
        fileContent << "-xlog(sum_m" << i << ")";
    }
    fileContent << ";\nend\n\n";

    // Marginal entropy of P
    fileContent << "function EntropyP(";
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_M" << i << "[m_size][m_size], ";
    }
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_P" << i << "[m_size][m_size]";
        if(i != m_amount) fileContent << ", ";
        else fileContent << ")";
    }
    fileContent << "\n";
    for(int i = 1; i <= m_amount; i++){
        fileContent << "  sum_p" << i << " = ";
        for(int j = 1; j <= m_amount; j++){
            fileContent << "tr(_M" << j << ", _P" << i << ")";
            if(j != m_amount) fileContent << " + ";
            else fileContent << ";\n";
        }
    }
    fileContent << "  return ";
    for(int i = 1; i <= m_amount; i++){
        fileContent << "-xlog(sum_p" << i << ")";
    }
    fileContent << ";\nend\n\n";

    // Joint entropy of M & P
    fileContent << "function EntropyMP(";
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_M" << i << "[m_size][m_size], ";
    }
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_P" << i << "[m_size][m_size]";
        if(i != m_amount) fileContent << ", ";
        else fileContent << ")";
    }
    fileContent << "\n";
    fileContent << "  return ";
    for(int i = 1; i <= m_amount; i++){
        for(int j = 1; j <= m_amount; j++){
            fileContent << "-xlog(tr(_M" << i << ", _P" << j << "))";
        }
    }
    fileContent << ";\nend\n\n";

    fileContent << "function MutualInformation(";
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_M" << i << "[m_size][m_size], ";
    }
    for(int i = 1; i <= m_amount; i++) {
        fileContent << "_P" << i << "[m_size][m_size]";
        if(i != m_amount) fileContent << ", ";
        else fileContent << ")";
    }
    fileContent << "\n";

    fileContent << "  return EntropyM(";
    for(int i = 1; i <= m_amount; i++){
        fileContent << "_M" << i << ", ";
    }
    for(int i = 1; i <= m_amount; i++){
        fileContent << "_P" << i;
        if(i != m_amount) fileContent << ", ";
        else fileContent << ") + ";
    }

    fileContent << "(";
    for(auto& pair: input){
        fileContent << " -" << pair.second << " * ln(" << pair.second << ")";
    }
    fileContent << ") - ";

    fileContent << "EntropyMP(";
    for(int i = 1; i <= m_amount; i++){
        fileContent << "_M" << i << ", ";
    }
    for(int i = 1; i <= m_amount; i++){
        fileContent << "_P" << i;
        if(i != m_amount) fileContent << ", ";
        else fileContent << ");";
    }
    fileContent << "\nend\n\n";

    if(symmetric) {
        fileContent << "function I(";
        for (int i = 1; i <= m_amount; i++) {
            fileContent << "_P" << i << "[m_size][m_size], ";
        }
        for (int i = 1; i <= m_amount; i++) {
            fileContent << "_M" << i << "_11" << ", _M" << i << "_12" << ", _M" << i << "_22";
            if (i != m_amount) fileContent << ", ";
            else fileContent << ")\n";
        }

        for (int i = 1; i <= m_amount; i++) {
            fileContent << "  _M" << i << " = ((_M" << i << "_11, _M" << i << "_12); (_M" << i << "_12, _M" << i
                        << "_22));\n";
        }
        fileContent << "  return MutualInformation(";
        for (int i = 1; i <= m_amount; i++) {
            fileContent << "_M" << i << ", ";
        }
        for (int i = 1; i <= m_amount; i++) {
            fileContent << "_P" << i;
            if (i != m_amount) fileContent << ", ";
            else fileContent << ");\nend\n\n";
        }
    }

    fileContent << "Variables\n";
    for(int i = 1; i <= m_amount; i++){
        if(symmetric){
            fileContent << "  M" << i << "_11 in [0, 1], " << " M" << i << "_12 in [-1, 1], " << " M" << i << "_22 in [0, 1];\n";
        }else{
            fileContent << "  M" << i << "[m_size][m_size] in (([0, 1], [-1, 1]); ([-1, 1], [0, 1]));\n";
        }
    }
    fileContent << "\nMinimize\n";
    if(symmetric){
        fileContent << "  -I(";
        for(int i = 1; i <= m_amount; i++){
            fileContent << "P" << i << ", ";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i << "_11, " << " M" << i << "_12, " << " M" << i << "_22";
            if(i != m_amount) fileContent << ", ";
            else fileContent << ");\n\n";
        }
    }else{
        fileContent << "  -MutualInformation(";
        for(int i = 1; i <= m_amount; i++){
            fileContent << "P" << i << ", ";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i;
            if(i != m_amount) fileContent << ", ";
            else fileContent << ");\n\n";
        }
    }


    fileContent << "Constraints\n  ";
    if(symmetric){

        fileContent << "  -I(";
        for(int i = 1; i <= m_amount; i++){
            fileContent << "P" << i << ", ";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i << "_11, " << " M" << i << "_12, " << " M" << i << "_22";
            if(i != m_amount) fileContent << ", ";
            else fileContent << ") <= ";
        }

        fileContent << "(";
        for(auto& pair: input){
            fileContent << " -" << pair.second << " * ln(" << pair.second << ")";
        }
        fileContent << ");\n\n  ";

        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i << "_11";
            if(i != m_amount) fileContent << " + ";
            else fileContent << " = 1;\n  ";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i << "_12";
            if(i != m_amount) fileContent << " + ";
            else fileContent << " = 0;\n  ";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i << "_22";
            if(i != m_amount) fileContent << " + ";
            else fileContent << " = 1;\n\n";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "  M" << i << "_11 > 0;\n";
            fileContent << "  M" << i << "_22 > 0;\n";
            fileContent << "  M" << i << "_11 * M" << i << "_22 - M" << i << "_12 ^ 2 > 0;\n";
        }
    }else{
        fileContent << "  -MutualInformation(";
        for(int i = 1; i <= m_amount; i++){
            fileContent << "P" << i << ", ";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i;
            if(i != m_amount) fileContent << ", ";
            else fileContent << ") <= ";
        }
        fileContent << "(";
        for(auto& pair: input){
            fileContent << " -" << pair.second << " * ln(" << pair.second << ")";
        }
        fileContent << ");\n\n  ";

        for(int i = 1; i <= m_amount; i++){
            fileContent << "M" << i;
            if(i != m_amount) fileContent << " + ";
            else fileContent << " = ";
        }
        fileContent << "(";
        for(int i = 0; i < m_size; i++){
            fileContent << "(";
            for(int j = 0; j < m_size; j++){
                if( i == j) fileContent << "1";
                else fileContent << "0";
                if(j != m_size-1) fileContent << ", ";
            }
            fileContent << ")";
            if(i != m_size-1) fileContent << "; ";
            else fileContent << ");\n";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "  M" << i << "(1)(1) > 0;\n";
            fileContent << "  M" << i << "(2)(2) > 0;\n";
        }
        for(int i = 1; i <= m_amount; i++){
            fileContent << "  M" << i << "(1)(1) * M" << i <<  "(2)(2) - M" << i << "(1)(2) * M" << i << "(2)(1) > 0;\n";
        }
    }

    fileContent << "end";
    return fileContent.str();
}


std::string generate_2d_bench(const std::vector<std::pair<ibex::Matrix, double>>& input){
    auto sum = 0.0;
    for(auto& i: input){
        sum += i.second;
    }
    if(std::abs(sum - 1) >= 0.001) {
        println("Warning, sum of probabilities is != 1 (" << sum << ")");
        return "";
    }
    std::ostringstream fileContent;
    fileContent << "Constants\n"
                   "  m_size = 2;\n"
                   "  P1[m_size][m_size] = ((" << input[0].first[0][0]*input[0].second << ", " << input[0].first[0][1]*input[0].second<<"); ("<<input[0].first[1][0]*input[0].second<<", "<<input[0].first[1][1]*input[0].second<<"));\n"
                   "  P2[m_size][m_size] = ((" << input[1].first[0][0]*input[1].second << ", " << input[1].first[0][1]*input[1].second<<"); ("<<input[1].first[1][0]*input[1].second<<", "<<input[1].first[1][1]*input[1].second<<"));\n"
                   "\n"
                   "// M: measurement operator\n"
                   "// P: density operator\n"
                   "function tr(M[m_size][m_size], P[m_size][m_size])\n"
                   "  return P(1)(1) * M(1)(1) + 2*M(1)(2)*P(1)(2) + 2*M(2)(1)*P(2)(1) + M(2)(2)*P(2)(2);\n"
                   "end\n"
                   "\n"
                   "function EntropyM(_M1[m_size][m_size], _M2[m_size][m_size], _P1[m_size][m_size], _P2[m_size][m_size])\n"
                   "  sum_m1 = tr(_M1, _P1) + tr(_M1, _P2);\n"
                   "  sum_m2 = tr(_M2, _P1) + tr(_M2, _P2);\n"
                   "  return -xlog(sum_m1)-xlog(sum_m2);\n"
                   "end\n"
                   "\n"
                   "function EntropyP(_M1[m_size][m_size], _M2[m_size][m_size], _P1[m_size][m_size], _P2[m_size][m_size])\n"
                   "  sum_p1 = tr(_M1, _P1) + tr(_M2, _P1);\n"
                   "  sum_p2 = tr(_M1, _P2) + tr(_M2, _P2);\n"
                   "  return -xlog(sum_p1)-xlog(sum_p2);\n"
                   "end\n"
                   "\n"
                   "function EntropyMP(_M1[m_size][m_size], _M2[m_size][m_size], _P1[m_size][m_size], _P2[m_size][m_size])\n"
                   "  return -xlog(tr(_M1, _P1))-xlog(tr(_M1, _P2))-xlog(tr(_M2, _P1))-xlog(tr(_M2, _P2));\n"
                   "end\n"
                   "\n"
                   "function MutualInformation(_M1[m_size][m_size], _M2[m_size][m_size], _P1[m_size][m_size], _P2[m_size][m_size])\n"
                   "  return EntropyM(_M1, _M2, _P1, _P2) + ( -0.10 * ln(0.10) -0.90 * ln(0.90)) - EntropyMP(_M1, _M2, _P1, _P2);\n"
                   "end\n"
                   "\n"
                   "function I(_P1[m_size][m_size], _P2[m_size][m_size], _m1a, _m1b, _m1c, _m1d)\n"
                   "  _M1 = ((_m1a, _m1b); (_m1c, _m1d));\n"
                   "  _M2 = ((1-_m1a, -_m1b); (-_m1c, 1-_m1d));\n"
                   "  return MutualInformation(_M1, _M2, _P1, _P2);\n"
                   "end\n"
                   "\n"
                   "Variables\n"
                   "  M1_a in [0, 0.5],  M1_b in [-1, 1], M1_d in [0, 1];\n"
                   "\n"
                   "Minimize\n"
                   "  -I(P1, P2, M1_a,  M1_b,  0, M1_d)\n"
                   "\n"
                   "Constraints\n"
                   "  M1_a >= 0;\n"
                   "  M1_a <= 0.5;\n"
                   "  M1_d >= 0;\n"
                   "  M1_a*M1_d - M1_b^2 >= 0;\n"
                   "  (1-M1_a)*(1-M1_d) - (-M1_b)^2 >= 0;\n"
                   "end";
    return fileContent.str();

}

int main(int argc, char *argv[]){

    auto symmetric = false;
    auto amount = 2;
    std::vector<double> durations;
    std::vector<double> angles;
    for(int i = 0; i <= 360; i++){
        float angle = i * M_PI / 180;
        angles.push_back(i);
        println("angle: " << i << " degrees")
        std::vector<std::pair<ibex::Matrix, double>> in;

        double p1[4] = {1, 0, 0, 0};
        in.emplace_back(std::make_pair(ibex::Matrix(2, 2, p1), 0.1));

        double p3[4] = {std::cos(angle)*std::cos(angle), std::abs(std::cos(angle)*std::sin(angle)), 0, std::sin(angle)*std::sin(angle)};
        in.emplace_back(std::make_pair(ibex::Matrix(2, 2, p3), 0.9));

        auto mbCt = generate_2d_bench(in);
        // Remove double precision errors (for ex, 0.1 written as 0.1000001)
        mbCt = std::regex_replace(mbCt, std::regex("0001"), "");

        std::ofstream outFile("opti_auto.txt");
        outFile << mbCt;
        outFile.close();

        ibex::System sys("opti_auto.txt");
        printvar(sys.goal->expr())
        ibex::DefaultOptimizerConfig cfg(sys);
        cfg.set_trace(0);
        cfg.set_abs_eps_f(0.01);
        cfg.set_inHC4(false);
        ibex::Optimizer o(cfg);
        auto now = clock();
        o.optimize(sys.box);
        double executionTime = ((double)(clock() - now)/1000000.0);
        durations.push_back(executionTime);
        println("nb_cells: " << o.get_nb_cells())
        println("execution time: " << executionTime);
        println("==========")
    }

    matplotlibcpp::title("Temps d'optimisation en fonction de l'angle entre rho_1 et rho_2, precision sur f=0.01");
    matplotlibcpp::xlabel("Angle");
    matplotlibcpp::ylabel("Temps d'optimisation (secondes)");
    matplotlibcpp::plot(angles, durations);
    matplotlibcpp::show();

    return 1;



//    std::ofstream outFile("opti_auto.txt");
//    outFile << mbCt;
//    outFile.close();

    ibex::System sys("opti_auto.txt");
    printvar(sys.goal->expr())
    ibex::DefaultOptimizerConfig cfg(sys);
    cfg.set_trace(1);
    cfg.set_abs_eps_f(0.01);
    cfg.set_inHC4(false);
//    cfg.set_extended_cov(true);
    ibex::Optimizer o(cfg);
    auto now = clock();
    o.optimize(sys.box);
    println("execution time: " << ((double)(clock() - now)/1000000.0));

    auto r_lb = o.get_loup_point().lb();
    auto r_ub = o.get_loup_point().ub();
    printvar(r_lb)
    printvar(r_ub)
    printvar(o.get_loup())
    printvar(o.get_uplo())
    printvar(o.get_nb_cells())
    printvar(o.get_data()[0])
    printvar(o.get_data().size())

    std::ifstream it("opti_auto_solve.txt");
    std::stringstream buffer;
    buffer << it.rdbuf();
    std::string content = buffer.str();
    std::string beforeModification = content;
//    println(content)
    std::stringstream values_bounds_solve;
    values_bounds_solve << o.get_uplo() << ", " << o.get_loup();
    printvar(values_bounds_solve.str())
    replace(content, "a, b", values_bounds_solve.str());
    std::ofstream newContent ("opti_auto_solve_tmp.txt");
    if(newContent.is_open()){
        newContent << content;
    }
    newContent.close();

    printvar(sys.goal->expr())
    printvar(sys.goal->cf)
    return 0;

    ibex::System optiDerivMa("opti_auto_deriv_a.txt");
    printvar(optiDerivMa.goal->expr())

    ibex::System optiDerivMb("opti_auto_deriv_b.txt");
    printvar(optiDerivMb.goal->expr())

    ibex::System optiDerivMd("opti_auto_deriv_d.txt");
    printvar(optiDerivMd.goal->expr())

    ibex::System solveSystem("opti_auto_solve_tmp.txt");
    ibex::DefaultSolver solver(solveSystem);
    println("Starting solver...")
    now = clock();
    solver.solve(solveSystem.box);
    println("execution time: " << ((double)(clock() - now)/1000000.0));

    auto data = solver.get_data();
    auto constraint0 = sys.ctrs[0];
    auto constraint1 = sys.ctrs[1];
    auto constraint2 = sys.ctrs[2];
    auto constraint3 = sys.ctrs[3];
    auto constraint4 = sys.ctrs[4];
    printvar(data.size())
    int amountContained = 0;
    int totalAmount = 0;
    int amountMin = data.size();
    int amountMax = 0;


    for(int i = 0; i < data.size(); i++){
        uint8_t amountLocal = 0;
        auto d = data[i];
        printvar(d)
        auto resultFunc = sys.goal->gradient(d);
        printvar(resultFunc)
        ibex::Interval newIt(std::min(sys.goal->eval(d.ub()).ub(), sys.goal->eval(d.lb()).lb()), std::max(sys.goal->eval(d.ub()).ub(), sys.goal->eval(d.lb()).lb()));
        printvar(newIt)
        printvar(newIt.rad() / resultFunc.rad())
        auto resultDerivMa = optiDerivMa.goal->eval(d);
        auto resultDerivMb = optiDerivMb.goal->eval(d);
        auto resultDerivMd = optiDerivMd.goal->eval(d);
        printvar(resultDerivMa)
        printvar(resultDerivMb)
        printvar(resultDerivMd)

        auto result1 = constraint1.f.eval(d);
        printvar(constraint1)
        printvar(result1)
        printvar((result1.lb() >= 0));
        println("")

        if(result1.lb() >= 0) amountLocal ++;

        auto result2 = constraint2.f.eval(d);
        printvar(constraint2)
        printvar(result2)
        printvar((result2.lb() >= 0));
        println("")
        if(result2.lb() >= 0) amountLocal ++;

        auto result3 = constraint3.f.eval(d);
        printvar(constraint3)
        printvar(result3)
        printvar((result3.lb() >= 0));
        println("")
        if(result3.lb() >= 0) amountLocal ++;

        auto result4 = constraint4.f.eval(d);
        printvar(constraint4)
        printvar(result4)
        printvar((result4.lb() >= 0));
        println("")
        if(result4.lb() >= 0) amountLocal ++;

        if(amountLocal == 4){
            println("Solution entirely contained !")
            amountContained++;
        }

        totalAmount += amountLocal;
        if(amountLocal <= amountMin) amountMin = amountLocal;
        if(amountLocal >= amountMax) amountMax = amountLocal;

        println("==========")
    }
    double mean = ((double)totalAmount) / ((double)data.size());
    printvar(mean)
    printvar(amountMin)
    printvar(amountMax)
    printvar(amountContained)
    auto amountContainedPercent = ((double) amountContained) / ((double) data.size());
    printvar(amountContainedPercent)
    remove("opti_auto_solve_tmp.txt");
    return 0;


//    ibex::Cell* cell = o.buffer.top();
//    bool isNull = (cell == nullptr);
    printvar(o.buffer.empty())

    // Convert result to matrix
    std::vector<ibex::Matrix> result;
    auto delta = (symmetric ? 3 : 4);
    for(int i = 0; i < amount; i++){
        double r[4] = {r_lb[delta*i], r_lb[delta*i + 1], r_lb[delta*i + (symmetric ? 1 : 2)], r_lb[delta*i + (symmetric ? 2 : 3)]};
        ibex::Matrix mat(2, 2, r);
        result.push_back(mat);
    }
    double _mat_id[4] = {1, 0, 0, 1};
    auto mat_id = ibex::Matrix(2, 2, _mat_id);
    println("M1=\n" << result[0])
    println("M2=\n" << result[1])
    println("M3=\n" << (mat_id - result[0] - result[1]))
    printvar(sys.goal->eval(r_lb))
    printvar(sys.goal->eval(r_ub))
    auto precision = std::abs(sys.goal->eval(r_lb).ub() - sys.goal->eval(r_lb).lb());
    printvar(precision)
    printvar(std::abs(o.get_uplo() - o.get_loup()) )

//    std::vector<double> x;
//    std::vector<double> y;
//
//    for(double i = 1.0; i >= 0.01; i-=0.01) x.push_back(i);
//
//    // Parallel execution for different precision values
//    std::for_each(std::execution::par_unseq, std::begin(x), std::end(x), [&](double i){
//        printvar(i)
//        ibex::System sys("opti_auto.txt");
//        ibex::DefaultOptimizerConfig cfg(sys);
//        cfg.set_trace(0);
//        cfg.set_abs_eps_f(i);
//        cfg.set_inHC4(false);
//        ibex::Optimizer o(cfg);
//        auto now = clock();
//        o.optimize(sys.box);
//        y.push_back(((double)(clock() - now)/1000000.0));
//    });
//
//    matplotlibcpp::title("Temps d'optimisation en fonction de la précision");
//    matplotlibcpp::xlabel("Précision");
//    matplotlibcpp::ylabel("Temps d'optimisation (secondes)");
//    matplotlibcpp::plot(x, y);
//    matplotlibcpp::show();

}
