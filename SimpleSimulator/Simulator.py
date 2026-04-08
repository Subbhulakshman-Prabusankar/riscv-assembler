import sys

stkPInit = 0x0000017C
stkMemStart = 0x00010000

def conv32(value):
    value = value & 0xFFFFFFFf
    return format(value, '032b')

def convInt(value, bits):
    if value & (1 << (bits - 1)):
        value -= (1 << bits)
    return value

def decode(ins):
    result = {}

    opcode = ""
    for i in range(25, 32):
        opcode += ins[i]
    result["opcode"] = opcode

    rd = ""
    for i in range(20, 25):
        rd += ins[i]
    result["rd"] = int(rd, 2)

    funct3 = ""
    for i in range(17, 20):
        funct3 += ins[i]
    result["funct3"] = funct3

    rs1 = ""
    for i in range(12, 17):
        rs1 += ins[i]
    result["rs1"] = int(rs1, 2)

    rs2 = ""
    for i in range(7, 12):
        rs2 += ins[i]
    result["rs2"] = int(rs2, 2)

    funct7 = ""
    for i in range(0, 7):
        funct7 += ins[i]
    result["funct7"] = funct7

    return result
# ALL THE FUNCTIONS YOU YOURSELF WILL NEED ARE IN HERE SO LIJE MAKE THEM THEN YOU CAN USE IT FOR YOUR code down below at bottom of file
#nishaanth
def convSinged32(value):
    pass

def immI(ins):
    pass

def immS(ins):
    pass
#------
#nithilan
def immB(ins):
    pass
#------
#rishabh
def immU(ins):
    pass

def immJ(ins):
    pass
#------
def main():
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]

    f = open(inputPath, "r")
    readed = f.readlines()
    f.close()

    lines = []
    for line in readed:
        line = line.strip()
        if line != "":
            lines.append(line)

    memoty = {}

    address = 0

    for line in lines:
        memoty[address] = line
        address += 4

    register = [0] * 32
    register[2] = stkPInit

    memory2 = {}
    num = 0
    while num < 32:
        memory2[stkMemStart + (num*4)] = 0
        num += 1

    PC = 0
    outputs = []

    def get(i):
        return register[i]

    def add(num, value):
        if num != 0:
            register[num] = value & 0xFFFFFFFF

    def memRead(address):
        if address in memoty:
            return memoty[address]
        return 0

    def memWrite(address, value):
        memoty[address] = value & 0xFFFFFFFF

    def output():
        x = ["0b" + format(PC, "032b")]
        num = 0;
        while num < 32:
            x.append("0b" + conv32(register[num]))
            num +=1
        outputs.append(" ".join(x) + " ")

    counter = 0
    while counter < 100000:
        if PC not in memoty:
            break

        opcode = decode(memoty[PC])["opcode"]
        rd = decode(memoty[PC])["rd"]
        rs1 = decode(memoty[PC])["rs1"]
        rs2 = decode(memoty[PC])["rs2"]
        funct3 = decode(memoty[PC])["funct3"]
        funct7 = decode(memoty[PC])["funct7"]

        PCnext = PC + 4

        isHalt = False

        #me
        if opcode == "0110011":
            pass
        #--
        #nishaanth addi, sltiu, lw, sw
        elif opcode == "0010011":
            pass

        elif opcode == "0000011":
            pass

        elif opcode == "0100011":
            pass
        #--
        #nithilan branch + halt
        elif opcode == "1100011":
            pass
        #--
        #rishabh jalr, jal, lui, auipc
        elif opcode == "1100111":
            pass

        elif opcode == "1101111":
            pass

        elif opcode == "0110111":
            pass

        elif opcode == "0010111":
            pass

        if isHalt == True:
            break

        PC = PCnext
        output()
        counter +=1

    f = open(outputPath, "w")
    num = 0
    while num < len(outputs):
        f.write(outputs[num] + "\n")
        num += 1

    num = 0

    while num < 32:
        address = 32 + (num*4)
        value = 0
        if address in memory2:
            value = memory2[address]
        f.write("0x" + format(address, "08X") + ":0b" + conv32(value) + "\n")
        num += 1
    f.close()

if __name__ == "__main__":
    main()













