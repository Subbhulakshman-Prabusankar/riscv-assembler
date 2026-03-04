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

    
























