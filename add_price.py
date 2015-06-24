import pymongo
from pymongo import MongoClient
import copy

def add_price(item_dict_list):
    pd_info = MongoClient().dsbc.product_info
    new_list = copy.deepcopy(item_dict_list)

    for item in new_list:
        list_id = pd_info.find({"asin":item['item_id']})
        info = list(list_id)[0]
        item["price"] = info['price']
    return new_list
