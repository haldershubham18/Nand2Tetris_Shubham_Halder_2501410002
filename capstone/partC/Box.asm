// Box.asm  --  Shubham Halder, Roll 2501410002, K = 02
// While any key is pressed: black box (rows 2..21, 48 px wide = 3 words,
// from the left edge). Key released: box disappears.
//
// Row r starts at SCREEN + 32*r. K = 2  ->  SCREEN + 64.

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE          // any key -> go black
    @val
    M=0            // no key -> white
    @PAINT
    0;JMP
(PRESSED)
    @val
    M=-1           // all 16 bits set = black
(PAINT)
    @SCREEN
    D=A
    @64            // 32 * K  (K = 2)
    D=D+A
    @addr
    M=D            // addr = start of row K
    @20
    D=A
    @rows
    M=D            // rows left = 20
(ROW)
    @val
    D=M
    @addr
    A=M
    M=D            // word 0
    A=A+1
    M=D            // word 1
    A=A+1
    M=D            // word 2  (3 words = 48 px)
    @32
    D=A
    @addr
    M=D+M          // next row = addr + 32
    @rows
    MD=M-1
    @ROW
    D;JGT
    @LOOP
    0;JMP
