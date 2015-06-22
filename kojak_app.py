import flask
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient


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

@app.route("/recommendation", methods=["POST"])
def recommendation():
	"""
	When a POST request with json data is made to this url,
	read the data from json, find the beauty product, then
	return the response
	"""
	data = flask.request.json
	
	priority_concern = data["priority"][0]
	other_concerns = data["others"][0].split(",")

	list_of_concern = data["priority"]+ data["skin_type"] + other_concerns

	list_of_concern = list(set(list_of_concern))
	print list_of_concern

	recommended_items =list_of_10(priority_concern,list_of_concern) 

	results = {1:[recommended_items[0]['name'],recommended_items[0]['price']],
			   2:[recommended_items[1]['name'],recommended_items[1]['price']],
			   3:[recommended_items[2]['name'],recommended_items[2]['price']]} 	

	return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0', port=8000, debug=True)




