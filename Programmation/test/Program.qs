namespace test {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    

    @EntryPoint()
    operation SayHello() : Unit {
        using(q = Qubit()){
            H(q);
            Reset(q);
        }
        Message("Hello quantum world!");
    }
}
