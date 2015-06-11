import pymongo
from pymongo import MongoClient


def get_b_product(id_list, i):
    beauty_item_info = {id_list.keys()[i] : id_list.values()[i], 
                    "Reviews" : '', "rating":{"Five_star":0, 
                                              "Four_star":0,
                                              "Three_star":0,
                                              "Two_star":0,
                                              "One_star":0}}
    match_list = MongoClient().dsbc.rbf.find({"asin":{"$in": [id_list.keys()[i]]}})

    for i in match_list:
        beauty_item_info["Reviews"]+=(i['reviewText'])
        if i['overall'] == 5.0:
            beauty_item_info["rating"]["Five_star"] += 1
        elif i['overall'] == 4.0:
            beauty_item_info["rating"]["Four_star"] += 1
        elif i['overall'] == 3.0:
            beauty_item_info["rating"]["Three_star"] += 1
        elif i['overall'] == 2.0:
            beauty_item_info["rating"]["Two_star"] += 1
        else:
            beauty_item_info["rating"]["One_star"] += 1
    return beauty_item_info



def strict_rating(x1,x2,x3,x4,x5,alpha,beta):
    numer = (2*x1+4*x2+3*x3+4*x4+5*x5)+alpha*beta
    denom = float(2*x1+2*x2+x3+x4+x5+beta)
    return numer/denom

def get_reviews (id_list,i):
    beauty_item_info = {id_list.keys()[i] : id_list.values()[i], 
                    "Reviews" : [], "rating":{"Five_star":0, 
                                              "Four_star":0,
                                              "Three_star":0,
                                              "Two_star":0,
                                              "One_star":0}}
    match_list = MongoClient().dsbc.rbf.find({"asin":{"$in": [id_list.keys()[i]]}})

    for i in match_list:
        beauty_item_info["Reviews"].append([i['reviewText']])
        if i['overall'] == 5.0:
            beauty_item_info["rating"]["Five_star"] += 1
        elif i['overall'] == 4.0:
            beauty_item_info["rating"]["Four_star"] += 1
        elif i['overall'] == 3.0:
            beauty_item_info["rating"]["Three_star"] += 1
        elif i['overall'] == 2.0:
            beauty_item_info["rating"]["Two_star"] += 1
        else:
            beauty_item_info["rating"]["One_star"] += 1
    return beauty_item_info