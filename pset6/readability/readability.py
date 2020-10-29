text = input("Text : ")
txtLen = len(text)
lettersNum,sentencesNum,wordsNum = 0,0,1
for i in range(txtLen):
    if text[i] in ["!",".","?"]:
        sentencesNum += 1
    elif text[i] == " ":
        wordsNum += 1
    elif text[i].isalpha():
        lettersNum += 1
L = lettersNum / wordsNum * 100
S = sentencesNum / wordsNum * 100
index = int(round(0.0588 * L - 0.296 * S - 15.8))
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print("Grade ",index)