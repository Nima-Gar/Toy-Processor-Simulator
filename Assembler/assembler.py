import sys

opcodes = {'JMP':'0', 'ADC':'1', 'XOR':'2', 'SBC':'3', 'ROR':'4', 'TAT':'5', 'OR':'6', 'AND':'8',
           'LDC':'9', 'BCC':'a', 'BNE':'b', 'LDI':'c', 'STT':'d', 'LDA':'e', 'STA':'f' }
immidiate_Needed_Instructions = ('JMP', 'ADC', 'XOR', 'SBC', 'OR', 'AND', 'LDC', 'BCC', 'BNE', 'LDA', 'STA')
jumps = ('JMP', 'BCC', 'BNE')

instructions, insAddresses, variables, labels = [], [], {}, {}
lineAddress = 1

if len(sys.argv) != 2 : 
    print("args must be in this format: assembler.py <sourceFile>")
    sys.exit(1)

file = open(sys.argv[1], 'r')
while True :
    line = file.readline()
    if not line : break

    if line.find('.org') != -1 or line.find('.ORG') != -1:
        line = line.split()
        origin = int(line[1], 16) if (line[1].find("0x") != -1) else int(line[1], 10)

    elif line.find('.data') != -1 or line.find('.Data') != -1 :
        line = line.split()
        variables[line[1]] = "{:03x}".format(origin)
        origin += 1

    else:
        endOfLabel = line.find(':')
        if endOfLabel != -1 :
            label = line[ : endOfLabel].strip()
            labels[label] = "{:03x}".format(lineAddress)
            line = line[endOfLabel+1 : ]
        if line.strip():
            instructions.append(line.strip())
            insAddresses.append("{:03x}".format(lineAddress))
            lineAddress += 1
file.close()

print(f'instructions: {instructions}')
print(f'ins addresses: {insAddresses}')
print(f'variables: {variables}')
print(f'labels: {labels}')


for i in range(0 , len(instructions)) :
    instrcution = instructions[i]
    ins = instrcution.split()
    ins[0] = ins[0].upper()

    if ins[0] in opcodes.keys() :
        opcode = opcodes[ins[0]]
    else :
        print('an unknown instruction has been used!')
        sys.exit(1)

    if len(ins) == 2 and ins[0] not in immidiate_Needed_Instructions :
        print(f"instruction {ins[0]} doesn't accept any value!")
        sys.exit(1)
    elif len(ins) == 1 and ins[0] in immidiate_Needed_Instructions :
        print(f"instruction {ins[0]} needs an immidiate value!")
        sys.exit(1)

    elif len(ins) == 2 :
        if ins[1] in variables.keys() :
            hexNum = variables[ins[1]]
        elif ins[1] in labels.keys() :
            if ins[0] not in jumps :
                print('labels can only be used for jumps')
                exit(1)
            hexNum = labels[ins[1]]
        else :
            hexNum = ins[1][2:] if(ins[1].find('0x') != -1) else "{:03x}".format( int(ins[1], 10) )
        
        instructions[i] = f'{insAddresses[i]} : {opcode} {hexNum} \t\t {instrcution}'
    
    elif len(ins) == 1 :
        instructions[i] = f'{insAddresses[i]} : {opcode} \t\t {instrcution}'
    
    else :
        print(f"instruction {ins[0]} hasn't been used correctly!")
        exit(1)


print()
for ins in instructions :
    print(ins)