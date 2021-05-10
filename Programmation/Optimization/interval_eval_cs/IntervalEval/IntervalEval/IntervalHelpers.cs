using System;
using System.Collections.Generic;
using System.Linq;
using IntSharp.Types;
using IntSharp;
namespace IntervalEval
{
    public static class IntervalHelpers
    {
        private static readonly double XLogMin = System.Math.Exp(-1);
        private const double ZeroPrecision = 1e-05;

        /** Custom method to evaluate f(x) = x*log(x) with f(0) = 0 instead of f(0) = -oo */
        public static Interval XLog(Interval it)
        {
            // x \in [-oo, 0] => no result
            if (it.Supremum <= ZeroPrecision)
            {
                return Interval.Zero;
            }
            // x \in [0+, exp(-1)] => y strictly decreasing
            if (it.Supremum <= XLogMin && it.Infimum > ZeroPrecision)
            {
                return Interval.FromInfSup(it.Supremum * System.Math.Log(it.Supremum), it.Infimum * System.Math.Log(it.Infimum));
            }
            // x \in [0-, exp(-1)] => y strictly decreasing and max(y) = 0
            if (it.Infimum <= ZeroPrecision && it.Supremum <= XLogMin)
            {
                return Interval.FromInfSup(it.Supremum * System.Math.Log(it.Supremum), 0);
            }
            // x \in [0+, +oo], x <= exp(-1)  => y increases then decreases
            if (it.Infimum <= XLogMin && it.Supremum >= XLogMin && it.Infimum >= ZeroPrecision)
            {
                return Interval.FromInfSup(XLogMin * System.Math.Log(XLogMin),
                    System.Math.Max(it.Infimum * System.Math.Log(it.Infimum), it.Supremum * System.Math.Log(it.Supremum)));
            }
            // x \in [0-, +00], x <= exp(-1) => y increases then decreases
            if (it.Infimum <= XLogMin && it.Supremum >= XLogMin && it.Infimum <= ZeroPrecision)
            {
                return Interval.FromInfSup(XLogMin * System.Math.Log(XLogMin),
                    System.Math.Max(0.0, it.Supremum * System.Math.Log(it.Supremum)));
            }
            // x \in [exp(-1), +oo] => y strictly increasing
            if (it.Infimum >= XLogMin)
            {
                return Interval.FromInfSup(it.Infimum * System.Math.Log(it.Infimum), it.Supremum * System.Math.Log(it.Supremum)); 
            }
            // No solution otherwise
            return Interval.Zero;
        }
        
        public static Tuple<IEnumerable<Interval>, IEnumerable<Interval>> Bisect(this IEnumerable<Interval> input)
        {
            var enumerable = input as List<Interval> ?? input.ToList();
            var largestWidth = enumerable[0].Diam();
            var largest = enumerable[0];
            foreach (var interval in enumerable.Where(interval => interval.Diam() >= largestWidth))
            {
                largestWidth = interval.Diam();
                largest = interval;
            }
            var (left, right) = largest.Bisect();
            var bisectIndex = enumerable.IndexOf(largest);
            var rightBox = enumerable.ToList();
            var leftBox = enumerable.ToList();
            rightBox[bisectIndex] = right;
            leftBox[bisectIndex] = left;
            return new Tuple<IEnumerable<Interval>, IEnumerable<Interval>>(leftBox, rightBox);
        }
        
        public static bool Contains(this Interval it, double value)
        {
            return it.Infimum <= value && it.Supremum >= value;
        }

        public static double MaxWidth(this IEnumerable<Interval> input)
        {
            var enumerable = input as List<Interval> ?? input.ToList();
            if (enumerable.Count == 0) return 0.0;
            var largestWidth = enumerable[0].Diam();
            foreach (var interval in enumerable.Where(interval => interval.Diam() >= largestWidth))
                largestWidth = interval.Diam();

            return largestWidth;
        }

        public static double MaxWidth(this IEnumerable<IEnumerable<Interval>> listOfVariables)
        {
            var enumerable = listOfVariables as List<IEnumerable<Interval>> ?? listOfVariables.ToList();
            if (enumerable.Count == 0) return 0.0;
            var largestWidth = enumerable[0].MaxWidth();
            foreach (var intervals in enumerable.Where(interval => MaxWidth(interval) >= largestWidth))
                largestWidth = intervals.MaxWidth();
            return largestWidth;
        }
        
        public static void Print(IEnumerable<Interval> its)
        {
            Console.Write("[");
            foreach (var interval in its)
            {
                Console.Write($"[{interval.Infimum}, {interval.Supremum}]");
            }
            Console.WriteLine("]");
        }
        
        public static void Print(Interval it)
        {
            Console.WriteLine($"[{it.Infimum}, {it.Supremum}]");
        }

    }
}