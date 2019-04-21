import twint
import time
import os
import asyncio
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def call_twint(user):
    asyncio.set_event_loop(asyncio.new_event_loop())
    # saves the tweets in a file
    a = twint.Config()
    a.Username = user
    a.Store_csv = True
    # username helps check if the tweet actiucally belongs to the user or not
    #a.Custom["tweet"] = ["tweet", "retweets_count", "id", "username"]
    a.Custom = ["tweet", "id", "username", "retweets"]
    # POISED limits the tweets to 300, the most recent ones
    a.Limit = 300
    a.Output = "Graph-Users-tweets/" + user + ".csv"
    twint.run.Profile(a)


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
    #for user in complete_list_of_users:
    #    call_twint(user)
    pool2 = ThreadPool(3)
    pool2.map(call_twint, complete_list_of_users)







getTweets()
while(1):
    try:
        getTweets()
    except TimeoutError:
        time.sleep(60)