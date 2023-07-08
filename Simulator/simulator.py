import sys
from tkinter import ttk
from tkinter import *

memory = {}
instrcutions, labels, varAddresses = {}, {}, {}
lineAddress = 1
A , T = 0 , 0
z , c = 0 , 0

if len(sys.argv) != 2 : 
    print("args must be in this format: simulator.py <sourceFile>")
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
        varAddress = "{:03x}".format(origin)
        varAddresses[line[1]] = varAddress
        memory[varAddress] = int(line[2] , 10) if (len(line) == 3)  else 0
        origin += 1

    else:
        endOfLabel = line.find(':')
        if endOfLabel != -1 :
            label = line[ : endOfLabel].strip()
            labels[label] = "{:03x}".format(lineAddress)
            line = line[endOfLabel+1 : ]
        
        instruction = line.strip()
        if instruction:
            instruction = instruction.split()
            if len(instruction) == 2 :
                instruction[1] = instruction[1][2:] if(instruction[1].find('0x') != -1)  else instruction[1]
                instruction = f'{instruction[0]} {labels[instruction[1]]}' if(instruction[1] in labels.keys())   else f'{instruction[0]} {instruction[1]}'
            else :
                instruction = instruction[0]

            addr = "{:03x}".format(lineAddress)
            instrcutions[addr] = instruction
            memory[addr] = instruction
            lineAddress += 1
file.close()

pc = 1
lastInsAddress = int(list(instrcutions)[-1] , 16)

while pc <= lastInsAddress :
    lastPC = pc
    ins = instrcutions["{:03x}".format(pc)]
    ins = ins.split()
    
    if ins[0].lower() == 'sta':
        # ins[1] is a variable or the address of a value in memory
        dest = varAddresses[ins[1]] if (ins[1] in varAddresses.keys()) else ins[1]

    elif len(ins) == 2 :
        # ins[1] is a variable (that we get its value from memory)
        # or the address of a value in memory
        # otherwise it's the addrees of an instruction existing in memory (that we want to put it in pc)
        ins[1] = memory[varAddresses[ins[1]]] if(ins[1] in varAddresses.keys()) else memory[ins[1]] if(type(memory[ins[1]]) in (int , float)) else ins[1]
    
    match ins[0].lower() :
        case 'jmp':
            pc = int(ins[1],16)

        case 'adc':
            A += ins[1]
            z = int(A == 0)
            c = int(A > (2**16-1))
            A = A-2**16 if (c==1)  else A
            

        case 'xor':
            A ^= ins[1]
            z = int(A == 0)
            c = 0

        case 'sbc':
            A -= ins[1]
            z = int(A == 0)
            c = int(A < 0)

        case 'ror':
           # adding c as the right bit
           A = A << 1
           A = A | c
           # rotate right
           # (n>>d) | (n<<(N-1)) & 0xFFF...
           A = (A>>1) | (A<<(16-1)) & 0xFFFF                                          # A is a 16-bit binary so 4 hex digits are needed            
           # seprating new c
           c = A & 0b0000000000000001
           A = A >> 1

           z = (A==0)

        case 'tat':
            T = A

        case 'or':
            A |= ins[1]
            z = int(A == 0)
            c = 0

        case 'and':
            A &= ins[1]
            z = int(A == 0)
            c = 0

        case 'ldc':
            A = ins[1]
            c = 0

        case 'bcc':
            pc = int(ins[1], 16) if (c == 1)  else pc

        case 'bne':
            pc = int(ins[1], 16) if (z == 0)  else pc

        case 'ldi':
            A = memory["{:03x}".format(A)]

        case 'stt':
            memory["{:03x}".format(A)] = T

        case 'lda':
            A = ins[1]

        case 'sta':
            memory[dest] = A


    if pc == lastPC : pc += 1


print(f'memory: {memory}')
print(f'instrcutions: {instrcutions}')
print(f'labels: {labels}')
print(f'varAddresses: {varAddresses}')


def onComboChange(event):
    combo = event.widget.get()
    
    global memToDiplay
    global varsToDiplay

    if listToDisplay == 'memory' :
        memToDiplay = memory
        lastKey = list(memToDiplay.keys())[-1]

        for cell , content in memToDiplay.items() :

            match combo :
                case 'Int' :
                    memToDiplay[int(cell,16)] = memToDiplay[cell]
                    del memToDiplay[cell]
                    if type(content) not in (int, float) :
                        content = content.split()
                        if (content[1] not in varAddresses.keys()) : memToDiplay[int(cell,16)] = f'{content[0]} {int(content[1],16)}'
                # case 'Binary'
            
            if cell == lastKey : break
    
    display(True, listToDisplay)


def display(displayContetnt , liName):
    global txt_output
    global combo
    global listToDisplay

    if not displayContetnt :
        listToDisplay = liName
        newWindow = Toplevel()    
        newWindow.geometry("800x470+340+150")
        newWindow.title("Values")
        newWindow ['background'] = '#118da8'

        Label(newWindow , text = 'Memory Cells' , fg = 'white' , bg = '#118da8' , pady = 30 , font=('Helvetica bold', 20)).pack()
        
        combo = ttk.Combobox(newWindow, state='readonly' , values=['Binary','Hex','Int'], font = ('Helvetica bold', 13) , width=43)
        ttk.Style().configure(combo, relief='raised')
        combo.place(x = 150 , y = 300)
        combo.bind("<<ComboboxSelected>>", onComboChange)
        combo.pack()

        txt_output = Text(newWindow, font=('Helvetica bold', 13) , height=17, width=40)
        txt_output.pack(pady=14)

    if displayContetnt :
        txt_output.delete("1.0", END)
        if listToDisplay == 'memory' :
            for addr , val in memToDiplay.items() :
                txt_output.insert(END, f'\t            {addr}  :  {val}' + "\n")

    

   

win = Tk()
win.title('Simulator Menu')
win.geometry('800x470+340+150')
win ['background'] = '#20bbc9'

Label(text = 'Amounts of Registers', bg='#20bbc9', font=('Helvetica bold', 24)).place(x = 413 , y = 58 , anchor = CENTER)
Label(text = f'A = {A}', fg = 'white' , bg='#20bbc9', font=('Helvetica bold', 24)).place(x = 410 , y = 138 , anchor = CENTER)
Label(text = f'T = {T}' , bg='#20bbc9', font=('Helvetica bold', 24)).place(x = 410 , y = 217 , anchor = CENTER)
Button(text='Display Memory', fg = 'black' , bg='white', font=('Helvetica bold', 20), width = 27, height = 2  , command = lambda : display(False, 'memory') ).place(x = 183 , y = 277)
Button(text='Display Variables', fg = 'black' , bg='white', font=('Helvetica bold', 20), width = 27, height = 2  , command = lambda : display(False, 'vars') ).place(x = 183 , y = 367)
win.mainloop()