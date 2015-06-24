import flask
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
import copy
import add_price 
import distance_measure
from distance_measure import two_paragraph_distance as tpd
import item_sentiment
from item_sentiment import get_item_sentiment
import plotly.plotly as py
from plotly.graph_objs import *

#py = plotly(username='ha.luu1207',key='prh430pf04')


#--------------Function for querying the product-----#
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


def list_of_5(items_list):
    item_reviews = MongoClient().dsbc.item_reviews
    list_item = []
    find_item_review = item_reviews.find({"item_id":{"$in":items_list}})
    order_items = find_item_review.sort("star_rating_ave", pymongo.DESCENDING)
    for each_item in order_items:
        list_item.append(each_item)
    return list_item[:5]

def add_distance(user_text,items_list):
    new_list = copy.deepcopy(items_list)
    for each_item in new_list:
        distance = tpd(user_text[0].lower(),each_item['reviews_summary'])
        each_item['distance'] = distance
    return new_list

def plot_sentiment(item,name_plot):
    sent_points = get_item_sentiment(item['item_id'])
    trace0 = Scatter(x=sent_points[0],y=sent_points[1],
                     mode='markers', markers=Marker(size=8),
                     name='reviews sentiment score')
    trace1 = Scatter(x=sent_points[0],y=[0]*len(sent_points[1]),
                     name = "neutral line")
    data = ([trace0,trace1])

    layout = Layout(xaxis=XAxis(title='Time Line',autorange=True),
                    yaxis=YAxis(title='Sentiment score on product',autorange=True),
                    legend=Legend(y=0.5,yref='paper',font=Font(size=10,)), )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename=name_plot)
    return plot_url






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
    #print list_of_concern

    recommended_15_items = list_of_15(priority_concern,list_of_concern)

    item_ids = [i['item_id'] for i in recommended_15_items]

    recommended_5_items =  list_of_5(item_ids)

    recommended_5 = add_price.add_price(recommended_5_items)
    
    

    #####------Trying to add price and distance into my data---------------
    #recommended_items = add_price.add_price(recommended_5_items)
    unsorted_recommended_items = add_distance(data['extra_info'], recommended_5)
    sorted_recommended_items = sorted(unsorted_recommended_items,key=lambda k: k['distance'],reverse=True)    
    recommended_items = sorted_recommended_items[:3]
    
    # plot1 = plot_sentiment(recommended_items[0],'sentiment plot 1')
    # plot2 = plot_sentiment(recommended_items[1],'sentiment plot 2')
    # plot3 = plot_sentiment(recommended_items[2],'sentiment plot 3')
    
    graph_data1 = get_item_sentiment(recommended_items[0]['item_id'])
    new_data1 = np.asarray(graph_data1).T.tolist()
    graph_data2 = get_item_sentiment(recommended_items[1]['item_id'])
    new_data2 = np.asarray(graph_data2).T.tolist()
    graph_data3 = get_item_sentiment(recommended_items[2]['item_id'])
    new_data3 = np.asarray(graph_data3).T.tolist()




    ####-------Result to be return to html----------------------------------
    results = {1:[recommended_items[0]['name'],round(recommended_items[0]['star_rating_ave'],3),
                  recommended_items[0]['number_of_reviews'],recommended_items[0]['reviews_summary'],
                  recommended_items[0]['price']],
               2:[recommended_items[1]['name'],round(recommended_items[1]['star_rating_ave'],3),
                  recommended_items[1]['number_of_reviews'],recommended_items[1]['reviews_summary'],
                  recommended_items[1]['price']],
               3:[recommended_items[2]['name'],round(recommended_items[2]['star_rating_ave'],3),
                  recommended_items[2]['number_of_reviews'],recommended_items[2]['reviews_summary'],
                  recommended_items[2]['price']],
              "graph_data1":new_data1,"graph_data2":new_data2,"graph_data3":new_data3 }
    

     

    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0', port=8000, debug=True)




