from cs50 import get_int
while(True):
    length = get_int("Enter length")
    if length in range(1, 9, 1):
        break
for i in range(length):
    for j in range(length - i - 1):
        print(" ", end="")
    for i2 in range(i + 1):
        print("#", end="")
    print("  ", end="")
    for i3 in range(i + 1):
        print("#", end="")
    print("")
    
    
    
    