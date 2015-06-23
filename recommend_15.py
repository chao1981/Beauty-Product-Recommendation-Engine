import pymongo
from pymongo import MongoClient

# This function get user priority concern as well as a list of concern
# and out put a list of 15 best product for the user. 


def list_of_15(priority,concern_list):
    dd ={"dry_skin_score":-0.1,"oily_skin_score":-0.1, 
         "sensitive_score":-0.1,"sunscreen_score":-0.1,
         "combination_skin_score":-0.1,"redness_score":-0.1,
         "anti_aging_score":-0.1,"acne_score":-0.1}

# concern_list = ["dry_skin_score", "acne_score"]
    for concern in concern_list:
        dd[concern]=0.0
    
    sp = MongoClient().dsbc.smarter_profile
    x = sp.find({"dry_skin_score":{"$gt":dd["dry_skin_score"]}, "oily_skin_score":{"$gt":dd["oily_skin_score"]},
                 "sensitive_score":{"$gt":dd["sensitive_score"]},"sunscreen_score":{"$gt":dd["sunscreen_score"]},
                 "combination_skin_score":{"$gt":dd["combination_skin_score"]}, "redness_score":{"$gt":dd["redness_score"]},
                 "anti_aging_score":{"$gt":dd["anti_aging_score"]},"acne_score":{"$gt":dd["acne_score"]}})
    number_of_items = min(15,x.count())
    list_of_items = []
    for i in xrange(number_of_items):
        list_of_items.append(x.sort(priority,pymongo.DESCENDING)[i])
    
    return list_of_items       