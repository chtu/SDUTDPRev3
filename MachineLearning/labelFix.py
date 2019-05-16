import csv
with open('testLabels.csv','r') as csvinput:
    with open('testLabelsProcessed.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)

        for row in csv.reader(csvinput):
            if row[1] == "1":
                writer.writerow(str(row[1])+"0")
            else:
                writer.writerow(str(row[1])+"1")