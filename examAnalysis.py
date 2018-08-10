# reference: https://www.geeksforgeeks.org/working-csv-files-python/
# importing csv module
import numpy as np
import csv
import sys
import os

if len(sys.argv) < 2:
    print ("python examAnalysis.py <datafile>")
    sys.exit("too few arguments")

# csv file name
filename = sys.argv[1]
 
# initializing the row list, the key (answer to the question) list and item (question: answer list) dictionary
rows = [] #list for 
keys = [] #list for 
items = {} #dictionary for 
mc = []
fr = []
total = []
questions = []
items_1_0 = {}

if os.path.isfile(filename):
    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting key through first row
        keys = next(csvreader)
        keys = keys[0: - 2] #remove 2 empty spaces (data format issue)
        
        numQuestions = len(keys)

        # extracting each data row by row
        for row in csvreader:
            rows.append(row)

        #number of students
        numStudents = csvreader.line_num - 2
else:
    sys.exit("datafile doesn't exist; check your spelling")

# initializing the items dict with question numbers as keys with empty lists.
for q in rows[0][0:numQuestions]:
    items[q] = []
    items_1_0[q] = []
    questions.append(q)

# appending answers list to the items dictionary
for row in rows[1:]:
    # parsing each column of a row
    index = 1
    for col in row[0:numQuestions]:
        items["q"+str(index)].append(col)
        index += 1
    mc.append(float(row[numQuestions]))
    fr.append(float(row[numQuestions + 1]))
    total.append(mc[-1] + fr[-1])

for x, y in zip(questions, keys):
        for z in items[x]:
            if z == y:
                items_1_0[x].append(1)
            else:
                items_1_0[x].append(0)

 
fields = ["Item ID", "# of Students Answered Correct", "# of Students Answered Incorrect",
          "Mean MC Scores of Students Answered Correct", "Mean MC Scores of Students Answered Incorrect", 
          "Mean FR Scores of Students Answered Correct", "Mean FR Scores of Students Answered Incorrect",
          "Mean Total Scores of Students Answered Correct", "Mean Total Scores of Students Answered Incorrect",
          "P Values", "r with MC", "r with FR", "r with MC+FR", "KR-20 if Item Omitted",
          "Key", "#ofA", "#ofB", "#ofC", "#ofD", "#ofE", "#ofF", "%ofA", "%ofB", "%ofC", "%ofD", "%ofE", "%ofF",
          "r of A with FR", "r of B with FR", "r of C with FR", "r of D with FR", "r of E with FR", "r of F with FR"
          ]

#rows
big_data = []
data = dict.fromkeys(fields)

#num of correct students for a question
def correct(id, answer):
    count = 0
    for x in items[id]:
        if x==answer:
            count += 1
    return count

# mean exam score for those who got the correct answer (you can pass in FR or MC exam scores)
def meanCorrect(itemsID, answer, listTestScores):
    sum = 0
    count = 0
    for response, score in zip(items[itemsID], listTestScores):
        if response == answer:
            sum += score
            count += 1
    return round(sum/count, 2)

# mean exam score for those who got the incorrect answer (you can pass in FR or MC exam scores)
def meanIncorrect(itemsID, answer, listTestScores):
    sum = 0
    count = 0
    for response, score in zip(items[itemsID], listTestScores):
        if response != answer:
            sum += score
            count += 1
    if count != 0:
        return round(sum/count, 2)
    else:
        return "-"

# num students who chose that answer choice 
def countAnswerChosen(itemsID, answer):
    count = 0
    for response in items[itemsID]:
        if response == answer:
            count += 1
    return count

# used to calculate correlation of each question with the MC or FRQ scores
def r(id, score, numCorrect):
    if numStudents == numCorrect:
        return "-"
    else:
        return round(np.corrcoef(items_1_0[id],score)[1,0], 2)

# Makes a list of P values of every question   
pVal = []    
for x in range(numQuestions):
    avg = np.mean(items_1_0[questions[x]])
    pVal.append(avg)
        
