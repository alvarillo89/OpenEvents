# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

class MongoDataManager:
    def __init__(self, url, database, collection):
        # Create connection:
        self.client = pymongo.MongoClient(url)
        self.collection = self.client[database][collection]

    # Define CRUD operations:
    def insert(self, element):
        _id = self.collection.insert_one(element).inserted_id
        return str(_id)

    def get_title(self, title):
        # None if no object is found:
        out = self.collection.find_one(dict(title=title))
        if out != None:
            out['_id'] = str(out['_id'])
        return out

    def get_id(self, _id):
        # None if no object is found:
        out = self.collection.find_one({"_id": ObjectId(_id)})
        if out != None:
            out['_id'] = str(out['_id'])
        return out

    def update(self, _id, new_values):
        _new_values = {'$set': new_values}
        self.collection.update_one({"_id": ObjectId(_id)}, _new_values)

    def delete(self, _id):
        self.collection.delete_one({"_id": ObjectId(_id)})