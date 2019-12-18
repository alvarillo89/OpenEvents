# -*- coding: utf-8 -*-

import os
import datetime
import unittest
from unittest.mock import MagicMock

import sys
sys.path.append("src")

import Events

class TestEvents(unittest.TestCase):

    def setUp(self):
        # We use a mock for simulate the datamanager:
        self.mock = MagicMock()
        # Create a Events class object with the mock:
        self.events = Events.Events(data_manager=self.mock)

        # Create a sample event:
        self.sample_event = dict(
            title="Sample title",
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )

        # Create a sample id:
        self.sample_id = '000000000000000000000000'


    def test_create_ok(self):
        """ Test if a new event is inserted on list """
        # Configure the mock for returning an id on insert, and None on get:
        self.mock.insert.return_value = self.sample_id
        self.mock.get.return_value = None

        id = self.events.create(
            self.sample_event["title"], self.sample_event["organizer"], 
            self.sample_event["date"], self.sample_event["address"], 
            self.sample_event["description"], self.sample_event["prize"],
            self.sample_event["tickets_availables"]
        )

        # Ensure that mock had been called with correct arguments:
        self.mock.insert.assert_called_with(self.sample_event)
        self.mock.get.assert_called_with(key='title', value=self.sample_event['title'])
        self.assertEqual(id, self.sample_id)

        
    def test_create_fail(self):
        """ Ensure that you cannot insert two events with same title """
        # Configure the mock for returning the sample event:
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        with self.assertRaises(ValueError):
            self.events.create(
                self.sample_event["title"], self.sample_event["organizer"], 
                self.sample_event["date"], self.sample_event["address"], 
                self.sample_event["description"], self.sample_event["prize"],
                self.sample_event["tickets_availables"]
            )

        # Ensure that insert method hadn't been called:
        self.mock.insert.assert_not_called()

    
    def test_search_by_title(self):
        """ Test the search for existing and non-existing events by name """
        # Existing event:
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        res_found = self.events.search_by_title(self.sample_event["title"])
        self.assertEqual(res_found, self.sample_event)
        self.mock.get.assert_called_with(key='title', value=self.sample_event['title'])

        # Non-existing event:
        self.mock.get.return_value = None        
        
        res_not_found = self.events.search_by_title("Non-existing event")
        self.assertEqual(res_not_found, None)
        self.mock.get.assert_called_with(key='title', value="Non-existing event")


    def test_search_by_id(self):
        """ Test the search for existing and non-existing events by ID """
        # Existing event:
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        res = self.events.search_by_id(self.sample_id)
        self.assertEqual(res, self.sample_event)
        self.mock.get.assert_called_with(key='_id', value=self.sample_id)

        # Non-existing event:
        self.mock.get.return_value = None

        with self.assertRaises(LookupError):
            res = self.events.search_by_id("000000000000000000000000")

        self.mock.get.assert_called_with(key='_id', value=self.sample_id)


    def test_remove_ok(self):
        """ Test the remove of a existing event """
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        self.events.remove(self.sample_id)
        self.mock.get.assert_called_with(key='_id', value=self.sample_id)
        self.mock.delete.assert_called_with(self.sample_id)        

    
    def test_remove_fail(self):
        """ Test the remove of a non-existing event """
        self.mock.get.return_value = None

        with self.assertRaises(LookupError):
            self.events.remove("non-existing-id")
        
        self.mock.get.assert_called_with(key='_id', value="non-existing-id")
        self.mock.delete.assert_not_called()

    
    def test_modify_ok(self):
        """ Test the modification of an event """
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        new_values = dict(
            title="I'm changing the name!",
            date=datetime.datetime(2020, 2, 12, 7, 15),
            description="This is the new description",
            prize=2.0
        )

        self.events.modify(self.sample_id, new_values)

        self.mock.get.assert_called_with(key='_id', value=self.sample_id)
        self.mock.update.assert_called_with(self.sample_id, new_values)
    

    def test_modify_fail_non_existing_event(self):
        """ Test exceptions thrown when trying to modify a non-existing event """
        self.mock.get.return_value = None

        new_values = dict(title="I'm changing the name!")
        with self.assertRaises(LookupError):
            self.events.modify("non-existing-id", new_values)

        self.mock.get.assert_called_with(key='_id', value="non-existing-id")
        self.mock.update.assert_not_called()
        

    def test_modify_fail_invalid_key(self):
        """ Test exceptions thrown when trying to modify an event in an erroneous way """
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        # Non-existing argument:
        new_values = dict(invalid_key="invalid")
        with self.assertRaises(KeyError):
            self.events.modify(self.sample_id, new_values)

        self.mock.get.assert_called_with(key='_id', value=self.sample_id)
        self.mock.update.assert_not_called()


    def test_modify_fail_update_id(self):
        """ Test exceptions thrown when trying to modify an event in an erroneous way """
        self.sample_event['_id'] = self.sample_id
        self.mock.get.return_value = self.sample_event

        # Trying to modify event's ID: 
        new_values = dict(_id="my-custom-id")
        with self.assertRaises(KeyError):
            self.events.modify(self.sample_id, new_values)

        self.mock.get.assert_called_with(key='_id', value=self.sample_id)
        self.mock.update.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)    