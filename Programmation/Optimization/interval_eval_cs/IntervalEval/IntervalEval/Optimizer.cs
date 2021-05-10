using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using IntSharp.Types;

namespace IntervalEval
{
    public enum OptimizationType
    {
        Minimization = 0,
        Maximization = 1
    }
    
    public static class Optimizer
    {
        public static readonly TypeListener<int> OptimizationIterations = new();
        
        /*
        private static void Optimize(IEnumerable<Interval> variables, OptimizationType optimizationType = OptimizationType.Minimization, double precision=1e-07)
        {
            var vars = new List<IEnumerable<Interval>>();
        
            vars.Add(variables);
            for (int iter = 0; iter < 2; iter++)
            {
                Console.WriteLine($"Iteration {iter}");
                var stopwatchGlobal = new Stopwatch();
                stopwatchGlobal.Start();
                var newVar = new List<IEnumerable<Interval>>();
                var stopwatch = new Stopwatch();
                foreach (var variableList in vars)
                {
                    var bisectLeft = new List<Interval>();
                    var bisectRight = new List<Interval>();
                    foreach (var interval in variableList)
                    {
                        var (left, right) = interval.Bisect();
                        bisectLeft.Add(left);
                        bisectRight.Add(right);
                    }
                    newVar.Add(bisectLeft);
                    newVar.Add(bisectRight);
                }
                vars.Clear();
                
                var res = CartesianProduct(Transpose(newVar));
                Console.WriteLine($"res.length = {res.Count()}");
                Console.WriteLine("****");
                foreach (var enumerable in res)
                {
                    Print(enumerable);
                }
                Console.WriteLine("****");
                
                var correct = new List<IEnumerable<Interval>>();
                var mutex = new Mutex();
                stopwatch.Restart();
                Parallel.ForEach(res, enumerable =>
                {
                    var resultConstraints = Constraint(enumerable);
                    if (!resultConstraints)
                    {
                        mutex.WaitOne();
                        Console.Write("Not correct: ");
                        Print(enumerable);
                        mutex.ReleaseMutex();
                    }
                    mutex.WaitOne();
                    if (resultConstraints && !Contains(correct, enumerable))
                    {
                        correct.Add(enumerable);
                    }
                    mutex.ReleaseMutex();
                });
                stopwatch.Stop();
                Console.WriteLine($"Correct.size = {correct.Count()}");
                Console.WriteLine($"Delta time Constraints: {stopwatch.ElapsedMilliseconds}");
        
                var keep = new List<IEnumerable<Interval>>();
                var previous = correct.Count;
        
                stopwatch.Restart();
                // Parallel evaluation of function to remove upper / lower bounded values (depending on min or max)
                Parallel.For(0, correct.Count, i =>
                {
                    var valueFunctionI = Function(correct[i]);
                    var ok = true;
                    var mutexOk = new Mutex();
                    Parallel.For(0, correct.Count, (j, state) =>
                    {
                        var valueFunctionJ = Function(correct[j]);
                        if (i == j) return;
                        mutexOk.WaitOne();
                        switch (optimizationType)
                        {
                            case OptimizationType.Minimization:
                                if (valueFunctionI.Infimum > valueFunctionJ.Supremum) ok = false;
                                break;
                            case OptimizationType.Maximization:
                                if (valueFunctionI.Supremum < valueFunctionJ.Infimum) ok = false;
                                break;
                        }
                        mutexOk.ReleaseMutex();
                        if (!ok) state.Break();
                    });
                    mutexOk.Close();
        
                    mutex.WaitOne();
                    if(ok && !Contains(keep, correct[i])) keep.Add(correct[i]);
                    mutex.ReleaseMutex();
                });
                mutex.Close();
                stopwatch.Stop();
                Console.WriteLine($"Delta time Function Eval: {stopwatch.ElapsedMilliseconds}");
        
                correct.Clear();
                vars = keep;
                Console.WriteLine($"vars.Count = {vars.Count}");
                Console.WriteLine($"Eliminated box amount = {previous - vars.Count}");
                stopwatchGlobal.Stop();
                Console.WriteLine($"Delta time Total: {stopwatchGlobal.ElapsedMilliseconds}");
                Console.WriteLine("==========");
                
            }
            
            Console.WriteLine(vars.Count);
        }
        */
        
