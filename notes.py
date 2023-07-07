string = '#org 1357'
s = string[string.find('#org') + 2:].split()
# s.insert(1, 'nima')

print(s)
print(int(s[1],10))

s = 5
def fu():
    global s
    s +=1
fu()
print(s)

print()
print(type(5.5) in (int, float))

print()
txt = "For only {price:.2f} dollars! {num:03b}"
print(txt.format(price = 49, num = 3))

print()
print("0b{:03b}".format(0b101 % 0b100))  # deleting a bit
print(bin((0b1001>>1) | (0b1001<<(4-1)) & 0xF))     # rotate right 1 bit where the num is a 4-bit binary (N=4)
