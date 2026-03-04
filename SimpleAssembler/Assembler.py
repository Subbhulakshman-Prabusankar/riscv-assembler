import sys

registers = {} # nishaanth fill the registers here

instructions = {"add", "sub", "slt", "sltu", "xor", "sll", "srl", "or", "and"}# add the instructions you guys work on here

def main():
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    if len(sys.argv) > 3:
        outputReadPath = sys.argv[3]
    else:
        outputReadPath = None

    f = open(inputPath, "r")
    lines = f.readlines()

    labels = {}

    pc = 0

    for line in lines:
        line = line.strip()
        if line == " ":
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

    output = ""
    pc = 0
    for line in lines:
        line = line.strip()
        if line == " ":
            continue
        if ":" in line:
            labIns = line.split(":", 1)[1].strip()
            if labIns == "":
                continue
            ins = labIns
        binNum = toBin(ins, pc, labels)
        if binNum:
            output.append(binNum)
            pc += 4

    # rishabh implement the code to write the binary string to the outputPath file.

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

    # nishaanth add the i and s type here (refer to the r type for variables and format)
    # nithilan add b and j type here
    # rishabh add u type here

    









