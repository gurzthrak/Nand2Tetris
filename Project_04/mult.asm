// Mult.asm
// Multiplies R0 and R1 and stores the result in R2.

// Initialize R2 (result) to 0
@R2
M=0

// Load R0 into D (this will be our base number for repeated addition)
@R0
D=M

// Main multiplication loop
(LOOP)
    // Check if R1 (our counter) is 0
    @R1
    D=M
    @STOP
    D;JEQ  // If R1 is 0, we're done, so jump to STOP

    // Add R0 to our running total in R2
    @R0
    D=M
    @R2
    M=M+D

    // Decrement R1 (our counter)
    @R1
    M=M-1

    // Jump back to start of loop
    @LOOP
    0;JMP

(STOP)
    // Program end
    @STOP
    0;JMP
