# -*- coding: utf-8 -*-

import unittest
import os
import datetime

import sys
sys.path.append("src")

import Events
from mongo_data_manager import MongoDataManager

class TestEvents(unittest.TestCase):

    def setUp(self):
        # Create a Events class object:
        self.MD = MongoDataManager(url=os.environ['EVENTS_DB_URL'], database='EventsDB', 
            collection='events')
        self.events = Events.Events(data_manager=self.MD)
        # Create a sample event:
        self.sample_event = dict(
            title="An event",
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )
        # Add sample event to database:
        self.sample_id = self.MD.insert(self.sample_event)
        self.sample_event['_id'] = self.sample_id

    
    def tearDown(self):
        # Borrar el evento añadido:
        self.MD.delete(self.sample_id)


    def test_create_ok(self):
        """ Test if a new event is inserted on list """
        event = dict(
            _id=None,
            title="Another event",
            organizer="Another organizer",
            date=datetime.datetime(2020, 6, 17, 17, 30),
            address="In another place",
            description="Just another example event",
            prize=5.0,
            tickets_availables=100
        )

        id = self.events.create("Another event", "Another organizer", 
            datetime.datetime(2020, 6, 17, 17, 30), "In another place", 
            "Just another example event", 5.0, 100)

        event['_id'] = id

        # Check if new event exists:
        self.assertEqual(self.MD.get_title("Another event"), event)

        # Remove recent added event:
        self.MD.delete(id)


    def test_create_fail(self):
        """ Ensure that you cannot insert two events with same title """
        with self.assertRaises(ValueError):
            self.events.create(
                self.sample_event["title"], self.sample_event["organizer"], 
                self.sample_event["date"], self.sample_event["address"], 
                self.sample_event["description"], self.sample_event["prize"],
                self.sample_event["tickets_availables"]
            )

    
    def test_search_by_title(self):
        """ Test the search for existing and non-existing events by name """
        res_found = self.events.search_by_title(self.sample_event["title"])
        res_not_found = self.events.search_by_title("Non-existing event")
        self.assertEqual(res_found, self.sample_event)
        self.assertEqual(res_not_found, None)


    def test_search_by_id(self):
        """ Test the search for existing and non-existing events by ID """
        res = self.events.search_by_id(self.sample_id)
        self.assertEqual(res, self.sample_event)

        with self.assertRaises(LookupError):
            res = self.events.search_by_id("000000000000000000000000")


    def test_remove(self):
        """ Test the remove of existing and non-existing events """
        self.events.remove(self.sample_id)
        self.assertEqual(self.MD.get_title(self.sample_event), None)

        with self.assertRaises(LookupError):
            self.events.remove("000000000000000000000000")

    
    def test_modify_ok(self):
        """ Test the modification of an event """
        new_values = dict(
            title="I'm changing the name!",
            date=datetime.datetime(2020, 2, 12, 7, 15),
            description="This is the new description",
            prize=2.0
        )

        self.events.modify(self.sample_id, new_values)

        new_event = dict(
            _id=self.sample_id,
            title="I'm changing the name!",
            organizer="An organizer",
            date=datetime.datetime(2020, 2, 12, 7, 15),
            address="In some place",
            description="This is the new description",
            prize=2.0,
            tickets_availables=10
        )

        event = self.MD.get_id(self.sample_id)
        self.assertNotEqual(event, self.sample_event)
        self.assertEqual(event, new_event)
    

    def test_modify_fail(self):
        """ Test exceptions thrown when trying to modify an event in an erroneous way """
        # Non-existing id:
        new_values = dict(title="I'm changing the name!")
        with self.assertRaises(LookupError):
            self.events.modify("000000000000000000000000", new_values)

        # Non-existing argument:
        new_values = dict(invalid_key="invalid")
        with self.assertRaises(KeyError):
            self.events.modify(self.sample_id, new_values)

        # Trying to modify event's ID: 
        new_values = dict(_id="my-custom-id")
        with self.assertRaises(KeyError):
            self.events.modify(self.sample_id, new_values)


if __name__ == "__main__":
    unittest.main(verbosity=2)    