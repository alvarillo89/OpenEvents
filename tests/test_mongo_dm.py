# -*- coding: utf-8 -*-

import os
import datetime
import pymongo
import unittest
from bson.objectid import ObjectId

import sys
sys.path.append("src")

from mongo_data_manager import MongoDataManager

class TestEvents(unittest.TestCase):

    def setUp(self):
        # Create client:
        self.client = MongoDataManager(uri=os.environ['DB_URI'], 
            database='EventsDB', collection='events')

        self.sample_event = dict(
            title="Sample title",
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )

        # Insert a sample event (directly with pymongo):
        _id = self.client.collection.insert_one(self.sample_event.copy()).inserted_id
        # Store id:
        self.sample_id = str(_id)


    def tearDown(self):
        # Remove inserted element:
        self.client.collection.delete_many({'title': self.sample_event['title']})


    def test_get_title(self):
        """ Test the query of an existing and non-exising event by title """
        out_ok = self.client.get(key='title', value=self.sample_event['title'])
        out_fail = self.client.get(key='title', value='non-existing title')
        self.sample_event['_id'] = self.sample_id
        self.assertEqual(out_ok, self.sample_event)
        self.assertEqual(out_fail, None)


    def test_get_id(self):
        """ Test the query of an existing and non-exising event by id """
        out_ok = self.client.get(key='_id', value=self.sample_id)
        out_fail = self.client.get(key='_id', value='000000000000000000000000')
        self.sample_event['_id'] = self.sample_id
        self.assertEqual(out_ok, self.sample_event)
        self.assertEqual(out_fail, None)


    def test_insert(self):
        """ Test the insertion of a new element """
        id = self.client.insert(element=self.sample_event)
        event = self.client.collection.find_one({'_id': ObjectId(id)})
        self.sample_event['_id'] = ObjectId(id)
        self.assertEqual(event, self.sample_event)

    
    def test_delete(self):
        """ Test the deletion of an event """
        self.client.delete(self.sample_id)
        event = self.client.collection.find_one({'_id': ObjectId(self.sample_id)})
        self.assertEqual(event, None)


    def test_update(self):
        """ Test the update of an event """
        new_values = dict(title="New Title", organizer="New organizer")
        self.client.update(self.sample_id, new_values)
        event = self.client.collection.find_one({'_id': ObjectId(self.sample_id)})
        self.sample_event['title'] = new_values['title']
        self.sample_event['organizer'] = new_values['organizer']
        self.sample_event['_id'] = ObjectId(self.sample_id)
        self.assertEqual(self.sample_event, event)


if __name__ == "__main__":
    unittest.main(verbosity=2)    