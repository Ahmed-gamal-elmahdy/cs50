from cs50 import get_int

cardNum = get_int("Enter number: ")
lastTwo = str(cardNum)[:2]
length = len(str(cardNum))
sum1,sum2,sum3 = 0,0,0
for i in range(length):
    if i % 2 == 0:
        sum1 += cardNum % 10
    else:
        num = (cardNum % 10) * 2
        if num > 9:
            for j in range(2):
                sum2 += num % 10
                num = int(num / 10)
        else:
            sum2 += num
    cardNum = int(cardNum / 10)
sum3 = sum1 + sum2
if sum3 % 10 == 0:
    if length == 15:
        if int(lastTwo) in [34,37]:
            print("AMEX")
        else:
            print("1 INVALID")
    if length == 16:
        if int(lastTwo) in range(51,56,1):
            print("MASTERCARD")
        elif lastTwo[0] == "4":
            print("VISA")
        else:
            print("INVALID")
    if length == 13:
        if lastTwo[0] == "4":
            print("VISA")
        else:
            print("NVALID")
else:
    print("INVALID")
            
                