import os
from shutil import copyfile
import twint


os.mkdir('StronglyConnectedUsers/')

complete_list_of_users = []

# open file and read the content in a list
with open('complete_list_of_users.txt', 'r') as f:
    for line in f:
        item = line[:-1]
        # add item to the list
        complete_list_of_users.append(item)
print((len(complete_list_of_users)))

for user in complete_list_of_users:
    # copy the file from Data Collection to Strongly Connected User:
    # saves the tweets in a file
    try:
        src = "/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/DataCollection/Graph-Users-tweets/"+user+".csv"
        dst = "/Users/savanpatel/Desktop/sfsu/research/spamDetection/SDUTDPRev3/DataProcessing/StronglyConnectedUsers/"+user+".csv"
        copyfile(src, dst)
    except FileNotFoundError:
        pass
