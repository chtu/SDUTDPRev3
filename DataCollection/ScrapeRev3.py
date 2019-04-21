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
    try:
        c = twint.Config()
        c.Username = user
        # only save the username, more information can be added. Check: https://github.com/twintproject/twint/wiki/Module
        c.Custom = ["username"]
        c.Store_csv = True
        # POISED does not include users with more than 2000 followers
        # We are including them but with a limit of 2000
        c.Limit = 500
        c.Output = user+"/followers.csv"
        twint.run.Followers(c)

        b = twint.Config()
        b.Username = user
        # only save the username, more information can be added. Check: https://github.com/twintproject/twint/wiki/Module
        b.Custom = ["username"]
        b.Store_csv = True
        # POISED does not imclude users with more than 2000 followees
        # We are including them but with a limit of 2000
        b.Limit = 500
        b.Output = user+"/following.csv"
        twint.run.Following(b)
    except TimeoutError:
        pass


def return_associated_user(subdir, user):
    with open(user+"-2/"+subdir+"/stronglyConnectedUsers.txt", "r") as f:
        lines = f.readlines()
    strongly_connected_users = []
    for line in lines:
        strongly_connected_users.append(line.strip())
    if ".DS_Store" in strongly_connected_users:
        strongly_connected_users.remove(".DS_Store")
    return strongly_connected_users


def get_followers(sub_user, user):
    try:
        with open(user+"-3/"+sub_user+"/followers.csv", "r") as f:
            lines = f.readlines()
        followers = []
        for line in lines:
            followers.append(line.strip())
        if "username" in followers:
            followers.remove("username")
        return followers
    except FileNotFoundError:
        return None


def get_followees(sub_user, user):
    try:
        with open(user+"-3/"+sub_user+"/following.csv", "r") as f:
            lines = f.readlines()
        followees = []
        for line in lines:
            followees.append(line.strip())
        if "username" in followees:
            followees.remove("username")
        return followees
    except FileNotFoundError:
        return None

# level 1
def level1(user):
    os.mkdir(user)
    os.chdir(user)
    get_user_information(user)
    os.chdir("..")
    # extract the list of users who and both follower and followee
    # read from followers
    followers = get_followers(user, user)
    followees = get_followees(user, user)
    print(len(followers))
    print(len(followees))
    strongly_connected_users = []
    for item in followers:
        if item in followees:
            strongly_connected_users.append(item)
    print(len(strongly_connected_users))
    print(strongly_connected_users)
    input("Enter key")
    os.chdir(user)
    with open('stronglyConnectedUsers.txt', 'w') as users_file:
        for item in strongly_connected_users:
            users_file.write("%s\n" % item)
    os.chdir("..")
    return


# level 2
def leve2(user):

    os.chdir(user)
    with open('stronglyConnectedUsers.txt', 'r') as f:
        lines = f.readlines()
    strongly_connected_users = []
    for line in lines:
        strongly_connected_users.append(line.strip())
    print(strongly_connected_users)
    pool = ThreadPool(10)
    pool.map(get_user_information, strongly_connected_users)

    os.chdir("..")
    return


def level2_associated_users_list(user):
    list_of_users = os.listdir(user)
    list_of_users.remove("stronglyConnectedUsers.txt")
    for x in list_of_users:
        stronglyConnectedUsers = []
        followers = get_followers(x, user)
        followees = get_followees(x, user)
        for y in followers:
            if y in followees:
                stronglyConnectedUsers.append(y)
        with open(user+"/"+x+'/stronglyConnectedUsers.txt', 'w') as users_file:
            for item in stronglyConnectedUsers:
                users_file.write("%s\n" % item)

def level3(user):
    # get complete list of followers and followees
    list_of_directories = os.listdir(user+"-2")

    print(len(list_of_directories))
    input("Enter Key")
    if "stronglyConnectedUsers.txt" in list_of_directories:
        list_of_directories.remove("stronglyConnectedUsers.txt")
    if ".DS_Store" in list_of_directories:
        list_of_directories.remove(".DS_Store")
    level2_list = []
    for item in list_of_directories:
        level2_list.extend(return_associated_user(item, user))
        #print(item)
    os.chdir(user+"-3")
    print("total users: "+str(len(level2_list)))
    print("total unique users: "+str(len(set(level2_list))))
    input("Enter key")
    directories_done = os.listdir("../"+user + "-3")
    for item in set(level2_list):
        if item in directories_done:
            level2_list.remove(item)
    print("total users: "+str(len(level2_list)))
    print("total unique users: "+str(len(set(level2_list))))
    input("Enter key")
    pool2 = ThreadPool(100)
    pool2.map(get_user_information, level2_list)


def level3_associated_users_list(user):
    list_of_users = os.listdir(user+"-3")
    if "stronglyConnectedUsers.txt" in list_of_users:
        list_of_users.remove("stronglyConnectedUsers.txt")
    if ".DS_Store" in list_of_users:
        list_of_users.remove(".DS_Store")
    for x in list_of_users:
        stronglyConnectedUsers = []
        followers = get_followers(x, user)
        followees = get_followees(x, user)
        try:
            for y in followers:
                if y in followees:
                    stronglyConnectedUsers.append(y)
        except TypeError:
            pass
        with open(user+"-3/"+x+'/stronglyConnectedUsers.txt', 'w') as users_file:
            for item in stronglyConnectedUsers:
                users_file.write("%s\n" % item)


def threading(user):
    # level 1


    #level1(user)


    # level 2
    #leve2(user)
    #level2_associated_users_list(user)
    #level3(user)
    level3_associated_users_list(user)








threading('Daddythompson2')

# test seed catattack
# catattack101
# kaydeekraig

