"""
Hack Assembler (Nand2Tetris Capstone)
Name: Shubham Halder | Roll No: 2501410002 | K = 02
Extra feature (K mod 3 = 2): warn when the same label is defined twice.

Usage: python assembler.py Prog.asm   ->  writes Prog.hack
"""
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}


def predefined():
    t = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
         "SCREEN": 16384, "KBD": 24576}
    t.update({f"R{i}": i for i in range(16)})
    return t


def clean(line):
    """Strip comments and all whitespace."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def first_pass(lines, table):
    """Record where each (LABEL) points. Labels don't take a ROM slot."""
    rom = 0
    seen = {}  # label -> source line number where first defined
    for num, raw in enumerate(lines, 1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if label in seen:
                # EXTRA FEATURE (K mod 3 == 2): duplicate label warning
                print(f"Warning: Line {num}: label '{label}' already defined "
                      f"on line {seen[label]} (keeping the first one)",
                      file=sys.stderr)
            else:
                seen[label] = num
                table[label] = rom
        else:
            rom += 1


def second_pass(lines, table):
    """Translate every instruction to 16 bits. New variables start at 16."""
    out = []
    next_var = 16
    for raw in lines:
        line = clean(raw)
        if not line or line.startswith("("):
            continue
        if line.startswith("@"):
            sym = line[1:]
            if sym.isdigit():
                addr = int(sym)
            else:
                if sym not in table:
                    table[sym] = next_var
                    next_var += 1
                addr = table[sym]
            out.append(f"{addr:016b}")
        else:
            dest, comp, jump = "", line, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)
            out.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
    return out


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        print("Usage: python assembler.py Prog.asm")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        lines = f.read().splitlines()
    table = predefined()
    first_pass(lines, table)
    code = second_pass(lines, table)
    out_path = path[:-4] + ".hack"
    with open(out_path, "w") as f:
        f.write("\n".join(code) + "\n")
    print(f"Wrote {len(code)} instructions to {out_path}")


if __name__ == "__main__":
    main()
