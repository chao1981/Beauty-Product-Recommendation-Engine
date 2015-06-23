from __future__ import division, unicode_literals 
import pymongo
from pymongo import MongoClient
import nltk
from textblob import TextBlob as tb
import math
from datetime import datetime
from dateutil import parser


def get_item_sentiment(item_asin):
    beauty_item_info = {"item_id":item_asin,"Reviews":[]}
    rbf = MongoClient().dsbc.rbf
    match_list = rbf.find({"asin": item_asin})

    for i in match_list:
        review_time = parser.parse(i['reviewTime'])
        review_sentiment = tb(i['reviewText']).sentiment.polarity
        
        beauty_item_info["Reviews"].append([review_time,review_sentiment])
        
    X = [beauty_item_info['Reviews'][j][0] for j in range(len(beauty_item_info['Reviews']))]
    y = [beauty_item_info['Reviews'][j][1] for j in range(len(beauty_item_info['Reviews']))]
    return [X,y]