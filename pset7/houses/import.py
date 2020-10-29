from cs50 import SQL
import sys,csv

if len(sys.argv) != 2:
    print("Usage: pyhton file1.py house ")
    exit(1)
db = SQL("sqlite:///students.db")
with open(sys.argv[1]) as file:
    reader = csv.DictReader(file)
    for row in reader:
      name =  row['name'].split(" ");
      house = row['house']
      birth = row['birth']
      if(len(name) == 3):
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ? , ?)", name[0], name[1], name[2], house, birth)
      elif(len(name) == 2):
        db.execute("INSERT INTO students (first, last, house, birth) VALUES(?, ?, ? , ?)", name[0], name[1], house, birth)
