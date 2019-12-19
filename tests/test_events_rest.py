# -*- coding: utf-8 -*-

import hug
import unittest
import datetime
from unittest.mock import MagicMock
from falcon import HTTP_404, HTTP_200, HTTP_201, HTTP_409

import sys
sys.path.append("src")

import events_rest

class TestEventsRest(unittest.TestCase):

    def setUp(self):
        # We use a mock for simulate the datamanager:
        events_rest.event.data_manager = MagicMock()
        self.mock = events_rest.event.data_manager 

        # Create a sample title and id:
        self.sample_title = "Sample title"
        self.sample_id = '000000000000000000000000'

        # Create a sample event:
        self.sample_event = dict(
            _id=self.sample_id,
            title=self.sample_title,
            organizer="An organizer",
            date=datetime.datetime(2020, 5, 17, 18, 30),
            address="In some place",
            description="Just a example event",
            prize=3.0,
            tickets_availables=10
        )


    def test_get_ok(self):
        """ Test the get request of an existing event by title """
        self.mock.get.return_value = self.sample_event
        request = hug.test.get(events_rest, "/event/title/" + self.sample_title)
        # Convert getted string date to datetime object:
        request.data["date"] = datetime.datetime.strptime(request.data["date"], '%Y-%m-%dT%H:%M:%S')
        self.assertEqual(request.status, HTTP_200)
        self.assertEqual(request.data, self.sample_event)
        self.mock.get.assert_called_with(key='title', value=self.sample_title)


    def test_get_not_found(self):
        """ Test the get request of an non-existing event by title """
        self.mock.get.return_value = None
        request = hug.test.get(events_rest, "/event/title/thiseventdoesntexists")
        self.assertEqual(request.status, HTTP_404)
        self.assertEqual(request.data, "Event not found")
        self.mock.get.assert_called_with(key='title', value="thiseventdoesntexists")

    
    def test_post_ok(self):
        """ Test the post request posting a new event """
        del self.sample_event['_id']
        self.mock.get.return_value = None
        self.mock.insert.return_value = self.sample_id

        request = hug.test.post(events_rest, "/event", self.sample_event)
        self.assertEqual(request.status, HTTP_201)
        self.assertEqual("Event Added. ID=" + self.sample_id, request.data)
        self.mock.get.assert_called_with(key='title', value=self.sample_title)
        # Convert the date to string:
        self.sample_event['date'] = self.sample_event['date'].strftime('%Y-%m-%dT%H:%M:%S')
        self.mock.insert.assert_called_with(self.sample_event)


    def test_post_conflict(self):
        """ Test the post request of an event with the same title of other """
        self.mock.get.return_value = self.sample_event
        del self.sample_event['_id']

        request = hug.test.post(events_rest, "/event", self.sample_event)
        self.assertEqual(request.status, HTTP_409)
        self.assertEqual(request.data, 
            "An Event with title {} already exists".format(self.sample_title))
        self.mock.get.assert_called_with(key='title', value=self.sample_event['title'])

    
    def test_delete_ok(self):
        """ Test the delete request of an existing event """
        self.mock.get.return_value = self.sample_event        

        response = hug.test.delete(events_rest, "/event/id/" + self.sample_id)
        self.assertEqual(response.status, HTTP_200)
        self.assertEqual(response.data, "Event removed")
        self.mock.get.assert_called_with(key='_id', value=self.sample_id)


    def test_delete_not_found(self):
        """ Test the delete request of a non-existing event """
        self.mock.get.return_value = None        
        response = hug.test.delete(events_rest, "/event/id/invalid-id")
        self.assertEqual(response.status, HTTP_404)
        self.assertEqual(response.data, "There is no event with that ID")
        self.mock.get.assert_called_with(key='_id', value='invalid-id')


    def test_put_ok(self):
        """ Test the modification of a existing event """
        self.mock.get.return_value = self.sample_event
        new_data = dict(description="A new description", prize=800.0)
        response = hug.test.put(events_rest, "event/id/" + self.sample_id, new_data)
        self.assertEqual(response.status, HTTP_200)
        self.assertEqual(response.data, "Event updated")
        self.mock.get.assert_called_with(key='_id', value=self.sample_id)
        self.mock.update.assert_called_with(self.sample_id, new_data)


    def test_put_fails(self):
        """ Test the modification of a non-existing event and the modification of a bad key """
        new_data = dict(badKey="This is bad")
        # Non existing event:
        self.mock.get.return_value = None
        response = hug.test.put(events_rest, "event/id/invalid-id", new_data)
        self.assertEqual(response.status, HTTP_404)
        self.assertEqual(response.data, "There is no event with that ID")
        self.mock.get.assert_called_with(key='_id', value='invalid-id')
        # Bad key:
        self.mock.get.return_value = self.sample_event
        response = hug.test.put(events_rest, "event/id/" + self.sample_id, new_data)
        self.assertEqual(response.status, HTTP_409)
        self.assertEqual(response.data, "Unknown field in new values")
        self.mock.get.assert_called_with(key='_id', value=self.sample_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)    