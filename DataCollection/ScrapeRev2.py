import twint
import os
import time
from datetime import datetime
import argparse
import shutil
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import sys
import asyncio


# Instantiate the parser
parser = argparse.ArgumentParser()


def get_user_information(user):
    asyncio.set_event_loop(asyncio.new_event_loop())

    print("Fetching " + user + " followers, followees and tweets")

    try:
        os.makedirs(user)
    except FileExistsError:
        return

    c = twint.Config()
    c.Username = user
    # only save the username, more information can be added. Check: https://github.com/twintproject/twint/wiki/Module
    c.Custom = ["username"]
    c.Store_csv = True
    # POISED does not include users with more than 2000 followers
    # We are including them but with a limit of 2000
    c.Limit = 60
    c.Output = user+"/followers.csv"
    twint.run.Followers(c)

    b = twint.Config()
    b.Username = user
    # only save the username, more information can be added. Check: https://github.com/twintproject/twint/wiki/Module
    b.Custom = ["username"]
    b.Store_csv = True
    # POISED does not imclude users with more than 2000 followees
    # We are including them but with a limit of 2000
    b.Limit = 60
    b.Output = user+"/following.csv"
    twint.run.Following(b)

    '''
    a = twint.Config()
    a.Username = user
    a.Store_csv = True
    # only save the username, more information can be added. Check: https://github.com/twintproject/twint/wiki/Module
    a.Custom = ["tweet", "retweets", "id"]
    # POISED limits the tweets to 300, the most recent ones
    a.Limit = 500
    a.Output = user+"/tweets.csv"
    twint.run.Profile(a)
    '''

    # get the list of followers
    try:
        with open(user+"/followers.csv") as f:
            followers_list = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        followers_list = [x.strip() for x in followers_list]
        f.close()
        # delete "username" from the list
        if "username" in followers_list:
            followers_list.remove("username")
    except FileNotFoundError:
        followers_list = []
        pass

    try:
        with open(user+"/following.csv") as f:
            followee_list = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
            followee_list = [x.strip() for x in followee_list]
        f.close()
        # delete "username" from the list
        if "username" in followee_list:
            followee_list.remove("username")
    except FileNotFoundError:
        followee_list = []
        pass

    return followee_list + followers_list


def only_return_followers_followees(sub_user, user):
    # get the list of followers
    os.chdir(user)
    try:
        with open(sub_user+"/followers.csv") as f:
            followers_list = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        followers_list = [x.strip() for x in followers_list]
        f.close()
        # delete "username" from the list
        if "username" in followers_list:
            followers_list.remove("username")
    except FileNotFoundError:
        followers_list = []
        pass

    try:
        with open(sub_user+"/following.csv") as f:
            followee_list = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
            followee_list = [x.strip() for x in followee_list]
        f.close()
        # delete "username" from the list
        if "username" in followee_list:
            followee_list.remove("username")
    except FileNotFoundError:
        followee_list = []
        pass
    os.chdir("..")
    return followee_list + followers_list


# level 1
def level1(user):
    os.mkdir(user+"-hop1")
    os.chdir(user+"-hop1")
    associated_users = get_user_information(user)
    # write the list of user's for continuation when code breaks
    temp_list = associated_users
    with open('associated_users.txt', 'w') as users_file:
        for item in temp_list:
            users_file.write("%s\n" % item)
    print(len(associated_users))
    input("Enter key")
    pool = ThreadPool(len(associated_users))
    pool.map(get_user_information, associated_users)
    os.chdir("..")
    return


# level 2
def level2(user):
    # get complete list of followers and followees
    list_of_directories = os.listdir(user+"-hop1")

    print(len(list_of_directories))
    input("Enter Key")
    if "associated_users.txt" in list_of_directories:
        list_of_directories.remove("associated_users.txt")
    level2_list = []
    for item in list_of_directories:
        level2_list.extend(only_return_followers_followees(item, user))
        #print(item)
    os.chdir(user)
    print("total users: "+str(len(level2_list)))
    print("total unique users: "+str(len(set(level2_list))))
    input("Enter key")

    pool2 = ThreadPool(100)
    pool2.map(get_user_information, level2_list)


def threading(user):
    # level 1
    '''
    a = datetime.now()
    level1(user)
    b = datetime.now()
    print(b-a)
    time.sleep(60)
    '''

    # level 2
    try:
        input("Enter key")
        level2(user)
    except TimeoutError:
        pass

    while 1:
        try:
            level2(user)
        except TimeoutError:
            time.sleep(1200)
            pass








threading('Daddythompson2')

# test seed catattack
# catattack101
# kaydeekraig

