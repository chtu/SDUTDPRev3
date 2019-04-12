import os
from shutil import copyfile
import twint

'''
The way twint 1.2.0 and 1.1.4.3 collect tweets is different.
Use 1.2.0 for this one and 1.1.4.3 for the previous data collection
'''

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
    c = twint.Config()
    c.Username = user
    c.Store_csv = True
    c.Output = "StronglyConnectedUsers/"+user+".csv"
    c.Limit = 500
    c.Hide_output = True
    c.Retweets = True
    # Run
    print(user)
    twint.run.Search(c)
