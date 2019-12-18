# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

class MongoDataManager:
    def __init__(self, uri, database, collection):
        # Create connection:
        self.client = pymongo.MongoClient(uri)
        self.collection = self.client[database][collection]


    # Define CRUD operations:
    def insert(self, element):
        _id = self.collection.insert_one(element.copy()).inserted_id
        return str(_id)


    def get(self, key, value):
        # None if no object is found:
        if key == '_id':
            out = self.collection.find_one({'_id': ObjectId(value)})
        else:
            out = self.collection.find_one({key: value})

        if out != None:
            out['_id'] = str(out['_id'])

        return out


    def update(self, _id, new_values):
        _new_values = {'$set': new_values}
        self.collection.update_one({"_id": ObjectId(_id)}, _new_values)


    def delete(self, _id):
        self.collection.delete_one({"_id": ObjectId(_id)})