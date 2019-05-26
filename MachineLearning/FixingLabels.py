import csv
with open('Set2/labels.csv','r') as csvinput:
    with open('Set2/FixedLabels.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput)

        for row in csv.reader(csvinput):
            if row[1] == "1":
                row.append("0")
                writer.writerow(row)
            else:
                row.append("1")
                writer.writerow(row)