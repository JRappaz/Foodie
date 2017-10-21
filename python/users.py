from urllib.request import *
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import requests
import json
import os
import time

url_start = "https://apps.allrecipes.com/v1/users/"
url_end = "/made"

max_made_it = 100

def getUserMadeIt(page, size, user_id, token):
    params = {
        "page": 1,
        "pagesize": 1000
    }
    r = requests.get(url_start + user_id + url_end, params=params, headers={'Authorization': 'Bearer ' + token})
    response = json.loads(r.text)
    
    if "recipes" in response:
        #print("Retrieved user made recipes: " + str(len(response["recipes"])))
        return response["recipes"]
    else:
        print("No recipes")
        return None

def getAllUserMadeIt(user_id, size, token):
    all_made_it = []
    nb_made_it = 0
    page = 1
    while (size - nb_made_it) > max_made_it:
        made_it = getUserMadeIt(page, max_made_it, user_id, token)
        nb_made_it += max_made_it
        page += 1
        if made_it is not None:
            all_made_it = all_made_it + made_it
        
    made_it = getUserMadeIt(page, (size - nb_made_it), user_id, token)
    nb_made_it += (size - nb_made_it)
    if made_it is not None:
        all_made_it = all_made_it + made_it
    
    return all_made_it

def getUserInfos(user_page, user_data):
    infos = ["FollowersCount","FollowingCount","FavoriteCount","MadeRecipesCount","RatingCount","PersonalRecipeSharedCount","SubmittedRecipesCount"]
    
    for info in infos:
        parts = str(user_page).split(info + "\":")
        count = 0
        for s in parts[1:]:
            count = max(int((s.split(",")[0])), count)
        user_data[info] = count    

scrapeToken = None

def scrapeUser(user_id):
    
    directory = 'user_data/' + user_id + "/"
    fname = directory + "recipes.json"
    if os.path.isfile(fname) :
        return False

    
    session = requests.Session()
    r = requests.get("http://allrecipes.com/cook/" + user_id)
    user_page = BeautifulSoup(r.text, 'html.parser')


    token = None
    i = 0
    while token == None:
        time.sleep(0.9)   # delays for 5 seconds.
        print("sleep")
        i += 1
        try:
            token = r.cookies.get_dict()["ARToken"]
        except:
            session = requests.Session()
            r = requests.get("http://allrecipes.com/cook/" + user_id)
            user_page = BeautifulSoup(r.text, 'html.parser')
        if i > 100:
            print("BIG PROBLEM")
            return False

    #print("Scraping User : " + user_id)

    user_data = {}
    
    getUserInfos(user_page, user_data)
    
    
    if os.path.exists(directory):
        i = 3
    else:
        os.makedirs(directory)
    
    with open('user_data/' + user_id + "/data.json", 'w+') as outfile:
        json.dump(user_data, outfile)
         
    made_it = getAllUserMadeIt(user_id, int(user_data["MadeRecipesCount"]), token)
    with open('user_data/' + user_id + "/recipes.json", 'w+') as outfile:
        json.dump(made_it, outfile)
        
    return True


users = pd.read_csv("users.csv")["user_id"]
i = 0
for user in users[200000:]:
    i += 1
    if scrapeUser(str(user)):
        time.sleep(0.9)   # delays for 5 seconds.
        print("sleep")

    if i % 100 == 0:
        print("Scraped " + str(i) + " recipes")