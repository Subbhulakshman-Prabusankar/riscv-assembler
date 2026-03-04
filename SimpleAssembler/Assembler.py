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
        binNum = toBin(ins, pc, label)
        if binNum:
            output.append(binNum)
            pc += 4



def toBin(instruction, pc, label):
    return 1










