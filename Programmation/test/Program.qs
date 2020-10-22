namespace test {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    

    @EntryPoint()
    operation SayHello() : Unit {
        using(q = Qubit()){
            CNOT(q);
            H(q);
        }
        Message("Hello quantum world!");
    }
}
