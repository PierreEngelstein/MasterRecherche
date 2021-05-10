using System;
using System.Collections.Generic;
using System.Linq;
using IntSharp;
using IntSharp.Types;

namespace IntervalEval
{
    public class ProblemDescriptor
    {
        private string ProblemFunctionDescription { get; init; }
        private string ProblemConstraintsDescription { get; init; }
        
        public Func<IEnumerable<Interval>, Interval> Function { get; private init; }
        public Func<IEnumerable<Interval>, bool> Constraints { get; private init; }

        public override string ToString()
        {
            return
                $"{ProblemFunctionDescription}{(string.IsNullOrEmpty(ProblemConstraintsDescription) ? $" ; {ProblemConstraintsDescription}" : "")}";
        }
        
        private static ProblemDescriptor ProblemX1X2 => new()
        {
            ProblemFunctionDescription = "f(x1, x2) = x1 + x2",
            ProblemConstraintsDescription = "x1² + x2² = 1",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 2 ? Interval.FromInfSup(double.NaN, double.NaN) : listVars[0] + listVars[1];
            },
            Constraints = variables =>
            {
                var enumerable = variables as Interval[] ?? variables.ToArray();
                if (enumerable.Length != 2)
                {
                    return false;
                }
                var listVars = enumerable.ToList();
                var result = IntSharp.Math.Sqr(listVars[0]) + IntSharp.Math.Sqr(listVars[1]) - 1.0;
                return result.Contains(0.0);
            }
        };
        
        private static ProblemDescriptor ProblemX1X2Square => new()
        {
            ProblemFunctionDescription = "f(x1, x2) = (x1 + x2)²",
            ProblemConstraintsDescription = "x1² + x2² = 1",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 2 ? Interval.FromInfSup(double.NaN, double.NaN) : IntSharp.Math.Sqr(listVars[0] + listVars[1]);
            },
            Constraints = variables =>
            {
                var enumerable = variables as Interval[] ?? variables.ToArray();
                if (enumerable.Length != 2)
                {
                    return false;
                }
                var listVars = enumerable.ToList();
                var result = IntSharp.Math.Sqr(listVars[0]) + IntSharp.Math.Sqr(listVars[1]) - 1.0;
                return result.Contains(0.0);
            }
        };
        
        private static ProblemDescriptor ProblemX1SqrX2 => new()
        {
            ProblemFunctionDescription = "f(x1, x2) = x1²x2",
            ProblemConstraintsDescription = "x1² + x2² = 3",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 2 ? Interval.FromInfSup(double.NaN, double.NaN) : IntSharp.Math.Sqr(listVars[0]) * listVars[1];
            },
            Constraints = variables =>
            {
                var enumerable = variables as Interval[] ?? variables.ToArray();
                if (enumerable.Length != 2)
                {
                    return false;
                }
                var listVars = enumerable.ToList();
                var result = IntSharp.Math.Sqr(listVars[0]) + IntSharp.Math.Sqr(listVars[1]) - 3.0;
                return result.Contains(0.0);
            }
        };
        private static ProblemDescriptor ProblemXLogX1 => new()
        {
            ProblemFunctionDescription = "f(x1, x2) = x1*log(x1) + x2 * log(x2)",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 2 ? Interval.FromInfSup(double.NaN, double.NaN) : IntervalHelpers.XLog(listVars[0]) + IntervalHelpers.XLog(listVars[1]);
            },
            Constraints = _ => true
        };
        
        private static ProblemDescriptor ProblemXLogX2 => new()
        {
            ProblemFunctionDescription = "f(x1, x2) = (x1 + x2) * log(x1 + x2) + (x1 - x2) * log(x1 - x2)",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 2 ? Interval.FromInfSup(double.NaN, double.NaN) : IntervalHelpers.XLog(listVars[0] + listVars[1]) + IntervalHelpers.XLog(listVars[0] - listVars[1]);
            },
            Constraints = _ => true
        };
        
        private static ProblemDescriptor ProblemXLogX3 => new()
        {
            ProblemFunctionDescription = "f(x1, x2, x3) = (x1 + x2) * log(x1 + x2) + (x1 - x3) * log(x1 - x3)",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 3 ? Interval.FromInfSup(double.NaN, double.NaN) : IntervalHelpers.XLog(listVars[0] + listVars[1]) + IntervalHelpers.XLog(listVars[0] - listVars[2]);
            },
            Constraints = _ => true
        };

        private static ProblemDescriptor ProblemMutualInformation => new()
        {
            ProblemFunctionDescription = "Mutual Information",
            ProblemConstraintsDescription = "",
            Function = variables =>
            {
                var listVars = variables.ToList();
                return listVars.Count != 3 ? 
                    Interval.FromInfSup(double.NaN, double.NaN) : 
                    IntervalHelpers.XLog(listVars[0] + listVars[1]) + IntervalHelpers.XLog(listVars[0] - listVars[2]);
            },
            Constraints = variables =>
            {
                var enumerable = variables as Interval[] ?? variables.ToArray();
                if (enumerable.Length != 3)
                {
                    return false;
                }
                
                var listVars = enumerable.ToList();
                if (listVars[0].Diam() >= Interval.FromInfSup(0, 1).Diam() ||
                    listVars[1].Diam() >= Interval.FromInfSup(-1, 1).Diam() ||
                    listVars[2].Diam() >= Interval.FromInfSup(0, 1).Diam())
                {
                    return true;
                }
                // Bounds
                var result1 = listVars[0] >= 0;
                var result2 = listVars[0] <= 0.5;
                var result3 = listVars[1] >= -1;
                var result4 = listVars[1] <= 1;
                var result5 = listVars[2] >= 0;
                var result6 = listVars[2] <= 1;
                // Positive Semi-Definite
                var result7 = listVars[0] * listVars[2] - IntSharp.Math.Sqr(listVars[1]) >= 0;
                var result8 = (1 - listVars[0]) * (1 - listVars[2]) - IntSharp.Math.Sqr(1 - listVars[1]) >= 0;
                return result1 && result2 && result3 && result4;
            }
        };

        public static readonly List<ProblemDescriptor> Problems2D = new()
        {
            ProblemX1X2Square,
            ProblemX1X2,
            ProblemX1SqrX2,
            ProblemXLogX1,
            ProblemXLogX2
        };

        public static readonly List<ProblemDescriptor> Problems3D = new()
        {
            ProblemXLogX3,
            ProblemMutualInformation
        };
    }
}