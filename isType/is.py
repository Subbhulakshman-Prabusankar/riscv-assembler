registers={

    #ABI names
    "zero":"00000", "ra":"00001", "sp":"00010", "gp":"00011",
     "tp":"00100", "t0":"00101", "t1":"00110", 't2':'00111',
    's0':'01000',   'fp':'01000', 's1':'01001', 'a0':'01010',
    'a1':'01011',   'a2':'01100', 'a3':'01101', 'a4':'01110',
    'a5':'01111',   'a6':'10000', 'a7':'10001', 's2':'10010',
    's3':'10011',   's4':'10100', 's5':'10101', 's6':'10110',
    's7':'10111',   's8':'11000', 's9':'11001', 's10':'11010',
    's11':'11011',  't3':'11100', 't4':'11101', 't5':'11110',
    't6':'11111',

    #register names
    'x0':'00000',  'x1':'00001',  'x2':'00010',  'x3':'00011',
    'x4':'00100',  'x5':'00101',  'x6':'00110',  'x7':'00111',
    'x8':'01000',  'x9':'01001',  'x10':'01010', 'x11':'01011',
    'x12':'01100', 'x13':'01101', 'x14':'01110', 'x15':'01111',
    'x16':'10000', 'x17':'10001', 'x18':'10010', 'x19':'10011',
    'x20':'10100', 'x21':'10101', 'x22':'10110', 'x23':'10111',
    'x24':'11000', 'x25':'11001', 'x26':'11010', 'x27':'11011',
    'x28':'11100', 'x29':'11101', 'x30':'11110', 'x31':'11111'
    
    }


iType={'addi':  ('000', '0010011'), 'lw':    ('010', '0000011'), 'sltiu': ('011', '0010011'), 'jalr':  ('000', '1100111')}
sType={'sw':    ('010', '0100011')}

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
                    

            

f1=open("test.asm", "r")
instructions=f1.readlines()
l=[]
for i in instructions:
   i=i.replace(",", " ")
   finalList=i.split()
   l.append(finalList)

complete=[]

for i in l:
    incomplete=[]
    if(i[0] in iType):
        if(i[0]=="addi" or i[0]=="sltiu" or i[0]=="jalr"):
            incomplete.append(binaryConverter12(int(i[3])))
            incomplete.append(registers[i[2]])
            func3OP=iType[i[0]]
            incomplete.append(func3OP[0])
            incomplete.append(registers[i[1]])
            incomplete.append(func3OP[1])
            complete.append(incomplete)
        else:
            imm = int(i[2].split('(')[0])       
            h = i[2].split('(')[1].strip(')')
            incomplete.append(binaryConverter12(imm))
            incomplete.append(registers[h])
            func3OP=iType[i[0]]
            incomplete.append(func3OP[0])
            incomplete.append(registers[i[1]])
            incomplete.append(func3OP[1])
            complete.append(incomplete)
    elif(i[0] in sType):
        imm = int(i[2].split('(')[0])
        h = i[2].split('(')[1].strip(')')
        imm_bin = binaryConverter12(imm)
        imm_upper = imm_bin[0:7]   
        imm_lower = imm_bin[7:12]   
        func3OP = sType[i[0]]
        incomplete.append(imm_upper)
        incomplete.append(registers[i[1]])
        incomplete.append(registers[h])
        incomplete.append(func3OP[0])
        incomplete.append(imm_lower)
        incomplete.append(func3OP[1])
        complete.append(incomplete)

    else:
        print("Unknown instruction")

f2 = open("output.txt", "w")
for instruction in complete:
    f2.write(''.join(instruction) + '\n')
f2.close()
f1.close()