        /// <summary>
        /// Launches an optimization operation.
        /// </summary>
        /// <param name="variables">List of variables as input of the problem. Define them as initial interval for the problem</param>
        /// <param name="function">The function to be optimized</param>
        /// <param name="constraints">Constraint function applied to variables</param>
        /// <param name="optimizationType">Are we maximizing or minimizing ? Defaults to minimization</param>
        /// <param name="iterations">Number of iterations for the optimization. Defaults to 1</param>
        /// <param name="debug">If true, prints additional debug information to console.</param>
        /// <param name="token">Cancels the running optimization if asked.</param>
        /// <returns>List of reduced intervals as solution</returns>
        public static IEnumerable<IEnumerable<Interval>> Optimize(
            IEnumerable<Interval> variables, 
            Func<IEnumerable<Interval>, Interval> function,
            Func<IEnumerable<Interval>, bool> constraints,
            OptimizationType optimizationType = OptimizationType.Minimization, 
            int iterations = 1, 
            bool debug = false,
            CancellationToken token = default
            )
        {
            if(debug) Console.WriteLine(optimizationType == OptimizationType.Minimization ? "Min" : "Max");
            var enumerable = variables as Interval[] ?? variables.ToArray();
            // List of current leaves to be processed
            var currentList = new List<IEnumerable<Interval>> {enumerable};

            for (OptimizationIterations.Value = 0; OptimizationIterations.Value <= iterations; OptimizationIterations.Value++)
            {
                if (token.IsCancellationRequested) return new List<IEnumerable<Interval>>(); // Cancel operation if asked
                if(debug) Console.WriteLine($"Iteration {OptimizationIterations.Value}");
                // New list of leaves
                var nextList = new List<IEnumerable<Interval>>();
                var listImages = new List<Interval>();
                // Process each leaf in the list
                foreach (var intervals in currentList)
                {
                    if (token.IsCancellationRequested) return new List<IEnumerable<Interval>>(); // Cancel operation if asked
                    // Bisect the leaf, and check constraints. If the resulting intervals matches constraints,
                    // add them to the new list of leaves, otherwise throw them out.
                    var (leftIt, rightIt) = intervals.Bisect();
                    if (constraints(leftIt))
                    {
                        nextList.Add(leftIt);
                        // Compute image of leaf
                        listImages.Add(function(leftIt));
                    }
                    else
                    {
                        if(debug) Console.Write("Removing out-constrained interval ");
                        if(debug) IntervalHelpers.Print(leftIt);
                    }
                    if (constraints(rightIt))
                    {
                        nextList.Add(rightIt);
                        // Compute image of leaf
                        listImages.Add(function(rightIt));
                    }
                    else
                    {
                        if(debug) Console.Write("Removing out-constrained interval ");
                        if(debug) IntervalHelpers.Print(rightIt);
                    }
                }
                var correctList = new List<IEnumerable<Interval>>();
                // Remove out of bounds leaves 
                for (var i = 0; i < nextList.Count; i++)
                {
                    if (token.IsCancellationRequested) return new List<IEnumerable<Interval>>(); // Cancel operation if asked
                    var ok = true;
                    var valueFunctionI = listImages[i];
                    // Check if leaf valueFunctionI has any leaf strictly superior to it (minimization) or
                    // strictly inferior to it (maximization). If so, discard it.
                    for (var j = 0; j < nextList.Count; j++)
                    {
                        if (i != j)
                        {
                            var valueFunctionJ = listImages[j];
                            switch (optimizationType)
                            {
                                case OptimizationType.Minimization:
                                    if (valueFunctionI.Infimum > valueFunctionJ.Supremum) ok = false;
                                    break;
                                case OptimizationType.Maximization:
                                    if (valueFunctionI.Supremum < valueFunctionJ.Infimum) ok = false;
                                    break;
                                default:
                                    if(debug) Console.WriteLine($"Warning: incorrect optimization type {optimizationType}");
                                    break;
                            }
                        }
                        if (!ok) break;
                    }
                    
                    // If not out of bounds, keep it
                    if (ok) correctList.Add(nextList[i]);
                    else
                    {
                        if(debug) Console.Write("Removing outbound interval ");
                        if(debug) IntervalHelpers.Print(nextList[i]);
                    }
                }
                // Assign new list of leaves to the current one, and follow with new processing
                currentList.Clear();
                currentList = correctList;

                if(debug) {
                    foreach (var intervals in currentList)
                    {
                        IntervalHelpers.Print(intervals);
                    }
                }
                if(debug) Console.WriteLine("==========");
            }

            return currentList;
        }
    }
}