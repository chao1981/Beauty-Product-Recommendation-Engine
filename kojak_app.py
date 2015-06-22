import flask
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient()


#--------------Function for querying the product-----#
def list_of_10(priority,concern_list):
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
    number_of_items = min(10,x.count())
    list_of_items = []
    for i in xrange(number_of_items):
        list_of_items.append(x.sort(priority,pymongo.DESCENDING)[i])
    
    return list_of_items 





#-------------URLS AND WEB PAGES---------------------#

#Initialize the app
app = flask.Flask(__name__)

#Homepage
@app.route("/")
def viz_page():
	"""
	Homepage: serve our visualization page, awake_beauty.html
	"""
	with open("awake_beauty.html", 'r') as viz_file:
		return viz_file.read()

@app.route("/recommendation", method=["POST"])
	"""
	When a POST request with json data is made to this url,
	read the data from json, find the beauty product, then
	return the response
	"""
	data = flask.request.json
	
	priority_concern = data["priority"]

	list_of_concern = data["priority"]+ data["skin_type"] +data["others"]

	list_of_concern = list(set(list_of_concern))

	recommended_items =list_of_10(priority_concern,list_of_concern) 	
	# CAN I DO :recommended_product = list_of_3(*data.values()) ???

	#this is in case the return json does not act like a dictionary :
	#data_dict = json.loads(data)[0]



