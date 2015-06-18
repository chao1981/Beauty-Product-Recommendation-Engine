import flask
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient()


#--------------Function for querying the product-----#
def list_of_3(priority,dry_score,oily_score,combination_score,sensitive_score,acne_score,sensitive_score,sunscreen_score,anti_aging_score,redness_score):
	client = MongoClient()
	smarter_profile = client.dsbc.smarter_profile
	pipeline = [{"$project":{"name":1,"item_id":1,"price":1}},
				{"$match":{"dry_skin_score":{"$gt":dry_score},
				 		   "oily_skin_score":{"$gt":oily_score},
				 		   "combination_skin_score":{"$gt":combination_score},
				 		   "sensitive_score":{"$gt":sensitive_score},
				 		   "acne_score":{"$gt":acne_score},
				 		   "sunscreen_score":{"$gt":sunscreen_score},
				 		   "anti_aging_score":{"$gt":anti_aging_score},
				 		   "redness_score":{"$gt":redness_score}}},
				 {"$sort":{"$$priority":-1}},
				 {"$limit":3}]
	list_of_products = smarter_profile.aggregate(pipeline)
	return list_of_products





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

	# CAN I DO :recommended_product = list_of_3(*data.values()) ???

	#this is in case the return json does not act like a dictionary :
	#data_dict = json.loads(data)[0]



