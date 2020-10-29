import sys
import csv
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)
csvFileName = sys.argv[1]
Db = {}
n = 0

##read the csv file and put in database Key: list of values
with open(csvFileName, 'r') as file:
    reader = csv.reader(file)
    line_count = 0
    for row in reader:
        n =  len(row)
        clist = []
        for i in range(1,n,1):
            clist.append(row[i])
        Db[row[0]] = clist
## open the sequences file
f = open(sys.argv[2], "r+")
string = f.read()
user = []
##make user sequance = 0
for k in range(n - 1):
    user.append(0)
##loop to check every pattern
for j in range(n - 1):
    word = Db.get("name")[j]
    Length = len(word)
    counter = 1
## loop for that pattern in the text
    for i in range(len(string) - 2 * Length):
        textword = string[i:i+len(word)]
        nextword = string[i + len(word) : i + 2 * len(word)]
        ##check if the current word and the next one are the same
        if(textword == word and nextword == word):
            counter += 1
    ##save the number of repeats 
    user[j] = counter
for the_key, the_value in Db.items():
    counter = 0
    if the_key != "name":
        for i in range(0, len(the_value)): 
                the_value[i] = int(the_value[i]) 
                if(the_value[i] == user[i]):
                    counter += 1
        if (counter + 1 == len(the_value)) or (counter == len(the_value)):
            print(the_key)
            exit(0)
print("No match")
