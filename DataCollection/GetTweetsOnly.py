import twint
import time
import os




def getTweets():
    with open('../DataProcessing/graph_users.txt', 'r') as f:
        lines = f.readlines()
        complete_list_of_users = []
    for line in lines:
        complete_list_of_users.append(line.strip())

    print(complete_list_of_users)
    print(len(complete_list_of_users))
    files_done = os.listdir("Graph-Users-tweets")
    print(len(files_done))

    files_done_new = [x[:-4] for x in files_done]
    if ".DS_S" in files_done_new:
        files_done_new.remove(".DS_S")
    print(len(files_done_new))
    for user in files_done_new:
        complete_list_of_users.remove(user)
    print(complete_list_of_users)
    print(len(complete_list_of_users))
    input("")


    for user in complete_list_of_users:
        # saves the tweets in a file
        a = twint.Config()
        a.Username = user
        a.Store_csv = True
        # only save the username, more information can be added. Check: https://github.com/twintproject/twint/wiki/Module
        a.Custom = ["tweet", "retweets", "id"]
        # POISED limits the tweets to 300, the most recent ones
        a.Limit = 500
        a.Output = "Graph-Users-tweets/"+user+".csv"
        twint.run.Profile(a)


getTweets()
while(1):
    try:
        getTweets()
    except TimeoutError:
        time.sleep(60)