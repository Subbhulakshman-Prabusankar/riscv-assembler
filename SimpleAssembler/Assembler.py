import sys

registers = {
    'zero':'00000', 'ra':'00001', 'sp':'00010', 'gp':'00011',
    'tp':'00100',   't0':'00101', 't1':'00110', 't2':'00111',
    's0':'01000',   'fp':'01000', 's1':'01001', 'a0':'01010',
    'a1':'01011',   'a2':'01100', 'a3':'01101', 'a4':'01110',
    'a5':'01111',   'a6':'10000', 'a7':'10001', 's2':'10010',
    's3':'10011',   's4':'10100', 's5':'10101', 's6':'10110',
    's7':'10111',   's8':'11000', 's9':'11001', 's10':'11010',
    's11':'11011',  't3':'11100', 't4':'11101', 't5':'11110',
    't6':'11111',
    'x0':'00000',  'x1':'00001',  'x2':'00010',  'x3':'00011',
    'x4':'00100',  'x5':'00101',  'x6':'00110',  'x7':'00111',
    'x8':'01000',  'x9':'01001',  'x10':'01010', 'x11':'01011',
    'x12':'01100', 'x13':'01101', 'x14':'01110', 'x15':'01111',
    'x16':'10000', 'x17':'10001', 'x18':'10010', 'x19':'10011',
    'x20':'10100', 'x21':'10101', 'x22':'10110', 'x23':'10111',
    'x24':'11000', 'x25':'11001', 'x26':'11010', 'x27':'11011',
    'x28':'11100', 'x29':'11101', 'x30':'11110', 'x31':'11111'
}

instructions = {"add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and", "addi", "lw", "sltiu", "jalr", "sw","lui","auipc"}# add the instructions you guys work on here

def main():
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    if len(sys.argv) > 3:
        outputReadPath = sys.argv[3]
    else:
        outputReadPath = None

    with open(inputPath, "r") as f:
        lines = f.readlines()

    labels = {}

    pc = 0

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if ":" in line:
            label = line.split(":")[0].strip()
            labels[label] = pc
            labIns  = line.split(":", 1)[1].strip()
            if labIns != "":
                pc += 4
        else:
            pc += 4

    # rishabh build an error checking function and run the line through them and print response or proceed further.
    def check_err(instructions, registers, line):
        tokens =  line.replace(",","").split('')
        operation = tokens[0]
        
        MIN_12BIT = -2048
        MAX_12BIT = 2047
        MIN_20BIT = -1048576
        MAX_20BIT = 1048575
        
        def check_reg(reg):
            if reg in registers:
                return true
            else:
                return false

        def check_imm(val, min_val, max_val):
            try:
                num = int(val)
                return min_val <= num <= max_val
            except ValueError:
                return False

        if operation not in instructions:
            return "Invalid instruction name"
        
        if operation in RType:
            if len(tokens)!= 4:
                return "Invalid syntax"
            if not check_reg(tokens[1]) or not check_reg(tokens[2]) or not check_reg(tokens[3]):
                return "Invalid registers name"

        elif operation in {"addi", "sltiu","jalr"}:
            p = int(tokens[3])
            if len(tokens)!= 4:
                return "Invalid syntax"
            if not check_reg(tokens[1]) or not check_reg(tokens[2]): 
                return "Invalid register name"    
            if not check_imm(p,MIN_12BIT,MAX_12BIT):
                return "Invalid value(value out of range)"

        elif operation in {"lw","sw"}:
            if len(tokens)!= 3:
                return "Invalid syntax"
            if not check_reg(tokens[1]):
                return "Invalid register name"
            
            part = tokens[2]
            if "(" not in part or ")" not in part:
                return "Invalid syntax(load or store instruction)"
            
            offset , base_reg = part.replace(")","").split("(")
            p = int(offset)
            if not check_reg(base_reg):
                return "Invalid syntax(load or store instruction)"
            if not check_imm(p,MIN_12BIT,MAX_12BIT):
                return "Invalid value(offset)"

        elif operation in {"lui","auipc"}:
            p = int(tokens[2])
            if len(tokens)!= 3:
                return "Invalid syntax"
            if not check_reg(tokens[1]):
                return "Invalid register name"
            if not check_imm(p, MIN_20BIT, MAX_20BIT):
                return "Invalid value(u-type)"
            
    
    output = []
    pc = 0
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if ":" in line:
            labIns = line.split(":", 1)[1].strip()
            if labIns == "":
                continue
            ins = labIns
        else:
            ins = line
        binNum = toBin(ins, pc, labels)
        if binNum:
            output.append(binNum)
            pc += 4

    with open(outputPath, 'w') as f:
        for line in output:
            f.write(line + '\n')
    # this is temporary code

    # rishabh implement the code to write the binary string to the outputPath file.

