
while True:
    try:
        val = float(input("Enter kosm change : "))    
        assert val >= 0
    except AssertionError:
        continue
    except ValueError:
        continue
    else:
        break 
    
cents = round(float(val) * 100)
steps = 0
while cents >= 25:
    cents -= 25
    steps += 1
while cents >= 10:
    cents -= 10
    steps += 1
while cents >= 5:
    cents -= 5
    steps += 1
while cents >= 1:
    cents -= 1
    steps += 1
print(steps, end="")