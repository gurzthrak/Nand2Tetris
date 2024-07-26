import sys

# Define the instruction code mappings
comp_codes = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
    'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
    '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101'
}

dest_codes = {
    '': '000', 'M': '001', 'D': '010', 'MD': '011',
    'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'
}

jump_codes = {
    '': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
    'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'
}

# Initialize symbol table with predefined symbols
symbol_table = {
    'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
    'SCREEN': 16384, 'KBD': 24576
}

def parse_a_instruction(instruction, line_number):
    value = instruction[1:]
    if value.isdigit():
        return format(int(value), '016b')
    elif value in symbol_table:
        return format(symbol_table[value], '016b')
    else:
        raise ValueError(f"Undefined symbol '{value}' at line {line_number}")

def parse_c_instruction(instruction):
    dest, comp, jump = '', '', ''
    if '=' in instruction:
        dest, instruction = instruction.split('=')
    if ';' in instruction:
        comp, jump = instruction.split(';')
    else:
        comp = instruction
    
    if comp not in comp_codes:
        raise ValueError(f"Invalid computation '{comp}'")
    if dest not in dest_codes:
        raise ValueError(f"Invalid destination '{dest}'")
    if jump not in jump_codes:
        raise ValueError(f"Invalid jump '{jump}'")
    
    return f'111{comp_codes[comp]}{dest_codes[dest]}{jump_codes[jump]}'

def first_pass(input_file):
    address = 0
    with open(input_file, 'r') as file:
        for line in file:
            line = line.split('//')[0].strip()
            if line:
                if line.startswith('(') and line.endswith(')'):
                    symbol = line[1:-1]
                    symbol_table[symbol] = address
                else:
                    address += 1

def assemble(input_file, output_file):
    try:
        first_pass(input_file)
        variable_address = 16

        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line_number, line in enumerate(infile, 1):
                line = line.split('//')[0].strip()
                if line and not (line.startswith('(') and line.endswith(')')):
                    try:
                        if line.startswith('@'):
                            value = line[1:]
                            if not value.isdigit() and value not in symbol_table:
                                symbol_table[value] = variable_address
                                variable_address += 1
                            binary = parse_a_instruction(line, line_number)
                        else:
                            binary = parse_c_instruction(line)
                        outfile.write(binary + '\n')
                    except ValueError as e:
                        print(f"Error at line {line_number}: {e}")
                        return

        print(f"Assembly completed. Output written to {output_file}")

    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except PermissionError:
        print(f"Permission denied when accessing {input_file} or {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python assembler.py input.asm output.hack")
    else:
        input_file, output_file = sys.argv[1], sys.argv[2]
        assemble(input_file, output_file)