def binaryConverter12(n):
    initial=n
    fstr=""
    if(n==0):
        return "000000000000"
    elif(n < -2048 or n > 2047):
        return "Number out of Range"
    else:
        while(n not in [0,1,-1]):
            t=str(n%2)
            istr=t
            istr+=fstr
            n=int(n/2)
            fstr=istr
    if(str(n)=="-1"):
        fstr="1"+fstr
    else:
        fstr=str(n)+fstr
    if(initial>0):
        fstr=("0"*(12-len(fstr)))+fstr
        return fstr
    else:
        fstr=("0"*(12-len(fstr)))+fstr
        for i in range(len(fstr)-1,-1,-1):
            if(fstr[i]=="1"):
                convertL=list(fstr[0:i])
                constL=list(fstr[i:])
                final=[]
                for j in convertL:
                    if(j=="0"):
                        final.append("1")
                    else:
                        final.append("0")
                break
    l=final+constL
    fstr="".join(l)
    return fstr

def intToBin(integer, bits):
    integer = int(integer)
    if integer < 0:
        integer = integer & ((1 << bits) - 1)
    return format(integer, f'0{bits}b')

def toBin(instruction, pc, labels):
    splitted = instruction.replace(",", " ").split()
    operation = splitted[0]

    RType = {
        'add': ('0000000', '000'),
        'sub': ('0100000', '000'),
        'sll': ('0000000', '001'),
        'slt': ('0000000', '010'),
        'sltu': ('0000000', '011'),
        'xor': ('0000000', '100'),
        'srl': ('0000000', '101'),
        'or': ('0000000', '110'),
        'and': ('0000000', '111'),
    }

    if operation in RType:
        rd = registers[splitted[1]]
        rs1 = registers[splitted[2]]
        rs2 = registers[splitted[3]]
        funct7, funct3 = RType[operation]
        return funct7 + rs2 + rs1 + funct3 + rd + "0110011"

    iType = {
        'addi':  ('000', '0010011'),
        'lw':    ('010', '0000011'),
        'sltiu': ('011', '0010011'),
        'jalr':  ('000', '1100111')
    }
    sType = {'sw': ('010', '0100011')}

    if operation in iType:
        funct3, opcode = iType[operation]
        if operation == 'lw':
            imm = int(splitted[2].split('(')[0])
            rs1 = registers[splitted[2].split('(')[1].strip(')')]
            rd  = registers[splitted[1]]
            return binaryConverter12(imm) + rs1 + funct3 + rd + opcode
        else:
            rd  = registers[splitted[1]]
            rs1 = registers[splitted[2]]
            imm = int(splitted[3])
            return binaryConverter12(imm) + rs1 + funct3 + rd + opcode

    if operation in sType:
        funct3, opcode = sType[operation]
        rs2     = registers[splitted[1]]
        imm     = int(splitted[2].split('(')[0])
        rs1     = registers[splitted[2].split('(')[1].strip(')')]
        imm_bin = binaryConverter12(imm)
        return imm_bin[0:7] + rs2 + rs1 + funct3 + imm_bin[7:12] + opcode

    bType = {
        'beq': '000',
        'bne': '001',
        'blt': '100',
        'bge': '101',
        'bltu': '110',
        'bgeu': '111',
    }

    if operation in bType:
        rs1 = registers[splitted[1]]
        rs2 = registers[splitted[2]]
        label2 = splitted[3]
        if label2 in labels:
            offset = labels[label2] - pc
        else:
            offset = int(label2)
        num = intToBin(offset, 13)
        return num[0] + num[2:8] + rs2 + rs1 + bType[operation] + num[8:12] + num[1] + '1100011'

    if operation == "jal":
        rd = registers[splitted[1]]
        label3 = splitted[2]
        if label3 in labels:
            offset = labels[label3] - pc
        else:
            offset = int(label3)
        num = intToBin(offset, 21)
        return num[0] + num[10:20] + num[9] + num[1:9] + rd + '1101111'

    uType = {
    'lui': '0110111',
    'auipc': '0010111',
    }
    
    if operation in uType:
        rd  = registers[splitted[1]]
        imm = int(splitted[2])
        imm_bin = intToBin(imm,20)
        return imm_bin + rd + uType[operation] 

if __name__ == "__main__":

    main()
