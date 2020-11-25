namespace Qrng{
    open Microsoft.Quantum.Intrinsic;

    operation SampleRngGenerator(): Result {
        using (q = Qubit()){
            H(q);
            let r = M(q);
            Reset(q);
            return r;
        }
    }
}