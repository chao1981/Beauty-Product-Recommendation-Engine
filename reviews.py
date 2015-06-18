import pymongo
from pymongo import MongoClient

def reviews(id_list, i):
    reviews_info = {id_list.keys()[i]:id_list.values()[i], "Reviews":[]}
    match_list = MongoClient().dsbc.rbf.find({"asin":{"$in": [id_list.keys()[i]]}})

    for i in match_list:
        reviews_info["Reviews"].append([i['reviewText'],i['overall']])
       
    return reviews_info