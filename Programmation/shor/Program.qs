namespace shor {
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Diagnostics;


    @EntryPoint()
    operation SayHello() : Unit {
        let n_qubits = 5;
        using(q = Qubit[n_qubits + 1]){
            for(i in 0..(n_qubits-1))
            {
                H(q[i]);
            }
            X(q[n_qubits]);

            Controlled R(PauliI, 0.7, q[n_qubits]);

            DumpRegister((), q);

            for(i in 0..(n_qubits))
            {
                Reset(q[i]);                
            }

        }

        Message("Hello quantum world!");
    }
}