# kr20 if item omitted
def kr20omit(c, q):
    pTemp = list(pVal)
    pTemp.pop(c)
    qTemp = [1-x for x in pTemp]
    mulval = [a*b for a,b in zip(pTemp,qTemp)]
    pqSum = sum(mulval)
    
    mc1 = list(mc)
    for s in range(numStudents):
        if items_1_0[q][s] == 1:
            mc1[s] = mc1[s]-1
            
    variance = np.var(mc1)
    kr20 = (numQuestions/(numQuestions-1))*(1-pqSum/variance)
    return round(kr20, 2)

# used to calculate correlation of each question's answer choice with FRQ score 
def rChoice(itemsID, choice):
    choice_0_1 = []
    num = 0
    for response in items[itemsID]:
        if response == choice:
            choice_0_1.append(1)
            num += 1
        else:
            choice_0_1.append(0)
    if np.std(choice_0_1)==0:
        return "-"
    else:
        return round(np.corrcoef(choice_0_1, fr)[1,0],2)

#loop through question by question
count = 0
for x, y in zip(questions, keys):
    data["Item ID"] = x
    data["# of Students Answered Correct"] = correct(x, y)
    data["# of Students Answered Incorrect"] = numStudents-data["# of Students Answered Correct"]
    data["Mean MC Scores of Students Answered Correct"] = meanCorrect(x,y,mc)
    data["Mean MC Scores of Students Answered Incorrect"] = meanIncorrect(x,y,mc)
    data["Mean FR Scores of Students Answered Correct"] = meanCorrect(x,y,fr)
    data["Mean FR Scores of Students Answered Incorrect"] = meanIncorrect(x,y,fr)
    data["Mean Total Scores of Students Answered Correct"] = meanCorrect(x,y,total)
    data["Mean Total Scores of Students Answered Incorrect"] = meanIncorrect(x,y,total)
    data["P Values"] = round(data["# of Students Answered Correct"]/numStudents, 2)
    data["r with MC"] = r(x, mc, data["# of Students Answered Correct"])
    data["r with FR"] = r(x, fr, data["# of Students Answered Correct"])
    data["r with MC+FR"] = r(x, total, data["# of Students Answered Correct"])
    data["KR-20 if Item Omitted"] = kr20omit(count, x)
    data["Key"] = y
    data["#ofA"] = countAnswerChosen(x, "a")
    data["#ofB"] = countAnswerChosen(x, "b")
    data["#ofC"] = countAnswerChosen(x, "c")
    data["#ofD"] = countAnswerChosen(x, "d")
    data["#ofE"] = countAnswerChosen(x, "e")
    data["#ofF"] = countAnswerChosen(x, "f")
    addedTotal = data["#ofA"]+data["#ofB"]+data["#ofC"]+data["#ofD"]+data["#ofE"]+data["#ofF"]
    data["%ofA"] = round(data['#ofA']/addedTotal, 2)
    data["%ofB"] = round(data['#ofB']/addedTotal, 2)
    data["%ofC"] = round(data['#ofC']/addedTotal, 2)
    data["%ofD"] = round(data['#ofD']/addedTotal, 2)
    data["%ofE"] = round(data['#ofE']/addedTotal, 2)
    data["%ofF"] = round(data['#ofF']/addedTotal, 2)
    data["r of A with FR"] = rChoice(x,"a")
    data["r of B with FR"] = rChoice(x,"b")
    data["r of C with FR"] = rChoice(x,"c")
    data["r of D with FR"] = rChoice(x,"d")
    data["r of E with FR"] = rChoice(x,"e")
    data["r of F with FR"] = rChoice(x,"f")
    
    count += 1
    big_data.append(data.copy())


PQ = []
    
for x in big_data:
    p = x["P Values"]
    q = 1 - x["P Values"]
    mulval = p*q
    PQ.append(mulval)

pqSum = sum(PQ)
variance = np.var(mc)

kr20 = (numQuestions/(numQuestions-1))*(1-pqSum/variance)
last_row = ["KR-20", str(kr20)]


# name of csv file
filename = "results.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = fields)
     
    # writing headers (field names)
    writer.writeheader()
     
    # writing data rows
    writer.writerows(big_data)

    # writing last row
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(last_row)
