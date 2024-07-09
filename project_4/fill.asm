(LOOP)
    @KBD
    D=M        // D = key pressed (or 0 if no key)
    @BLACK
    D;JNE      // If D ≠ 0 (key pressed), goto BLACK
    @WHITE
    0;JMP      // else, goto WHITE

(BLACK)
    @color
    M=-1       // Set color to black (-1)
    @FILL
    0;JMP

(WHITE)
    @color
    M=0        // Set color to white (0)

(FILL)
    @SCREEN
    D=A        // D = screen base address
    @8192      // number of 16-bit words in the screen
    D=D+A      // D = address after the last screen word
    @i
    M=D        // i = address after last screen word

(FILL_LOOP)
    @i
    D=M-1
    M=D        // Decrement i
    @LOOP
    D;JLT      // If i < 0, go back to main loop

    @color
    D=M        // D = current color
    @i
    A=M        // A = current screen word address
    M=D        // Set word to current color

    @FILL_LOOP
    0;JMP      // Continue filling
