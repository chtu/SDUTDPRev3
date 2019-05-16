import csv
with open('testVectors.csv','r') as csvinput:
    with open('testVectorsProcessed.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)

        for row in csv.reader(csvinput):
            writer.writerow(row[1:])
