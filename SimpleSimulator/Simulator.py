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
    value=value & 0xFFFFFFFF
    if(value & 0x80000000):
        value-=0x100000000
    return value

def immI(ins):
    immBits=ins[0:12]
    imm=int(immBits, 2)
    return convInt(imm, 12)

def immS(ins):
    immBits=ins[0:7]+ins[20:25]
    imm=int(immBits, 2)
    return convInt(imm, 12)

#nithilan
def immB(ins):
    p=""
    p+=ins[0]
    p+=ins[24]
    p+=ins[1:7]
    p+=ins[20:24]
    p+="0"
    return convInt(int(p, 2), 13)
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

    def addnew(num, value):
        if num != 0:
            register[num] = value & 0xFFFFFFFF

    def memRead(address):
        if address in memory2:
            return memory2[address]
        return 0

    def memWrite(address, value):
        memory2[address] = value & 0xFFFFFFFF

    def output():
        x = ["0b" + format(PC, "032b")]
        num = 0
        while num < 32:
            x.append("0b" + conv32(register[num]))
            num +=1
        outputs.append(" ".join(x) + " ")

    counter = 0
    while counter < 100000:
        if PC not in memoty:
            break

        one = decode(memoty[PC])
        opcode = one["opcode"]
        rd = one["rd"]
        rs1 = one["rs1"]
        rs2 = one["rs2"]
        funct3 = one["funct3"]
        funct7 = one["funct7"]

        PCnext = PC + 4

        isHalt = False

        #me
        if opcode == "0110011":
            val1 = get(rs1)
            val2 = get(rs2)

            sig1 = convSinged32(val1)
            sig2 = convSinged32(val2)

            if funct3 == "000" and funct7 == "0000000":
                result = sig1 + sig2
                addnew(rd, result)

            elif funct3 == "000" and funct7 == "0100000":
                result =sig1- sig2
                addnew(rd, result)

            elif funct3 == "001":
                shift = val2 & 0x1F
                result = val1 << shift
                addnew(rd, result)

            elif funct3 == "010":
                if sig1< sig2:
                    addnew(rd, 1)
                else:
                    addnew(rd, 0)

            elif funct3 == "011":
                if val1 < val2:
                    addnew(rd, 1)
                else:
                    addnew(rd, 0)

            elif funct3 == "100":
                result = val1 ^ val2
                addnew(rd, result)

            elif funct3 == "101" and funct7 == "0000000":
                shift = val2 & 0x1F
                result = val1 >> shift
                addnew(rd, result)

            elif funct3 == "110":
                result = val1 | val2
                addnew(rd, result)

            elif funct3 == "111":
                result = val1 & val2
                addnew(rd, result)
        #--
        #nishaanth addi, sltiu, lw, sw
        elif opcode == "0010011":
            imm=immI(memoty[PC])
            if(funct3=="000"):
                result=convSinged32(get(rs1))+imm #eda missed the singed thing for -ve int here fix
                addnew(rd, result)

            elif(funct3=="011"):
                val1=get(rs1) & 0xFFFFFFFF
                val2=imm & 0xFFFFFFFF 
                if(val1 < val2):
                    addnew(rd, 1)
                else:
                    addnew(rd, 0)

        elif opcode =="0000011":
            if(funct3=="010"):
                imm=immI(memoty[PC])
                address=(convSinged32(get(rs1)) + imm) & 0xFFFFFFFF#here asw
                value=memRead(address)
                addnew(rd, value)

        elif opcode == "0100011":
            if(funct3=="010"):
                imm=immS(memoty[PC])
                address = (convSinged32(get(rs1)) +imm) & 0xFFFFFFFF #here asw
                memWrite(address, get(rs2))
        #--
        #nithilan branch + halt
        elif opcode == "1100011":
            imm = immB(memoty[PC])
            if (rs1 == 0 and rs2 == 0 and imm == 0):
                output()
                isHalt = True
            elif (funct3 == "000"):
                if (get(rs1) == get(rs2)):
                    PCnext = PC + imm
            elif (funct3 == "001"):
                if (get(rs1) != get(rs2)):
                    PCnext = PC + imm
            elif (funct3 == "100"):
                if (convSinged32(get(rs1)) < convSinged32(get(rs2))):
                    PCnext = PC + imm
            elif (funct3 == "101"):
                if (convSinged32(get(rs1)) >= convSinged32(get(rs2))):
                    PCnext = PC + imm
            elif (funct3 == "110"):
                if (get(rs1) < get(rs2)):
                    PCnext = PC + imm
            elif (funct3 == "111"):
                if (get(rs1) >= get(rs2)):
                    PCnext = PC + imm

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
        address = stkMemStart + (num*4)
        value = 0
        if address in memory2:
            value = memory2[address]
        f.write("0x" + format(address, "08X") + ":0b" + conv32(value) + "\n")
        num += 1
    f.close()

if __name__ == "__main__":
    main()













