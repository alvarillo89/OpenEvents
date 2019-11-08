# -*- coding: utf-8 -*-

import unittest
import uuid
import datetime

import sys
sys.path.append("src")

import Events

class TestEvents(unittest.TestCase):

    def setUp(self):
        # Create a Events class object:
        self.events = Events.Events()
        # Create a sample event:
        self.sample_id = uuid.uuid1().hex
        self.sample_event = dict(
            ID=self.sample_id,
            title="An event",
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )
        # Add sample event to list:
        self.events.event_list.append(self.sample_event.copy())


    def test_create_ok(self):
        """ Test if a new event is inserted on list """
        event = dict(
            ID=None,
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

        event['ID'] = id

        # Check if new event exists:
        self.assertTrue(event in self.events.event_list)


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
        self.assertEqual(res_found, [self.sample_event])
        self.assertEqual(res_not_found, [])


    def test_search_by_id(self):
        """ Test the search for existing and non-existing events by ID """
        res = self.events.search_by_id(self.sample_id)
        self.assertEqual(res, [self.sample_event])

        with self.assertRaises(LookupError):
            res = self.events.search_by_id("wrong-id")


    def test_remove(self):
        """ Test the remove of existing and non-existing events """
        self.assertTrue(self.sample_event in self.events.event_list)
        self.events.remove(self.sample_id)
        self.assertFalse(self.sample_event in self.events.event_list)

        with self.assertRaises(LookupError):
            self.events.remove("wrong-id")

    
    def test_modify_ok(self):
        """ Test the modification of an event """
        new_values = dict(
            title="I'm changing the name!",
            date=datetime.datetime(2020, 2, 12, 7, 15),
            description="This is the new description",
            prize=2.0
        )

        self.assertTrue(self.sample_event in self.events.event_list)
        self.events.modify(self.sample_id, new_values)

        new_event = dict(
            ID=self.sample_id,
            title="I'm changing the name!",
            organizer="An organizer",
            date=datetime.datetime(2020, 2, 12, 7, 15),
            address="In some place",
            description="This is the new description",
            prize=2.0,
            tickets_availables=10
        )

        self.assertFalse(self.sample_event in self.events.event_list)
        self.assertTrue(new_event in self.events.event_list)
    

    def test_modify_fail(self):
        """ Test exceptions thrown when trying to modify an event in an erroneous way """
        # Non-existing id:
        new_values = dict(title="I'm changing the name!")
        with self.assertRaises(LookupError):
            self.events.modify("wrong-id", new_values)

        # Non-existing argument:
        new_values = dict(invalid_key="invalid")
        with self.assertRaises(KeyError):
            self.events.modify(self.sample_id, new_values)

        # Trying to modify event's ID:
        new_values = dict(ID="my-custom-id")
        with self.assertRaises(KeyError):
            self.events.modify(self.sample_id, new_values)